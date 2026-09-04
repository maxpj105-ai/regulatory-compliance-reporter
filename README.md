# ⚖️ Weekly Regulatory Compliance Reporter (跨國與台商法規監理、內控內稽週報雲端自動化)

本專案將 Antigravity **`regulatory-compliance-reporter`** 技能完整轉化為 **GitHub Actions 雲端定時自動化系統**。  
**電腦免開機**，每週五定時自動搜集台灣、越南（中越雙語對照）、泰國及中國大陸（含崑山台商）最新 7 天法規動態、內控內稽三大防線，並自動生成**商務排版 Word 報告 (.docx)** 與郵件發送！

---

## ⏰ 自動排程設定 (Schedule)

* **執行時間**：**每週五 09:30 AM (台灣時間 UTC+8)**
* **Cron 表達式**：`30 1 * * 5` (對應 UTC 時間每週五 01:30 AM)
* **手動隨時觸發**：支援 `workflow_dispatch`，隨時可在 GitHub 網頁或手機 GitHub App 點擊「Run workflow」立即產出最新週報。

---

## 📁 專案架構

```
regulatory-compliance-reporter/
├── .github/
│   └── workflows/
│       └── weekly_compliance_report.yml    # 每週五 09:30 自動化執行工作流程
├── scripts/
│   ├── cloud_regulatory_runner.py          # 雲端/本機通用自動化執行主程式
│   ├── export_word_and_email.py            # 商務 Word 排版產生與郵件寄送引擎
│   └── run_weekly_report.bat               # 本機一鍵雙擊執行批次檔
├── output/                                 # 產出之 Word (.docx) 與 Markdown 週報
├── SKILL.md                                # 原始完整法規簡報官技能規格
├── requirements.txt                        # Python 依賴清單
├── .gitignore
└── README.md                               # 本說明文件
```

---

## 🚀 3 步驟快速推送到 GitHub (首次設定)

### 步驟 1：在 GitHub 上建立 Repository
1. 登入您的 GitHub 帳號 ([github.com](https://github.com/))。
2. 點擊右上角 **+** ➔ **New repository**。
3. 設定：
   - **Repository name**：`regulatory-compliance-reporter`
   - **Visibility**：可依需求選擇 `Public` 或 `Private`。
   - **不要**勾選 Initialize this repository with a README（本地已備妥）。
4. 點擊 **Create repository**。

---

### 步驟 2：將本地專案 Push 至 GitHub
在終端機（PowerShell 或 Git Bash）執行以下指令：

```bash
cd C:\Users\max.fanchiang\Documents\GitHub\regulatory-compliance-reporter
git init
git add .
git commit -m "feat: Initial commit for regulatory compliance reporter weekly automation"
git branch -M main
git remote add origin https://github.com/maxpj105-ai/regulatory-compliance-reporter.git
git push -u origin main
```

---

### 步驟 3：設定 GitHub Repository Secrets (選填)
進入 GitHub 專案頁面 ➔ **Settings** ➔ **Secrets and variables** ➔ **Actions** ➔ 點擊 **New repository secret**：

| Secret 名稱 | 說明與填寫建議 |
| :--- | :--- |
| `GEMINI_API_KEY` | *(選填)* Google Gemini API Key，用於調用最新 AI 檢索與法規分析（若未填寫，系統將自動啟動內建標準確定性法規模組）。 |
| `REPORT_RECIPIENTS` | *(選填)* 報告收件人清單（預設：`max.fanchiang@bellwether-corp.com; amelia.bui@bellwether-corp.com`）。 |
| `SMTP_SERVER` | *(選填)* 雲端發信用 SMTP 伺服器（例如：`smtp.gmail.com` 或企業內部 SMTP）。 |
| `SMTP_PORT` | *(選填)* SMTP 埠號（例如：`587`）。 |
| `SMTP_USER` | *(選填)* 發件郵箱帳號。 |
| `SMTP_PASSWORD` | *(選填)* 發件郵箱密碼或應用程式專用密碼。 |
| `LINE_CHANNEL_ACCESS_TOKEN` | *(選填)* 若需手機 LINE 推播，填入 LINE Channel Access Token。 |
| `LINE_USER_ID` | *(選填)* LINE 接收者 User ID。 |
| `TELEGRAM_BOT_TOKEN` | *(選填)* Telegram 機器人 Token。 |
| `TELEGRAM_CHAT_ID` | *(選填)* Telegram 接收頻道/群組 ID。 |

> [!TIP]
> 即使不設定任何 Secret，GitHub Actions 每週五仍會準時在雲端自動執行並產出最新的 Word 週報 (.docx) 及 Markdown 檔，並自動上傳至 **GitHub Artifacts**，供您隨時在 GitHub 網頁或手機 App 免費下載！

---

## 📱 如何在手機或網頁手動觸發與下載報告？

1. **手動觸發**：
   - 進入 Repository 的 **Actions** 分頁。
   - 點選左側 **Weekly Compliance Report Automation**。
   - 點擊右側 **Run workflow** ➔ 點選綠色 **Run workflow** 按鈕。
2. **下載生成的 Word 週報**：
   - 點擊剛跑完的工作流程（打綠色勾勾）。
   - 滑動至最下方的 **Artifacts** 區塊。
   - 點擊 **`weekly-compliance-report-X`**，即可下載包含精美 `.docx` 格式與 `.md` 的壓縮包！

---

## 💻 本機手動執行 (Windows)

在本地電腦上，只需雙擊執行：
```
scripts\run_weekly_report.bat
```
程式將自動整合最新情報、渲染 Word 報告，並優先透過您本機的 **Outlook** 自動寄送給指定的團隊收件人。
