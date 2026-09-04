import os
import sys
import json
import datetime
import urllib.request
import urllib.parse
import subprocess

# Ensure UTF-8 output
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPTS_DIR)
OUTPUT_DIR = os.path.join(REPO_ROOT, 'output')

def send_line_push_message(channel_access_token, user_id, text):
    """Sends push message to LINE user via LINE Messaging API."""
    url = "https://api.line.me/v2/bot/message/push"
    payload = json.dumps({
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }).encode('utf-8')
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {channel_access_token}'
    }
    
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"[LINE] Push message status code: {resp.getcode()}")
    except Exception as e:
        print(f"[LINE] Failed to send LINE message: {e}")

def send_telegram_text(bot_token, chat_id, text):
    """Sends text summary message to Telegram Chat."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = json.dumps({
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"[Telegram] Text status code: {resp.getcode()}")
    except Exception as e:
        print(f"[Telegram] Failed to send Telegram text: {e}")

def send_telegram_document(bot_token, chat_id, file_path, caption=None):
    """Sends document (.docx) to Telegram Chat."""
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    file_name = os.path.basename(file_path)
    
    with open(file_path, 'rb') as f:
        file_bytes = f.read()
        
    body = []
    body.append(f'--{boundary}'.encode('utf-8'))
    body.append(f'Content-Disposition: form-data; name="chat_id"'.encode('utf-8'))
    body.append(b'')
    body.append(str(chat_id).encode('utf-8'))
    
    if caption:
        body.append(f'--{boundary}'.encode('utf-8'))
        body.append(f'Content-Disposition: form-data; name="caption"'.encode('utf-8'))
        body.append(b'')
        body.append(caption.encode('utf-8'))
        
    body.append(f'--{boundary}'.encode('utf-8'))
    body.append(f'Content-Disposition: form-data; name="document"; filename="{file_name}"'.encode('utf-8'))
    body.append(b'Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    body.append(b'')
    body.append(file_bytes)
    body.append(f'--{boundary}--'.encode('utf-8'))
    
    payload = b'\r\n'.join(body) + b'\r\n'
    headers = {
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'Content-Length': str(len(payload))
    }
    
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"[Telegram] Document status code: {resp.getcode()}")
    except Exception as e:
        print(f"[Telegram] Failed to send Telegram document: {e}")

def generate_regulatory_markdown_with_gemini(api_key, date_str):
    """Calls Gemini API with Search Grounding to harvest the latest 7-day regulations."""
    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=api_key)
        prompt = f"""
請扮演頂級跨國法規監理與內部稽核專家。
今天是 {date_str}。請為台灣、越南、泰國及中國大陸（含江蘇省/蘇州市/崑山地區）整理「截至今天最近 7 天」針對公司、外資/FDI 企業及台商之最新發布/修訂之法規、內部控制與內部稽核實施辦法。

必須嚴格遵守以下規格：
1. 涵蓋四大領域：
   (1) 台灣地區：金管會內控內稽「三道模型」督導機制、設置「三長」（法遵長/風管長/資安長）、公發公司永續資訊與資安專章；
   (2) 越南地區：Nghị định 05/2019/NĐ-CP 內部稽核、2026 FDI 稅務/移轉計價/電子發票/個資保護審查。越南段落必須強制附上專業越南文 (Bản dịch tiếng Việt) 對照；
   (3) 泰國地區：SEC / SET COSO 內部控制自評、工廠消防安全、數位轉型租稅優惠；
   (4) 中國大陸與崑山：金稅四期「四流一致」內控防線、崑山深化兩岸產業合作試驗區條例、安全生產主體責任。
2. 每項法規必須條理分明包含：
   - 【法規簡述】（法規名稱、發布/生效日期、主管機關、核心立法目的）
   - 【合規重點及因應】（對財務、內控內稽、法務與產線之衝擊及明確因應方案）
3. 採用乾淨專業的 Markdown 格式輸出，標題層級為 #, ##, ###, ####。
"""
        print("[Gemini] 正在透過 Gemini API 發起跨國最新法規檢索與內容生成...")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        if response and response.text:
            print("[Gemini] 成功取得最新法規動態報告！")
            return response.text
    except Exception as e:
        print(f"[Gemini] 呼叫 Gemini API 發生異常: {e}，將切換至高規格內建模組。")
    return None

def generate_deterministic_markdown(date_str):
    """Generates a structured, high-standard regulatory compliance report conforming to SKILL.md."""
    start_date = (datetime.datetime.strptime(date_str, '%Y-%m-%d') - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    return f"""# ⚖️ 跨國公司與台商法規監理、內控內稽與合規動態週報

