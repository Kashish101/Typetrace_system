# 🔐 TypeTrace — Secure Keylogger Monitoring System

> A secure, ethical, and research-oriented keylogging system built with Python and React.js — designed for cybersecurity research, parental control, and authorized user monitoring.

---

## 📸 Screenshots

### Dashboard — Light Theme
![TypeTrace Dashboard Light](./dashboard_light.png)

### Dashboard — Dark Theme
![TypeTrace Dashboard Dark](./dashboard_dark.png)

---

## 📌 Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Workflow](#workflow)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Security](#security)
- [Future Enhancements](#future-enhancements)
- [Team](#team)
- [License](#license)

---

## 📖 About

**TypeTrace** is a secure and ethical keylogging system built for cybersecurity research, parental control, and authorized user monitoring. It combines a Python-based keylogger backend with a modern React.js management console, allowing users to:

- Start/stop keylogging sessions remotely
- Monitor real-time system stats (CPU, memory, disk usage)
- View logging stats (keystrokes logged, screenshots taken, commands received)
- Export and analyse encrypted logs securely

> ⚠️ **Disclaimer:** TypeTrace is intended **only** for ethical, authorized, and legal use. Unauthorized keylogging is illegal and a violation of privacy. Always obtain proper consent before monitoring any system.

---

## ✨ Features

- 🖥️ **Real-time Dashboard** — Monitor CPU, memory, and disk usage live
- ▶️ **Remote Start/Stop** — Control keylogging sessions from the web UI
- 📊 **Logging Stats** — Track keystrokes logged, screenshots taken, and commands received
- 🔒 **AES Encryption** — All captured keystrokes are encrypted before storage
- 🌗 **Light/Dark Theme** — Toggle between themes with one click
- 📁 **CSV Export** — Export logs for further analysis
- 📈 **Graphical Reports** — Visualize keystroke data with charts
- 🔑 **Authentication** — Only authorized users can access the system

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React.js |
| Backend | Python, Flask |
| Keylogger | Python (Pynput) |
| Encryption | AES (Cryptography library) |
| Database | MongoDB |
| Backend Hosting | Render |
| Frontend Hosting | Vercel |
| Version Control | GitHub |

---

## 🏗️ System Architecture

```
┌─────────────────────┐       ┌──────────────────────┐
│   React.js Frontend │ <───> │   Flask API (Backend) │
│   (Management UI)   │       │   + Auth + Encryption │
└─────────────────────┘       └──────────┬───────────┘
                                          │
                              ┌───────────▼───────────┐
                              │   Keylogger Module     │
                              │   (Python + Pynput)    │
                              └───────────┬───────────┘
                                          │
                              ┌───────────▼───────────┐
                              │   MongoDB Database     │
                              │   (Encrypted Logs)     │
                              └───────────────────────┘
```

---

## 🔄 Workflow

1. User logs into the React web application
2. User starts/stops keylogging from the dashboard
3. The Flask API processes the request and activates the keylogger in the background
4. Keystrokes are captured, AES-encrypted, and stored in MongoDB
5. User can view logs, analyse keystrokes via graphical reports, and export as CSV

---

## 📂 Project Structure

```
TypeTrace/
├── frontend/               # React.js UI
│   ├── src/
│   │   ├── components/     # Dashboard, Config, Charts
│   │   └── App.js
│   └── package.json
├── backend/                # Flask API
│   ├── app.py              # Main Flask server
│   ├── keylogger.py        # Pynput keylogger module
│   ├── encryption.py       # AES encryption logic
│   └── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB (local or Atlas)

### Setup

```bash
# Clone the repository
git clone https://github.com/your-username/TypeTrace.git
cd TypeTrace/backend

# Install dependencies
pip install -r requirements.txt

# Run Flask server
python app.py
```

### Environment Variables

Create a `.env` file in the backend directory:

```env
MONGO_URI=your_mongodb_connection_string
SECRET_KEY=your_secret_key
ENCRYPTION_KEY=your_aes_encryption_key
```

---

## 🔐 Security

- **AES Encryption** — All keystroke logs are encrypted using AES before being stored
- **Authentication** — JWT-based login; only authorized users can access the dashboard
- **Auto-deletion** — Logs are automatically purged after a configurable retention period
- **Ethical Use Only** — The system is designed with consent-based monitoring in mind

---

## 🔮 Future Enhancements

- 🤖 **AI-based Keystroke Analysis** — Detect user behaviour anomalies using ML models
- 👥 **Role-Based Access Control (RBAC)** — Admin and User access levels
- ☁️ **Cloud Storage Integration** — AWS S3 / Firebase for multi-device access
- 📱 **Mobile App** — React Native app for on-the-go management
- 🔔 **Real-Time Alerts** — Notifications for suspicious keystroke patterns
- 🕐 **Activity Scheduling** — Define time intervals for monitoring sessions
- 🔍 **Advanced Log Filtering** — Search logs by timestamp or key type
- 🔑 **Two-Factor Authentication (2FA)** — Extra security layer for login


> *"TypeTrace is not just a keylogger — it's a step toward cybersecurity innovation and responsible monitoring."*
