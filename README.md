![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

# Backend API

This repository contains the backend service of the [Expense Manager Project](https://github.com/pCarboneroDev/expensesManager). The API is built using **FastAPI**, with **SQLAlchemy** as the ORM and **SQLite** as the database for development purposes. A migration to **PostgreSQL** is planned for future production use (not yet implemented).

---

## 🚧 Project Status

> ✅ The project is actively developed and functional.  
> ⚠️ The API is still evolving — some features may change before the first stable release.  
> 🗄️ PostgreSQL is **planned but not yet implemented** — SQLite remains the active database.

---

## 🛠️ Tech Stack

* **Framework:** FastAPI
* **ORM:** SQLAlchemy
* **Database (current):** SQLite
* **Database (planned):** PostgreSQL (not yet implemented)

---

## 🗄️ Database

Currently, the project uses **SQLite** for simplicity and local development.

* No additional setup is required.
* The database file will be created automatically when the application runs for the first time.

### 🔄 Future Plans

* Migration to **PostgreSQL**
* Integration with migration tools (e.g., Alembic)
* Improved scalability and production readiness

---

## ▶️ Execution Guide

Follow these steps to run the project locally:

### 1. Clone the repository

```bash
git clone https://github.com/pCarboneroDev/expensesManager-backend.git
cd expensesManager-backend
```

### 2. (Optional) Create virtual environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python main.py
```