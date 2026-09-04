---
name: regulatory-compliance-reporter
description: 自動搜尋與彙整最近 7 天關於台灣、越南 (Vietnam)、泰國 (Thailand) 及中國大陸 (含江蘇省/蘇州市/崑山地區) 對公司、外資/FDI 公司及台商企業 (Taiwan-invested enterprises) 所受規範之法規新增與修正項目。每次執行時強制重新發起網路即時搜尋與官方來源精準核實，嚴禁套用舊快照或先前對話資訊。實施當地語言優先原則（越南語 Tiếng Việt、泰語 ภาษาไทย、簡體中文/地方政策、繁體中文），規範範圍涵蓋內部稽核 (Internal Audit)、內部控制制度 (Internal Control System)、財務會計、公司治理與 ESG、勞工管理、消防安全 (PCCC/Fire Safety)、工作安全衛生與環境保護 (EHS)、稅務與轉讓定價 (Transfer Pricing) 及台商專屬政策。針對每項法規強制包含：(1)該項法規簡述、(2)合規重點及因應，且越南資訊段落必須強制附上專業越南文 (Tiếng Việt) 雙語翻譯對照。整理完畢後自動調用 Python 腳本 (scripts/export_word_and_email.py) 導出商務級精美排版 Word 報告 (.docx)，並透過 Outlook 自動寄送至 max.fanchiang@bellwether-corp.com 及 amelia.bui@bellwether-corp.com。
---

# ⚖️ 跨國公司與台商法規監理、內控內稽與合規動態簡報官 (Global & Taiwan-Invested Enterprise Regulatory, Internal Audit & Control Compliance Reporter)

## 🎯 核心目標與資訊真偽極致要求
本 Skill 旨在協助使用者定期精準掌握**台灣、越南、泰國及中國大陸（含江蘇省/蘇州市/崑山地區）**當地針對本地企業、外資/FDI 公司及台商企業最新發布或修正之法令規範、內部控制制度與內部稽核實施辦法。

> [!CAUTION]
> **【零快照與即時精準核實鐵律 (Strict Real-time Search & Verification Protocol)】**
> 1. **每次執行必須即時重新搜尋**：每次呼叫或觸發本 Skill 時，**必須強制對所有國家/地區發起全新的網路即時搜尋**，精確抓取截至執行當下（近 7 天）最新發布之官方公告。
> 2. **嚴禁直接套用舊數據**：**絕對禁止直接複製、重用或套用先前執行過或歷史對話中留存的舊資訊**。
> 3. **官方來源交叉精準核實**：所有搜集到的法規名稱、發布字號、生效日期、條文門檻與違規罰則，必須對照官方發布來源進行二次核實，杜絕 AI 幻覺與不實訊息。

---

## 📌 法規整理四大強制要求：
1. **(1) 該項法規簡述**：法規/地方條例名稱、編號、發布/生效日期、主管機關及核心立法目的背景。
2. **(2) 合規重點及因應**：法規對企業、外資公司及台商（財務、內部稽核、內控、HR、廠務 EHS/消防、ESG、法務）的具體衝擊、潛在違規處罰風險，以及明確的企業落地因應步驟。
3. **🇻🇳 越南段落強制中越雙語對照 (Bilingual Requirement)**：
   * 越南資訊的所有法規段落，必須在中文說明下方附上相對應之精準越南文翻譯 (Bản dịch tiếng Việt)。
4. **🇨🇳 中國大陸與崑山段落專屬台商條款**：
   * 包含國務院/稅務總局金稅四期、江蘇省/蘇州市/崑山市（如《崑山深化兩岸產業合作試驗區條例》、安全生產、環保綠色轉型）之地方規範與台企政策。

---

## 📋 涵蓋規範領域：
1. **內部稽核與內部控制制度 (Internal Audit & Internal Control System)**：
   * **台灣**：《公開發行公司建立內部控制制度處理準則》、《金融控股公司及銀行業/保險業內部控制及稽核制度實施辦法》最新修訂（如「三道模型」、設置法遵長/風管長/資安長「三長」、資安與永續資訊內控專章、內部稽核人員資格與報告格式）。
   * **越南**：`Nghị định 05/2019/NĐ-CP` (Kiểm toán nội bộ - 內部稽核) 及 2026 FDI 內控審查、財務與個資合規稽核。
   * **泰國**：SET / SEC (สำนักงาน ก.ล.ต.) 內部控制 (COSO Framework) 與內部稽核 (Internal Audit System) 自評與報告規範。
   * **中國大陸與崑山**：《企业内部控制基本规范》、金稅四期下「四流一致」內控防線、安全生產與財務內控自查。