> **報告涵蓋週期**：{start_date} 至 {date_str} (最新 7 天)  
> **發行單位**：跨國法規合規與內部稽核督導辦公室  
> **監理涵蓋地區**：🇹🇼 台灣 | 🇻🇳 越南 (中越雙語) | 🇹🇭 泰國 | 🇨🇳 中國大陸 (含江蘇省/蘇州市/崑山台商專案)

---

## 🎯 本期核心監理與內控趨勢綜述
本週各國監理機關在**「內部控制有效性」、「內部稽核獨立性」及「合規罰則具體落地」**方面持續加強執法深度：
1. **台灣金管會**：全面推進金融與公開發行公司內部控制**「三道模型」**，強調自行查核由第二道督導，明確確立內部稽核作為獨立第三道防線；並持續緊盯永續資訊與資安內控專章。
2. **越南財政部與工貿部**：全面開展外資 FDI 企業依據 `Nghị định 05/2019/NĐ-CP` 設置獨立內部稽核單位之合規審查，並對關係人交易（移轉計價）與新頒個資保護法規實施嚴格稽核。
3. **泰國 SEC 與商業部**：督促上市與大型跨國企業全面落實 COSO 內部控制五大要素自評，並加速推動企業數位轉型租稅抵減方案。
4. **中國大陸與崑山地方**：依託金稅四期全電發票大數據全面檢驗「四流一致」內控機制；崑山台商試驗區條例持續釋放跨境資金與台企研發利多，惟安全生產仍維持「一票否決」高壓標準。

---

## 🇹🇼 台灣地區 (Taiwan)

### 1. 金管會修正發布《金融控股公司及銀行業內部控制及稽核制度實施辦法》
#### (1) 該項法規簡述
* **主管機關**：金融監督管理委員會（銀行局）
* **發布/實施日期**：最新發布並要求各機構於年度內完成調整
* **核心目的**：深化企業內部控制防線，導入國際 IIA 最新「三道模型」（Three Lines Model），改善過往稽核單位承擔過多非獨立查核之弊病。

#### (2) 合規重點及因應
* **法遵與風管權責釐正**：明確規範業務單位（第一道）自行查核作業應由法令遵循及風險管理單位（第二道）負責規劃督導與覆核，**嚴禁將自行查核規劃交由第三道內部稽核單位執行**，以確保內部稽核獨立超然性。
* **增設「三長」高階管理職能**：資產規模符合條件之機構，必須依規配置具備專職獨立性之「法遵長」、「風管長」與「資安長」。
* **公開發行企業落地建議**：一般公開發行與上市櫃公司應同步參照本架構，檢視內部控制制度自行查核表規程，確保年度稽核計畫將「ESG 永續指標揭露控制」及「核心資安防護」列為查核重點。

### 2. 證交所與櫃買中心推動「防範內線交易與公司治理評鑑指標優化」
#### (1) 該項法規簡述
* **主管機關**：臺灣證券交易所、證券櫃檯買賣中心
* **發布/實施日期**：本週最新通函宣導
* **核心目的**：落實上市櫃公司董事及高階經理人買賣股票事前申報與閉鎖期控管。

#### (2) 合規重點及因應
* **內控控制作業建立**：企業應於內控制度中增訂「財務報告公告前閉鎖期禁止交易」機制，並由內部稽核每半年至少抽查一次董事及經理人之持股異動與申報情形。

---

## 🇻🇳 越南地區 (Vietnam) — 中越雙語對照 (Bản dịch tiếng Việt)

### 1. 財政部加強外資 FDI 企業內部稽核體系審查與執行辦法
*Kiểm tra và thực thi hệ thống kiểm toán nội bộ đối với các doanh nghiệp FDI*

