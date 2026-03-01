# GitHub Webhook Events Dashboard

This is a Flask application that receives events from GitHub (via Webhooks), stores them in a MongoDB database, and dynamically presents them on a live, real-time dashboard.

## Prerequisites

Before you can run the project, ensure you have the following installed on your machine:
*   [Python 3.8+](https://www.python.org/downloads/)
*   [MongoDB](https://www.mongodb.com/try/download/community) (Running locally on default port `27017`)
*   [Git](https://git-scm.com/)

---

## 🚀 Setup & Running Instructions

### 1. Clone the repository
```bash
git clone https://github.com/pigeio/TechStaX.git
cd TechStaX
```

### 2. Create and connect to a virtual environment
**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the dependencies
```bash
pip install -r requirements.txt
```

### 4. Ensure MongoDB is running
By default, the application connects to a MongoDB database hosted at `mongodb://localhost:27017/github_events`.
Ensure the MongoDB Service is running in your background on your OS.

### 5. Run the Flask application
```bash
python run.py
```

### 6. View the Dashboard
Open your web browser and navigate to:
```
http://127.0.0.1:5000/
```
*(The dashboard will initially say "Waiting for events..." until a GitHub webhook hits the API and populates the MongoDB!).*

---

## 🔗 Testing with Real GitHub Webhooks

To test with real events:
1.  Since GitHub cannot post webhooks directly to your `localhost` address, you must tunnel your local port to the internet using a tool like [Ngrok](https://ngrok.com/).
    ```bash
    ngrok http 5000
    ```
2.  Go to a GitHub repository of your choosing (Settings -> Webhooks -> Add Webhook).
3.  Set the **Payload URL** to your generated `<ngrok_url>/webhook/receiver`.
4.  Set the **Content type** to `application/json`.
5.  Select **"Let me select individual events."** and ensure **Pushes** and **Pull requests** are checked.
6.  Start pushing code or opening PRs to that GitHub repository and watch the events populate on your local dashboard!