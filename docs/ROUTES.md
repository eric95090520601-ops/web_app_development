# 路由設計文件 (API Design) - 食譜收藏檢索系統

本文件規劃了所有的 Flask 路由，並定義各路由對應的 HTTP 方法、輸入、處理邏輯與渲染的 Jinja2 模板。

## 1. 路由總覽表格

| 功能模組 | 功能名稱 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **首頁** | 網站首頁 | GET | `/` | `templates/index.html` | 顯示搜尋列、熱門/最新食譜列表 |
| **會員** | 註冊頁面 | GET | `/auth/register` | `templates/auth/register.html` | 顯示註冊表單 |
| **會員** | 註冊處理 | POST | `/auth/register` | — | 接收表單，寫入資料庫，重導向至登入 |
| **會員** | 登入頁面 | GET | `/auth/login` | `templates/auth/login.html` | 顯示登入表單 |
| **會員** | 登入處理 | POST | `/auth/login` | — | 驗證帳密，設定 session，重導向首頁 |
| **會員** | 登出處理 | GET | `/auth/logout` | — | 清除 session，重導向首頁 |
| **會員** | 個人頁面 | GET | `/user/profile` | `templates/user/profile.html` | 顯示自己上傳的食譜與收藏 |
| **食譜** | 搜尋結果 | GET | `/recipes/search` | `templates/recipe/list.html` | 依據 `q` (關鍵字) 或 `ingredient` 查詢 |
| **食譜** | 食譜詳細 | GET | `/recipes/<id>` | `templates/recipe/detail.html` | 顯示特定食譜與留言 |
| **食譜** | 新增頁面 | GET | `/recipes/create` | `templates/recipe/create.html` | 顯示新增表單 (需登入) |
| **食譜** | 新增處理 | POST | `/recipes/create` | — | 接收表單，存入 DB，重導向至該食譜 |
| **食譜** | 編輯頁面 | GET | `/recipes/<id>/edit`| `templates/recipe/edit.html` | 顯示編輯表單 (限原作者) |
| **食譜** | 編輯處理 | POST | `/recipes/<id>/edit`| — | 接收表單，更新 DB，重導向至該食譜 |
| **食譜** | 刪除處理 | POST | `/recipes/<id>/delete`| — | 刪除食譜，重導向至個人頁面 (限原作者) |
| **互動** | 留言處理 | POST | `/recipes/<id>/comment`| — | 新增留言，重導向至該食譜 (需登入) |
| **互動** | 收藏處理 | POST | `/recipes/<id>/collect`| — | 新增/移除收藏，重導向至該食譜 (需登入) |

---

## 2. 每個路由的詳細說明

### 2.1 首頁模組 (`main.py`)
- **GET `/`**
  - 輸入：無。
  - 邏輯：呼叫 `Recipe.get_all()` 取得最新的食譜列表。
  - 輸出：渲染 `index.html`。

### 2.2 會員模組 (`auth.py`)
- **POST `/auth/register`**
  - 輸入：表單欄位 `username`, `email`, `password`。
  - 邏輯：檢查信箱/帳號是否重複，密碼 hash 後呼叫 `User.create()`，成功則 flash 訊息。
  - 輸出：重導向至 `/auth/login`。若驗證失敗則重新渲染 `register.html`。
- **POST `/auth/login`**
  - 輸入：表單欄位 `email`, `password`。
  - 邏輯：查詢 User 並使用 `check_password_hash` 驗證，成功則將 `user_id` 寫入 `session`。
  - 輸出：重導向至 `/`。若驗證失敗則重新渲染 `login.html` 並提示錯誤。

### 2.3 使用者模組 (`user.py`)
- **GET `/user/profile`**
  - 輸入：自 `session` 取得 `user_id`。
  - 邏輯：檢查登入狀態。查詢該使用者建立的食譜以及收藏的食譜 (`Collection` 關聯)。
  - 輸出：渲染 `profile.html`。未登入則重導向 `/auth/login`。

### 2.4 食譜模組 (`recipe.py`)
- **GET `/recipes/search`**
  - 輸入：Query String `?q=關鍵字` 或 `?type=ingredient`。
  - 邏輯：若為食材搜尋則比對 `ingredients`，若為菜名則比對 `title`，回傳結果列表。
  - 輸出：渲染 `list.html`。
- **POST `/recipes/create`**
  - 輸入：表單 `title`, `description`, `ingredients`, `steps`。
  - 邏輯：檢查登入，呼叫 `Recipe.create()`。
  - 輸出：重導向至 `/recipes/<id>`。
- **POST `/recipes/<id>/edit`**
  - 輸入：表單內容。
  - 邏輯：檢查登入且是否為作者，呼叫 `recipe.update()`。
  - 輸出：重導向至 `/recipes/<id>`。
- **POST `/recipes/<id>/delete`**
  - 輸入：無額外參數。
  - 邏輯：檢查登入且是否為作者，呼叫 `recipe.delete()`。
  - 輸出：重導向至 `/user/profile`。

### 2.5 互動模組 (`comment.py`)
- **POST `/recipes/<id>/comment`**
  - 輸入：表單 `content`。
  - 邏輯：檢查登入，呼叫 `Comment.create()` 關聯當前使用者與食譜。
  - 輸出：重導向至 `/recipes/<id>`。
- **POST `/recipes/<id>/collect`**
  - 輸入：無額外參數。
  - 邏輯：檢查登入。若已收藏則移除 (`delete()`)，若未收藏則新增 (`Collection.create()`)。
  - 輸出：重導向回原頁面或 `/recipes/<id>`。

---

## 3. Jinja2 模板清單

所有模板皆繼承自共用版型 `base.html`：
1. `templates/base.html`：共用頭尾、導覽列 (Navbar 包含搜尋框、登入狀態切換)。
2. `templates/index.html`：首頁。
3. `templates/auth/login.html`：登入頁面。
4. `templates/auth/register.html`：註冊頁面。
5. `templates/user/profile.html`：會員中心 (我的食譜、收藏清單)。
6. `templates/recipe/list.html`：搜尋結果列表。
7. `templates/recipe/detail.html`：食譜詳細內容與留言區塊。
8. `templates/recipe/create.html`：新增食譜表單。
9. `templates/recipe/edit.html`：編輯食譜表單。
