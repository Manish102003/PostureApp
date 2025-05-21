

# 🧍‍♂️ PostureApp - Posture Detection & Correction Web App

**PostureCheck** is a full-stack web application designed to detect posture deformities in real-time and provide personalized corrective exercise recommendations. With secure user authentication, the app ensures each user can track and improve their posture over time to prevent health issues such as back pain and fatigue.

## 🔍 Features

* 🧠 **AI-Powered Posture Detection**
  Real-time posture analysis using OpenCV and MediaPipe.

* 🔐 **User Authentication**
  Secure login/signup functionality using Django's built-in authentication system.

* 📊 **Personalized Dashboards**
  Custom dashboards where users can monitor their posture history and receive tailored corrective exercise plans.

* 🔄 **History Tracking**
  Users can view their past analyses and track their posture improvement over time.

* 🧘‍♀️ **Exercise Recommendations**
  Intelligent suggestions for stretches and strengthening exercises based on specific posture issues detected.

## 🛠 Tech Stack

* **Backend**: Django (Python)
* **Frontend**: HTML,BootStrap CSS
* **Computer Vision**: OpenCV, MediaPipe
* **Database**: SQLite (can be configured for PostgreSQL or others)
* **Authentication**: Django Auth system

## 🚀 Getting Started

### Prerequisites

* Python 3.8
* pip
* virtualenv (optional but recommended)

### Installation

1. **Clone the repository:**

   ```bash
   git clone (https://github.com/Manish102003/PostureApp.git)
   cd PostureApp
   ```

2. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Start the development server:**

   ```bash
   python manage.py runserver
   ```

6. **Open your browser** and go to `http://127.0.0.1:8000/`