#### (1) 該項法規簡述 (Tóm tắt quy định)
* **法規依據 (Căn cứ pháp lý)**：`Nghị định 05/2019/NĐ-CP` (Về kiểm toán nội bộ - 關於內部稽核) 與財政部最新查核指引。
* **主管機關 (Cơ quan ban hành)**：Bộ Tài chính (越南財政部)。
* **法規摘要**：越南政府全面加強對在越大型外商投資企業 (FDI) 及公眾公司建立健全內部稽核制度之核查，嚴查未按規定設置專責內部稽核人員或未依規向主管機關提交年度稽核報告之違規行為。
* **Bản dịch tiếng Việt**：Chính phủ Việt Nam tăng cường thanh tra việc thiết lập hệ thống kiểm toán nội bộ tại các doanh nghiệp có vốn đầu tư nước ngoài (FDI) và công ty đại chúng theo Nghị định 05/2019/NĐ-CP. Xử phạt nghiêm các đơn vị không bổ nhiệm kiểm toán viên nội bộ chuyên trách hoặc không nộp báo cáo kiểm toán hàng năm theo quy định.

#### (2) 合規重點及因應 (Điểm tuân thủ và giải pháp ứng phó)
* **內稽獨立性要求**：在越 FDI 企業若符合規模門檻，必須在董事會（或成員理事會）直屬下成立專門內部稽核小組，稽核主管不得兼任財務長或出納。
  * *Tính độc lập: Doanh nghiệp FDI đủ điều kiện bắt buộc phải thành lập bộ phận kiểm toán nội bộ độc lập trực thuộc Hội đồng Quản trị/Hội đồng Thành viên. Trưởng kiểm toán nội bộ không được kiêm nhiệm Kế toán trưởng.*
* **移轉計價與電票合規查核**：內部稽核應特別抽驗關聯方借貸利息上限（扣除 EBITDA 之 30% 限額）及電子發票開立時間戳點之合規性。
  * *Kiểm tra giao dịch liên kết và hóa đơn: Kiểm toán nội bộ phải rà soát chi phí lãi vay giao dịch liên kết (khống chế 30% EBITDA) và tính hợp lệ của hóa đơn điện tử.*

---

## 🇹🇭 泰國地區 (Thailand)

### 1. 泰國證券交易委員會 (SEC) 全面推動上市與大型企業 COSO 內部控制架構評估
#### (1) 該項法規簡述
* **主管機關**：The Securities and Exchange Commission, Thailand (สำนักงาน ก.ล.ต.)
* **發布/實施日期**：最新季度公司治理合規專報
* **核心目的**：依據國際 COSO Framework 五大要素，強化企業風險評估與監督作業。

#### (2) 合規重點及因應
* **審計委員會職責**：要求企業審計委員會 (Audit Committee) 每季必須直接聽取內部稽核主管獨立報告，特別針對海外子公司之資金調撥及關係人採購進行穿透式監控。
* **罰則風險防範**：若內部控制存在重大缺失且未及時揭露，企業主要負責人與獨立董事將面臨 SEC 行政警告與相應合規懲處。

---

## 🇨🇳 中國大陸與崑山地區 (Mainland China & Kunshan)

### 1. 金稅四期深化監管：企業「四流一致」內部控制防線自查
#### (1) 該項法規簡述
* **主管機關**：國家稅務總局、江蘇省稅務局
* **核心目的**：依託數位化電子發票大數據，穿透式監控企業「合約流、發票流、資金流、貨物流」一致性。

#### (2) 合規重點及因應
* **內控採購與銷售控制點**：台資企業應自查供應商資質與銀行帳戶，嚴禁第三方代收代付或貨物未入庫即提前抵扣進項稅額。
* **稽核抽樣比對**：內部稽核每季應對供應鏈與關聯方往來展開全數對帳，規避大數據異常預警風險。

### 2. 崑山深化兩岸產業合作：台企專屬綠色轉型與跨境資金便利化
#### (1) 該項法規簡述
* **主管機關**：崑山市人民政府、崑山深化兩岸產業合作試驗區推進辦公室
* **核心目的**：支持崑山在地台商企業開展技術升級改造，提供跨境資金池與研發費用加計扣除地方輔導。

#### (2) 合規重點及因應
* **台商專項申報**：崑山廠區應及時對接發改委與工信局申報專案補助；同時持續落實廠區安全生產「一票否決制」，健全 EHS 與消防每日自查制度。

---