2. **財務會計 (Financial & Accounting)**：最新會計準則、電子發票規範、微型與外資企業會計制度。
3. **公司治理與 ESG (Corporate Governance & ESG)**：ESG 評鑑轉型、永續報告書申報、IFRS S1/S2 接軌、供應鏈人權與強迫勞動防制。
4. **勞工相關管理 (Labor Management)**：勞工退休金自提與連帶責任、電子勞動合同、勞保違規罰則與個資保護。
5. **消防安全 (Fire Safety / PCCC)**：廠房與營業場所消防安檢、PCCC 行政處罰與災害防禦標準。
6. **工作安全衛生與環境保護 (EHS & Environmental Protection)**：工作場所危險標誌、安全生產主體責任、綠色低碳轉型與排放標準。
7. **稅務與轉讓定價 (Taxation & Transfer Pricing)**：金稅四期「四流一致」、企業所得稅 (TNDN/CIT)、轉讓定價 (Transfer Pricing) 關係人交易、數位轉型租稅優惠。
8. **台商專屬政策與地方條例 (Taiwan-Invested Enterprise Regulations)**：崑山兩岸產業合作試驗區條例、台胞台企扶持措施、跨境資金調配。

---

## ⚙️ 自動化工作流程 (每次執行重新發起全套檢索)

當使用者輸入「法規動態」、「最新法規整理」、「內控內稽規範」、「跨國合規週報」、「越南泰國崑山法規」、「更新法規週報並寄信」時，請嚴格執行以下步驟：

### 步驟 1：發起當地語言與地方規範優先之「即時全新」跨國法令檢索 (近 7 天 ~ 當下)

#### 1. 🇹🇼 台灣地區 (Taiwan) — *即時檢索金管會/證交所/櫃買中心/勞動部*
* **內控內稽**：《金融控股公司及銀行業內部控制及稽核制度實施辦法》（三道模型、設置三長、自行查核與合確報告）、《保險業內部控制及稽核制度實施辦法》（資安長範圍）、《公開發行公司建立內部控制制度處理準則》（永續與資安內控專章）。
* **資本市場/勞動/ESG**：注意處置作業要點、勞退細則連帶責任、ESG 評鑑轉型、IFRS S1/S2。

#### 2. 🇻🇳 越南地區 (Vietnam) — *即時使用越南語 (Tiếng Việt) 檢索官方資料庫*
* **內控內稽 (Kiểm toán nội bộ & Kiểm soát nội bộ)**：`Nghị định 05/2019/NĐ-CP` 內部稽核架構及 FDI 企業財務/稅務/個資內部審查要點。
* **稅務/勞動/消防**：`Thông tư 20/2026/TT-BTC`（TNDN 合理費用）、`Nghị định 255/2026`（移轉計價）、`Nghị định 283/2026`（勞動處罰/個資最高罰 1.4 億越盾）、`Nghị định 69/2026`（PCCC 消防處罰）。

#### 3. 🇹🇭 泰國地區 (Thailand) — *即時使用泰語 (ภาษาไทย) 檢索ราชกิจจานุเบกษา與 SEC*
* **內控內稽 (Internal Control & Audit)**：SEC / SET COSO 框架內部控制自評與內部稽核體系審查。
* **稅務/勞工/消防**：`พระราชกฤษฎีกา (ฉบับที่ 802) พ.ศ. 2569`（Digital Transformation 租稅優惠）、`ระเบียบกระทรวงแรงงาน 2569`（欠薪資產查封）、`ประกาศกระทรวงอุตสาหกรรม`（工廠防火）。

#### 4. 🇨🇳 中國大陸與崑山地區 (Mainland China & Kunshan) — *即時檢索國家與江蘇/崑山地方政府*
* **內控內稽 (企业内部控制)**：《企业内部控制基本规范》、金稅四期大數據下「四流一致」內部控制防線、安全生產主體責任內控自查。
* **台商專屬與稅務/安衛**：修訂版《崑山深化兩岸產業合作試驗區條例》、江蘇省「稅路通·蘇服達」跨境稅務服務、崑山安全生產一票否決制。

*所有地區每項法規均須經過即時網頁搜尋與核實，寫出 (1)法規簡述 與 (2)合規重點及因應。*

---

### 步驟 2：生成結構化 Markdown 暫存檔
將當下即時發起搜尋並核實無誤的最新內容整理成符合 Alert/Callout 與四國/地方對照結構之 Markdown 內容，暫存於：
```
<appDataDir>\brain\<conversation-id>\regulatory_updates_7d.md
```

---

### 步驟 3：調用 Python 腳本匯出 Word 檔並經由 Outlook 自動寄送
執行以下 Python 指令，轉換為精美 Word 報告 (.docx) 並優先經由 Outlook 寄出給多位收件人：

```powershell
python "C:\Users\max.fanchiang\.gemini\config\skills\regulatory-compliance-reporter\scripts\export_word_and_email.py" --input "<appDataDir>\brain\<conversation-id>\regulatory_updates_7d.md" --output "C:\Users\max.fanchiang\Desktop\最新跨國與崑山台商法規內控內稽指南週報.docx" --email "max.fanchiang@bellwether-corp.com; amelia.bui@bellwether-corp.com"
```

---

## 📧 預設雙收件人 (Default Dual Recipients)
* **預設信箱**：`max.fanchiang@bellwether-corp.com` 及 `amelia.bui@bellwether-corp.com`
* **郵件附件**：產出的精美跨國與崑山台商法規（含內控內稽）Word 報告 `.docx`
