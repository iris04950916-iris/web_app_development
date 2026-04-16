# 路由與頁面設計文件 (ROUTES) - 線上抽籤系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|---|---|---|---|---|
| **管理員登入** | GET | `/login` | `templates/auth/login.html` | 顯示登入表單 |
| **執行登入驗證** | POST | `/login` | — | 接收登入表單資料並驗證，成功則導向儀表板 |
| **登出** | GET | `/logout` | — | 清除登入狀態，重導向回登入頁 |
| **後台總覽** | GET | `/dashboard` | `templates/activity/dashboard.html` | 顯示所有活動列表（需登入） |
| **建立活動頁面** | GET | `/activity/create` | `templates/activity/create.html` | 顯示建立活動表單 |
| **儲存新活動** | POST | `/activity/create` | — | 接收表單並建立活動資料 |
| **活動詳情與名單** | GET | `/activity/<int:id>` | `templates/activity/detail.html` | 顯示單一活動設定及該活動參加者清單 |
| **新增/匯入參加者** | POST | `/activity/<int:id>/participants` | — | 新增單一或批次送出參加者，儲存後重導向 |
| **刪除參加者** | POST | `/activity/<int:activity_id>/participants/<int:participant_id>/delete` | — | 刪除單一參加者，防呆設計 |
| **執行抽籤** | POST | `/activity/<int:id>/draw` | — | 執行抽獎並產出得獎名單寫庫 |
| **查看抽籤結果** | GET | `/activity/<int:id>/results` | `templates/activity/results.html` | 公開的開獎結果畫面，展示給所有人看 |

---

## 2. 每個路由的詳細說明

### 帳號驗證與登入 (`app/routes/auth.py`)

- **`/login` (GET/POST)**
  - **輸入**: POST 會收到 `username` 與 `password` 表單欄位。
  - **處理邏輯**: 呼叫 `Admin.get_by_username()` 比對邏輯。比對成功後，將標記寫入 Flask `session`。
  - **輸出**: GET 渲染 `auth/login.html`；POST 成功重導向至 `/dashboard`，失敗退回並顯示錯誤。
- **`/logout` (GET)**
  - **處理邏輯**: 執行 `session.clear()` 確保安全。
  - **輸出**: 重導向至 `/login`。

### 活動與抽籤管理 (`app/routes/activity.py`)

- **`/dashboard` (GET)**
  - **處理邏輯**: 確認是否已登入。若已登入，使用 `Activity.get_all()` 抓取資料庫活動清單。
  - **輸出**: 渲染 `activity/dashboard.html`。
- **`/activity/create` (GET/POST)**
  - **輸入**: POST 會收到 `name` 與 `description`。
  - **處理邏輯**: 呼叫 `Activity.create()` 建立基本資料。
  - **輸出**: GET 渲染表單；POST 成功則重導向 `/dashboard` 或該活動的 `/activity/<id>`。
- **`/activity/<int:id>` (GET)**
  - **輸入**: URL 參數 `id` 取出特定活動。
  - **處理邏輯**: 呼叫 `Activity.get_by_id()` 和 `Participant.get_by_activity_id()` 組合資料。若活動不存在回傳 404。
  - **輸出**: 渲染 `activity/detail.html`。
- **`/activity/<int:id>/participants` (POST)**
  - **輸入**: 表單傳入 `participant_names`。
  - **處理邏輯**: 切割文字或 CSV 內容，迴圈透過 `Participant.create()` 寫入資料庫。
  - **輸出**: 處理完畢後重導向至 `/activity/<id>`。
- **`/activity/<int:Activity_id>/participants/<int:participant_id>/delete` (POST)**
  - **處理邏輯**: 呼叫 `Participant.delete()`。
  - **輸出**: 重導向至 `/activity/<id>`。
- **`/activity/<int:id>/draw` (POST)**
  - **輸入**: 表單可能帶有如「抽出人數」或「獎項名稱 (`prize_name`)」。
  - **處理邏輯**: 呼叫 `Participant.get_eligible_participants()`，引入 Python `random.sample()` 抽出結果，最後呼叫 `DrawResult.create()`。
  - **輸出**: 重導向顯示特定的動畫頁或直接跳去 `/activity/<id>/results`。
- **`/activity/<int:id>/results` (GET)**
  - **處理邏輯**: 調用 `DrawResult.get_by_activity_id()` 回傳此活動的得獎者關聯清單。不需要求使用者登入（公開展示用途）。
  - **輸出**: 渲染 `activity/results.html`。

---

## 3. Jinja2 模板清單

所有的模板將繼承自一個大版型 `base.html`：

- **`templates/base.html`**
  - 全站導覽列與共同 CSS / JS 引入骨架。

**身分驗證相關：**
- **`templates/auth/login.html`**
  - 管理員登入表單元件。

**活動管理相關：**
- **`templates/activity/dashboard.html`**
  - 後台總覽介面，卡片化或條列式顯示所有的活動。
- **`templates/activity/create.html`**
  - 建立一場抽籤活動的單純表單輸入頁。
- **`templates/activity/detail.html`**
  - 活動後台管理頁：左邊可能有匯入表單、右邊有參加者列表與刪除按鈕；下方有個大大的「按下抽籤」區域。
- **`templates/activity/results.html`**
  - 單場活動中獎榜單，可以給所有參與者查證是否自己中獎的唯獨顯示頁面。