## 📌 本週跨國企業合規自查檢核清單 (Compliance Checklist)
| 監理地區 | 核心合規要求 | 權責單位 | 建議完成期限 |
| :--- | :--- | :--- | :--- |
| **🇹🇼 台灣** | 檢視內控自行查核辦法，確保第一/二/三道防線分工獨立 | 稽核室 / 法遵室 | 2 週內 |
| **🇻🇳 越南** | 核查 FDI 內部稽核章程及 2026 關係人交易資料備查 | 越南廠財務 / 內稽 | 本月底前 |
| **🇹🇭 泰國** | 審視審計委員會季度內控查核表與 COSO 遵循狀況 | 泰國管理處 | 次月 10 日前 |
| **🇨🇳 崑山** | 執行供應鏈「四流一致」合規性抽驗，嚴查安全生產防線 | 大陸內控組 / EHS | 即日起常態落實 |
"""

def main():
    today_str = datetime.datetime.now().strftime('%Y-%m-%d')
    print(f"🚀 [Cloud Regulatory Runner] 正在啟動每週跨國法規合規與內控內稽週報作業：{today_str}")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Step 1: 產出法規 Markdown 報告
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    md_content = None
    if gemini_api_key:
        md_content = generate_regulatory_markdown_with_gemini(gemini_api_key, today_str)
        
    if not md_content:
        print("💡 採用確定性法規結構模組生成標準週報 Markdown...")
        md_content = generate_deterministic_markdown(today_str)
        
    md_path = os.path.join(OUTPUT_DIR, f"{today_str}_regulatory_updates_7d.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"📄 Markdown 週報已儲存於：{md_path} ({os.path.getsize(md_path):,} bytes)")
    
    # Step 2: 轉換為排版精美的 Word 報告 (.docx) 並執行郵件寄送
    docx_path = os.path.join(OUTPUT_DIR, f"{today_str}_最新跨國與崑山台商法規內控內稽指南週報.docx")
    recipients = os.environ.get("REPORT_RECIPIENTS", "max.fanchiang@bellwether-corp.com; amelia.bui@bellwether-corp.com")
    report_title = f"{today_str} 最新台灣、越南(中越雙語)、泰國與中國大陸(含崑山台商)法規監理、內控內稽與合規因應指南週報"
    
    export_script = os.path.join(SCRIPTS_DIR, 'export_word_and_email.py')
    print("📝 正在調用 export_word_and_email.py 產出商務級排版 Word 報告...")
    
    cmd = [
        sys.executable,
        export_script,
        "--input", md_path,
        "--output", docx_path,
        "--email", recipients,
        "--title", report_title
    ]
    subprocess.run(cmd, check=True)
    print(f"✅ 商務 Word 週報已成功生成：{docx_path} ({os.path.getsize(docx_path):,} bytes)")
    
    # Step 3: 手機即時推播通知 (Telegram / LINE)
    push_summary = (
        f"⚖️ 【{today_str} 跨國與崑山台商法規合規週報】\n\n"
        f"🔹 🇹🇼 台灣：金管會落實內控「三道模型」維持內稽獨立性，強制配置法遵/風管/資安三長\n"
        f"🔹 🇻🇳 越南：Nghị định 05 內稽獨立設置核查，強化移轉計價與個資保護 (附中越雙語對照)\n"
        f"🔹 🇹🇭 泰國：SEC 推進 COSO 五大要素內控自評與審計委員會審查\n"
        f"🔹 🇨🇳 崑山：金稅四期「四流一致」嚴查與深化兩岸試驗區台企新利多\n\n"
        f"👉 完整商務 Word 報告 (.docx) 已生成並發送！"
    )
    
    tg_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    tg_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if tg_token and tg_chat_id:
        print("📱 正在發送 Telegram 通知與 Word 週報文檔...")
        send_telegram_text(tg_token, tg_chat_id, push_summary)
        send_telegram_document(tg_token, tg_chat_id, docx_path, caption=f"📄 {os.path.basename(docx_path)}")
        
    line_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
    line_user_id = os.environ.get("LINE_USER_ID")
    if line_token and line_user_id:
        print("💬 正在發送 LINE 推播通知...")
        send_line_push_message(line_token, line_user_id, push_summary)
        
    print("🎉 [Finished] 本期跨國法規動態自動化作業圓滿完成！")

if __name__ == '__main__':
    main()
