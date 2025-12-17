# Plex Collection Creator 🎬

This is a custom Python application that helps users manage and organize their Plex movie libraries by building themed collections. Whether you're a fan of franchises like _Harry Potter_ or studios like _A24_, this tool streamlines the process of grouping titles into collections.
![Uploading CleanShot 2025-12-17 at 20.54.28@2x.png…]()

## <img width="1282" height="1484" alt="CleanShot 2025-08-07 at 16 13 03@2x" src="https://github.com/user-attachments/assets/ef08fb26-52c1-4797-b566-2d1169688b39" />

## 🛠️ Setup

1. **Clone the repository.**
2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**

   ```bash
   python main.py
   ```

4. **Enter your credentials when prompted.**  
   You’ll need your Plex Token, Plex URL, and (optionally) a TMDb API key.

---

## 🔐 Credentials Required

On first run, you’ll be prompted to enter your Plex Token, Plex URL, and optionally a TMDb API key via the **Configure Credentials** option in the main menu. These credentials are securely saved in a local `config.json` file (excluded from version control).

---

### 📎 Finding Your Plex Token & URL

- **Plex Token:**

  1. Sign in at [app.plex.tv](https://app.plex.tv)
  2. Click on any Movie/Show → ⋮ → **Get Info**
  3. Click **View XML** at the bottom
  4. In the browser URL, copy the string after `X-Plex-Token=`

- **Plex URL:**
  1. Open Plex in your browser.
  2. Go to **Settings** (wrench icon) → **Remote Access**.
  3. Copy the URL shown under "Remote Access".
     - Use the **Private URL** if you’re on your home Wi-Fi or LAN.
     - Use the **Public URL** if you’re outside your network.

---

## 📦 Why Use This?

This app is designed for individuals who use Plex as a personal media server to catalog and enjoy their legally acquired digital media — including backups of physical media like DVDs and Blu-rays. It supports better curation, discoverability, and enjoyment of your existing library.

---

## ⚙️ Features

- Automatically group movies into collections using TMDb (optional).
- Manual entry and studio-based collection options.
- TMDb API key is optional — fallback logic supports limited use without it.
- Local config management via built-in UI (no need to edit files manually).

---

This project was developed as part of a software development assignment and is intended for educational and personal use only.
