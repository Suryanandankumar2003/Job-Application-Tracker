import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px
import re

# st.markdown("""
#     <style>
#     div[data-testid="stToolbar"] {
#         display: none;
#     }
#     </style>
# """, unsafe_allow_html=True)


from streamlit_cookies_manager import EncryptedCookieManager

#  COOKIE SETUP 
cookies = EncryptedCookieManager(
    prefix="job_tracker",
    password="af54cbd4ed33e25377488556edcb7c55"
)

if not cookies.ready():
    st.stop()

#  EMAIL VALIDATION 
def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

#  STREAMLIT CONFIG 
st.set_page_config(page_title="Job Tracker", layout="wide")

#  DATABASE 
conn = sqlite3.connect("jobs.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    user_job_id INTEGER,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    status TEXT,
    date TEXT,
    notes TEXT
)
""")

conn.commit()

#  AUTH FUNCTIONS 
def signup(name, email, password):
    try:
        email = email.strip().lower()
        if not is_valid_email(email):
            return "invalid"

        c.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()
        return "success"
    except:
        return "exists"


def login_user(email, password):
    email = email.strip().lower()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    return c.fetchone()

#  SESSION INIT 
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

#  RESTORE FROM COOKIE 
if not st.session_state.logged_in:
    email_cookie = cookies.get("user_email")
    name_cookie = cookies.get("user_name")

    if email_cookie and name_cookie:
        st.session_state.logged_in = True
        st.session_state.user_email = email_cookie.lower()
        st.session_state.user_name = name_cookie

#  AUTH UI 
if not st.session_state.logged_in:
    st.title("🔐 Auth System")

    menu = st.radio("Choose", ["Login", "Sign Up"])

    if menu == "Sign Up":
        name = st.text_input("Full Name")
        email = st.text_input("Email").strip().lower()
        password = st.text_input("Password", type="password")

        if st.button("Create Account"):
            result = signup(name, email, password)

            if result == "success":
                st.success("Account created!")
            elif result == "invalid":
                st.error("Invalid email format")
            else:
                st.error("Email already exists")

    else:
        email = st.text_input("Email").strip().lower()
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login_user(email, password)

            if user:
                st.session_state.logged_in = True
                st.session_state.user_email = user[2]
                st.session_state.user_name = user[1]

                # SAVE COOKIE
                cookies["user_email"] = user[2]
                cookies["user_name"] = user[1]
                cookies.save()

                st.rerun()
            else:
                st.error("Invalid credentials")

    st.stop()

#  MAIN APP 
user_email = st.session_state.user_email
user_name = st.session_state.user_name

st.title(f"📌 Job Tracker : {user_name}")
st.sidebar.markdown(f"👤 Logged in as: {user_name}")

#  LOGOUT FIX 
if st.sidebar.button("🚪 Logout"):
    cookies["user_email"] = ""
    cookies["user_name"] = ""
    cookies.save()

    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.session_state.user_name = ""

    st.rerun()

#  JOB FUNCTIONS 
def add_job(email, company, role, status, date, notes):
    c.execute("SELECT MAX(user_job_id) FROM jobs WHERE email=?", (email,))
    last_id = c.fetchone()[0]
    new_id = 1 if last_id is None else last_id + 1

    c.execute("""
        INSERT INTO jobs (email, user_job_id, company, role, status, date, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (email, new_id, company, role, status, date, notes))
    conn.commit()


def get_jobs(email):
    c.execute("""
        SELECT user_job_id, company, role, status, date, notes
        FROM jobs
        WHERE email=?
        ORDER BY user_job_id DESC
    """, (email,))

    data = c.fetchall()

    return pd.DataFrame(data, columns=[
        "Job ID", "Company", "Role", "Status", "Date", "Notes"
    ])


def update_job(email, job_id, company, role, status, date, notes):
    c.execute("""
        UPDATE jobs
        SET company=?, role=?, status=?, date=?, notes=?
        WHERE email=? AND user_job_id=?
    """, (company, role, status, date, notes, email, job_id))
    conn.commit()


def delete_job(email, job_id):
    c.execute("""
        DELETE FROM jobs
        WHERE email=? AND user_job_id=?
    """, (email, job_id))
    conn.commit()

#  ADD JOB 
st.sidebar.header("➕ Add Job")

company = st.sidebar.text_input("Company")
role = st.sidebar.text_input("Role")
status = st.sidebar.selectbox("Status", ["Applied", "Interview", "Rejected", "Offer"])
date = st.sidebar.date_input("Date")
notes = st.sidebar.text_area("Notes")

if st.sidebar.button("Add Job"):
    if company and role:
        add_job(user_email, company, role, status, str(date), notes)
        st.success("Job added!")
        st.rerun()

#  DATA 
df = get_jobs(user_email)

#  TABLE 
st.subheader("📋 Applications")
st.dataframe(df, use_container_width=True)

#  EDIT 
st.subheader("✏️ Edit Job")

edit_id = st.number_input("Enter Job ID", min_value=1)

if st.button("Load Job"):
    job = df[df["Job ID"] == edit_id]

    if not job.empty:
        st.session_state.edit_data = job.iloc[0].to_dict()
    else:
        st.error("Job not found")

if "edit_data" in st.session_state:
    data = st.session_state.edit_data

    company = st.text_input("Company", value=data["Company"])
    role = st.text_input("Role", value=data["Role"])
    status = st.selectbox(
        "Status",
        ["Applied", "Interview", "Rejected", "Offer"],
        index=["Applied", "Interview", "Rejected", "Offer"].index(data["Status"])
    )
    date = st.date_input("Date", value=pd.to_datetime(data["Date"]))
    notes = st.text_area("Notes", value=data["Notes"])

    if st.button("Update Job"):
        update_job(user_email, data["Job ID"], company, role, status, str(date), notes)
        st.success("Updated!")
        del st.session_state.edit_data
        st.rerun()

#  DELETE 
st.subheader("🗑 Delete Job")

delete_id = st.number_input("Enter Job ID to Delete", min_value=1)

if st.button("Delete Job"):
    delete_job(user_email, delete_id)
    st.success("Deleted!")
    st.rerun()

#  DASHBOARD 
st.subheader("📊 Dashboard")

if not df.empty:
    status_counts = df["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]

    st.plotly_chart(
        px.pie(status_counts, names="Status", values="Count", hole=0.4),
        use_container_width=True
    )

    st.plotly_chart(
        px.bar(status_counts, x="Status", y="Count", text="Count"),
        use_container_width=True
    )
else:
    st.info("No data yet")
