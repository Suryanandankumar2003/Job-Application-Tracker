# 📌 Job Application Tracker

A simple and interactive **Job Application Tracker** built using Streamlit.
This application helps users manage and track their job applications efficiently with authentication and analytics.

---

## 🚀 Features

* 🔐 User Authentication (Login / Signup)
* 🍪 Persistent Login using Cookies
* ➕ Add Job Applications
* ✏️ Edit Existing Applications
* 🗑 Delete Applications
* 📊 Dashboard with Visual Insights (Pie & Bar Charts)
* 💾 SQLite Database Integration

---

## 🛠 Tech Stack

* **Frontend & Backend:** Streamlit
* **Database:** SQLite
* **Visualization:** Plotly
* **Language:** Python

---

## 📂 Project Structure

```bash
Job-Application-Tracker/
│── main.py
│── jobs.db (auto-created)
│── README.md
│── .gitignore
│── requirements.txt
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/job-application-tracker.git
cd job-application-tracker
```

---

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate:

* Windows:

```bash
venv\Scripts\activate
```

* Mac/Linux:

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install streamlit pandas plotly streamlit-cookies-manager
```

---

## ▶️ Run the Application

```bash
python -m streamlit run main.py
```

Open in browser:

```
http://localhost:8501
```

---

## 🔑 Usage

1. Sign up with your name, email, and password
2. Login to access your dashboard
3. Add job applications from the sidebar
4. Track job status (Applied, Interview, Offer, Rejected)
5. Edit or delete applications anytime
6. View analytics using charts

---

## 📊 Dashboard Preview

* Pie Chart → Application status distribution
* Bar Chart → Number of applications per status

---

## 📸 Screenshots

*Sign Up Page*
<img width="1807" height="762" alt="image" src="https://github.com/user-attachments/assets/5487ab85-ea74-4223-8ce0-2150aa8ab326" />


*Login Page*
<img width="1795" height="584" alt="image" src="https://github.com/user-attachments/assets/a8ba76c1-691c-4510-953b-d3e0ebef6913" />



*Main Page*

<img width="1811" height="863" alt="image" src="https://github.com/user-attachments/assets/45a9d270-43ef-49e7-8360-9d0008e810fa" />

---

## 🔐 Security Note

* Passwords are currently stored in plain text
* Recommended improvement: use hashing (e.g., bcrypt)

---

## 🧠 Future Improvements

* 🔒 Secure authentication (hashed passwords)
* ☁️ Deployment on AWS / Streamlit Cloud
* 📧 Email notifications for job updates
* 📱 Responsive UI improvements

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork this repository and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Suryanandan Kumar**

GitHub: https://github.com/Suryanandankumar2003
