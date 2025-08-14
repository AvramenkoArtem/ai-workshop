## ✅ Prerequisites

- A Google Account (create one at https://accounts.google.com/signup)

---

## 🧩 Step 1: Create a Google Account

If you don’t already have one, create a Google account:

👉 https://accounts.google.com/signup

---

## 🏗️ Step 2: Set Up a Google Cloud Project

1. Go to the Google Cloud Console:  
   👉 https://console.cloud.google.com/
2. Click on **"Select a project" > New Project**
3. Enter a **Project name** (e.g., `Workshop`)
4. Click **Create**

---

## 📬 Step 3: Enable Gmail API

1. In the Google Cloud Console, go to:  
   **APIs & Services > Library**
2. Search for **Gmail API**
3. Click on it and hit **Enable**

---

## 🛡️ Step 4: Configure OAuth Consent Screen

1. Go to: **APIs & Services > OAuth consent screen**
2. Choose **"External"** and click **Create**
3. Fill in information and press next at each step of the wizard:
   - **App name**: e.g., `Workshop`
   - **User support email**: your Google account email used for workshop
   - **Developer contact info**: your email, could be the same as above
4. Click **Save and Continue** (no need to add scopes or test users now)
5. Click **Back to Dashboard** when done

---

## 🔐 Step 5: Create OAuth 2.0 Credentials

1. Go to: **APIs & Services > Credentials**
2. Click **"Create Credentials" > "OAuth client ID"**
3. Set:
   - **Application type**: `Desktop app`
   - **Name**: `Workshop`
4. Click **Create**
5. Download the `credentials.json` file
6. Save it in your Python project folder

---

## 🔐 Step 6: Add test user
1. Go to: **APIs & Services > OAuth consent screen**
2. Choose **"Audience"** and add email
