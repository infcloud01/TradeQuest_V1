# ⚔️ TradeQuest | Automated Trading RPG & Analytics Workstation

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![TailwindCSS](https://img.shields.io/badge/Frontend-Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![ChartJS](https://img.shields.io/badge/Analytics-Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://www.chartjs.org)

TradeQuest is an institutional-grade, self-hosted performance logging framework that converts clinical execution metrics into real-time RPG character telemetry. By bridging mechanical chart executions with psychological risk evaluation, it turns disciplined risk management into an interactive experience. 

The application deploys a fully automated, asynchronous background worker that hooks directly into the **TradeLocker live API network gateway**, automatically checking your ledger, processing closed transactions, and updating performance metrics without the latency or recurring token fees of external live LLM APIs.

---

## 🗺️ System Overview & Architecture

```text
  ┌────────────────────────┐         🚀 Polling Daemon (Every 60s)         ┌─────────────────────────┐
  │  TradeLocker Exchange  │ ────────────────────────────────────────────> │  TradeQuest Core Engine │
  │   Live Broker Ledger   │                                               │    (FastAPI / SQLite)   │
  └────────────────────────┘                                               └─────────────────────────┘
                                                                                        │
         ┌──────────────────────────────────────────────────────────────────────────────┤
         ▼ (Saves State)                                                                ▼ (Serves Render UI)
 ┌────────────────┐                                                      ┌───────────────────────────┐
 │ Local Database │ <─────────────────────────────────────────────────── │ Dual-Pane Interface HTML5 │
 │ (tradequest.db)│                Reads Live Profile States             │  • /play   • /dashboard   │
 └────────────────┘                                                      └───────────────────────────┘
                                                                                        ▲
                                                                Local Network Link      │
                                                           (Wi-Fi / Private LAN Port) ──┘
                                                                                        │
                                                                             ┌──────────────────────┐
                                                                             │  Client Mac/iPhone   │
                                                                             └──────────────────────┘
```

### 💎 Key Features
* **Automated TradeLocker Core Engine:** An asynchronous polling loop that safely synchronizes your live broker execution stream every 60 seconds. Features a rigorous single-execution safeguard via structural `broker_order_id` checks to eliminate double-counting older history.
* **30-Day Historical Lookback Guardrail:** Keeps database indexing scalable by automatically ignoring data sets older than 30 days during active ledger polls.
* **Dual-Pane Interface Workstation:**
  * `⚔️ /play (Game Arena)`: Displays character levels, rank progression, stats (Discipline, Patience, Risk Management, Consistency), active multi-quest bounties, and boss combat zones.
  * `📊 /dashboard (Workstation)`: Tracks metrics including win rate %, profit factor ratios, and active session win rates, and maps an interactive monthly calendar matrix with custom weekly roll-ups.
* **Dynamic Lookback Window Switcher:** Instant chart macro scaling allows you to transition your performance bar chart among **7 Days**, **30 Days**, and **90 Days** views on the fly.
* **Local Behavioral AI Coach:** Built-in clinical critique widget ("Jesse") that calculates trading telemetry to identify psychological weaknesses (over-leveraging, win-cutting, revenge trading) and issues targeted strategy rules without adding external cloud network dependencies.

---

## 🛠️ System Prerequisites

Ensure your local machine environment meets the following baselines before installation:
* **Python 3.10+** installed on the host system.
* Active trading profile with **TradeLocker** (Live or Demo server tokens provided by your broker or prop firm).
* Modern desktop web browser engine (Chrome, Safari, Firefox, Edge).
* Devices must share the same local area network (LAN) router to support cross-device viewing.

---

## 📦 Step-by-Step Installation & Setup Blueprint

### 1. Synchronize the Repository
Open a terminal (Command Prompt/PowerShell on Windows, or Terminal on macOS) and run:
```bash
git clone https://github.com/yourusername/tradequest.git
cd tradequest
```

### 2. Isolate Dependencies via a Virtual Environment
Generate an isolated virtual environment to protect system libraries, then activate it:
```bash
# Generate the workspace
python -m venv venv

# Activate via Windows Command Prompt
call venv\Scripts\activate

# Alternative: Activate via Windows PowerShell
# .\venv\Scripts\Activate.ps1

# Alternative: Activate via macOS/Linux Terminal
# source venv/bin/activate
```

### 3. Install Required Engine Packages
Upgrade the environment execution tools and pull in the core asynchronous package frameworks:
```bash
python -m pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy httpx
```

### 4. Inject Local Environment Variable Configuration
Create a file named `.env` in the root folder structure of the project using a text editor (e.g., Notepad, VS Code) and populate your verified TradeLocker credentials:

```text
DATABASE_URL=sqlite:///./tradequest.db
TRADELOCKER_EMAIL=your_tradelocker_account_email@example.com
TRADELOCKER_PASSWORD=your_secret_login_password
TRADELOCKER_SERVER=YourOfficialBrokerServerString-Live
```
> ⚠️ **CRITICAL CONFIGURATION:** The `TRADELOCKER_SERVER` string must match the exact server designation label displayed on your broker's platform login card (e.g., `TradersWay-Live`, `FunderPro-Demo`).

---

## 🔥 Launching the Production Server

To run the application and allow other machines on your local network (like your Mac or phone) to view the client, you must explicitly bind the server execution host to `0.0.0.0`:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Upon a successful handshake, your terminal will display the active connection logs:
```text
🤖 Automated TradeLocker Synchronization Engine Active.
INFO:     Started server process [12844]
INFO:     Waiting for application startup.
INFO:     Uvicorn server running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## 🌐 Setting Up Cross-Device Local Access (PC Server ──> Mac Client)

Windows operating systems block all unrecognized incoming connections by default. Follow this 4-step sequence to let your Mac or iPhone view the app hosted on your Windows PC:

### 1. Set Windows Connection Profile to Private
By default, Windows places Wi-Fi cards on a "Public" stealth profile, hiding your PC from other household devices.
1. Click the Wi-Fi icon on your Windows Taskbar and click **Properties** underneath your connected network name.
2. Toggle the **Network Profile Type** selection from *Public* over to **Private**.

### 2. Open Port 8000 in Windows Firewall
Open an administrative port rule to clear a path for your incoming frontend web traffic:
1. Open the Start Menu, type **cmd**, right-click **Command Prompt**, and select **Run as Administrator**.
2. Paste this command and press Enter:
```cmd
netsh advfirewall firewall add rule name="TradeQuest Port 8000" dir=in action=allow protocol=TCP localport=8000
```

### 3. Allow ICMP (Ping) Requests through Windows Firewall
Ensure your devices can verify connection paths by letting Windows respond to network pings:
1. Inside that same administrative Command Prompt, execute:
```cmd
netsh advfirewall firewall add rule name="Allow ICMPv4-In" protocol=icmpv4:8,any dir=in action=allow
```

### 4. Locate Your Local IP and Connect
1. Discover your Windows PC's local address by typing `ipconfig` in the command prompt. Look for your **Wireless LAN adapter Wi-Fi** address (e.g., `192.168.1.15`).
2. Verify both your Mac and PC are on the exact same Wi-Fi router network.
3. Open Safari or Chrome on your Mac and type your PC's IP address directly into the URL bar:
```text
http://<YOUR_PC_IPV4_ADDRESS>:8000/play
```
*(Example: `http://192.168.1.15:8000/play`)*

---

## 🕹️ Interface Navigation

Once logged in, your session is remembered across tabs via browser `localStorage`. You can seamlessly hop between the two core views using the navigation links in the header:
* **The Game Arena (`/play`):** Monitor your level progression, accept dynamic stat-boosting side quests, log manual trade overrides, and view live boss health markers.
* **The Performance Station (`/dashboard`):** Analyze long-term growth trends, toggle lookback views (7d, 30d, 90d), and view calendar summaries with weekly roll-ups.

---

## 🛠️ Advanced Troubleshooting Matrix

| Symptom | Root Cause | Remedial Action |
| :--- | :--- | :--- |
| **Mac browser reports timeout error** | Windows Profile is still set to Public, or a local block rule is active. | Verify network properties are explicitly flagged as **Private**. Follow the steps below to check for stuck Python block rules. |
| **Ping requests fail from Mac terminal** | Windows Firewall is ignoring incoming ICMP echoes. | Execute the `netsh ... icmpv4` rule inside an administrative command prompt on your PC. |
| **Background sync prints `Retrieved 0 transactions`** | The targeted sub-account ledger is blank or has no historical closed trades. | Open your physical TradeLocker platform app. Execute and **completely close** a mini position (e.g., 0.01 lot EURUSD) to write data to the ledger tape, then refresh. |
| **Server errors out after code update** | Structural table column shifts conflict with old local database formats. | Stop your server (`Ctrl + C`), delete your local `tradequest.db` file from the directory, and restart Uvicorn to regenerate the tables fresh. |

### 🛠️ Clearing Stuck Python Block Rules
If you accidentally clicked "Cancel" on a Windows Firewall prompt in the past, an absolute **Block Rule** may be override-locking your server.
1. Press the Windows Key, type **Firewall**, and open *Windows Defender Firewall with Advanced Security*.
2. Select **Inbound Rules** in the left-hand panel.
3. Click the **Action** column to sort rules by status. Look for entries with a **Red Stop Sign icon** named `python.exe` or `uvicorn`.
4. Right-click and select **Delete** or **Disable Rule** on any blocked Python lines to restore normal connections.

---

## ⚖️ License & Modification Guidance
This application framework is structured for localized retail sandbox optimization. To customize trade rewards, level caps, scaling targets, or task rules to match your specific manual trading plan, modify the parameter equations directly within `execute_rpg_game_tick` inside `app/main.py`.
