
# 🏥 Medilink - Integrated Healthcare Platform

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)


**Medilink** is an integrated HealthTech solution that brings together three modular apps — **Aspatre**, **Medilink**, and **Medtech** — each serving a unique purpose in the healthcare ecosystem. This unified platform facilitates appointment booking, chatbot-based assistance, treatment tracking, hospital-patient communication, bed availability tracking, and much more.

## 🎥 Project Demo

Download and watch: https://drive.google.com/file/d/1P0PIU_pZeQ5yaJXOTOPKs-72mYKPAn_2/view?usp=sharing
---

## 📁 Project Structure

```

final\_meditech\_project/
│
├── aspatre/        # Django app for user auth & hospital services
│   ├── accounts/
│   ├── aspatre/
│   └── manage.py
│
├── c\_bot/          # Frontend chatbot with JS, HTML, CSS
│   ├── Index.html
│   ├── script.js
│
├── medilink/       # Telemedicine app
│   └── telemed\_project/
│       └── manage.py
│
├── medtech/        # Bed tracking & treatment file sharing
│   └── meditech/
│       └── manage.py
│
└── README.md

````

---

## 🚀 Features

### ✅ Aspatre
- Django-based hospital & user authentication
- Appointment booking
- Profile management

### 🤖 C_Bot
- Chatbot frontend
- Simple query handling interface

### 💊 Medtech & Medilink
- QR code-based treatment file sharing
- Telemedicine consultations
- Hospital bed availability tracker
- Mobile clinic booking
- Email and notification system
- Google Maps integration

---

## ⚙️ How to Run the Project (Multi-App Integration)

We have many functionalities divided into **3 separate apps**, and each needs to be run **on a separate port** using **different terminals**.

---

### 1️⃣ Aspatre

📍 **Runs on port 8000**  
📂 Path: `final_meditech_project/aspatre`

```bash
cd aspatre
py manage.py runserver
````

🔗 Open in browser: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

✅ Make sure this is running before moving to others.

---

### 2️⃣ Medilink (Telemedicine)

📍 **Runs on port 1111**
📂 Path: `final_meditech_project/medilink/telemed_project`

```bash
cd medilink/telemed_project
py manage.py runserver 1111
```

🔗 Open in browser: [http://127.0.0.1:1111/](http://127.0.0.1:1111/)

⚠️ Must be run in a separate terminal window.

---

### 3️⃣ Medtech (Bed Tracker & File Sharing)

📍 **Runs on port 2222**
📂 Path: `final_meditech_project/medtech/meditech`

```bash
cd medtech/meditech
py manage.py runserver 2222
```

🔗 Open in browser: [http://127.0.0.1:2222/](http://127.0.0.1:2222/)

```

---

## 🔑 API Keys & Configuration

### 🗺️ Medtech – GeoLocation API

📂 File: `user_dashboard.html`


```js
GeoLocationApi-456223
const API_KEY = "your_key"  // Replace with your actual Google Maps API key
```

> 👤 **Test Login**
> Username: `meditech`
> Email: `meditech@gmail.com`
> Password: `meditech`

---

### 📧 Medilink – Email Configuration

📂 File: `settings.py` (inside `telemed_project`)

> 👤 **Test Login**
Username: medilink
Email address: medilink@gmail.com
Password: medilink

```python
EMAIL_HOST_USER = 'your_email'  # Replace with your actual email address
EMAIL_HOST_PASSWORD = 'a_secret_key'  # Use app password or real email password
```

> 🛡️ Make sure you've enabled "less secure apps" or used a secure app password from your Gmail settings.

---

### 🤖 C\_Bot API Key

📂 File: `c_bot/script.js`

```js
const API_KEY = "YOUR_APIKEY_HERE";  // Replace with your actual API key
```

---

### 🔐 Aspatre API Key

📂 File: `aspatre/static/script.js`

```js
const API_KEY = "your_api_key_here";  // Replace with your actual API key
```

---

## 🛠️ Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite
* **APIs:** Google Maps, Email Services
* **Other Tools:** QR Code, Chatbot Interface, Notifications

---

## 💡 Future Scope

* Merge all apps under one unified Django project
* Integrate chatbot with backend via API
* Add REST API for mobile app support
* Implement role-based dashboards
* Add JWT or Allauth-based authentication

---

## ⚙ Requirements

Make sure you have Python and Django installed:

bash
pip install django

---

## 🧑‍💻 Developer Instructions
Ensure all required packages are installed in your Python environment. You may need to configure environment variables, and use SQLite (or migrate to PostgreSQL as needed).

---

## 👨‍💻 Author

**Abhinav Shetty**
II Year Project | Dayananda Sagar Academy of Technology and Management
Passionate about HealthTech, AI, and Full-Stack Development

```
Happy Coding! 👨‍⚕️💻

