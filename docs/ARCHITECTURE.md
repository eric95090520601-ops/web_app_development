# 系統架構設計文件 (Architecture) - 食譜收藏檢索系統

## 1. 技術架構說明

本專案採用經典的「伺服器端渲染 (Server-Side Rendering, SSR)」架構，不進行前後端分離，藉此降低開發初期的複雜度，適合快速打造出符合 MVP 範圍的產品。

### 1.1 選用技術與原因
- **後端框架：Python + Flask**
  - 原因：Flask 是輕量級的 Python 網頁框架，彈性極高且易於上手，非常適合用來開發小至中型的食譜系統。
- **模板引擎：Jinja2**
  - 原因：內建於 Flask 中，能方便地將後端資料（如食譜列表、留言）嵌入 HTML 中，動態渲染出網頁給使用者。
- **資料庫：SQLite (搭配 SQLAlchemy ORM)**
  - 原因：SQLite 是一個輕量、無需額外安裝伺服器的關聯式資料庫，所有資料存於單一檔案中，非常適合初期開發與部署。搭配 SQLAlchemy 能有效防範 SQL Injection 並簡化資料庫操作。
- **前端技術：HTML / CSS / JavaScript**
  - 原因：使用原生的前端技術（可搭配 Bootstrap 或 Tailwind 等 CSS 框架），足夠應付食譜展示與表單送出等互動需求。

### 1.2 Flask MVC 模式說明
雖然 Flask 本身沒有強制的目錄結構，但我們將採用類似 MVC（Model-View-Controller）的模式來組織程式碼：
- **Model（模型）**：負責與 SQLite 資料庫互動，定義資料表結構（如 `User`, `Recipe`, `Comment`），處理資料的儲存與讀取。
- **View（視圖）**：負責畫面呈現，由 Jinja2 模板（`.html` 檔）組成，接收來自 Controller 的資料並渲染成最終網頁。
- **Controller（控制器）**：對應到 Flask 的路由（Routes/Views 函數）。負責接收使用者的 HTTP 請求（如搜尋食譜、送出留言），調用對應的 Model 處理業務邏輯，最後把結果傳遞給 View。

---

## 2. 專案資料夾結構

本專案將依照模組化的方式來組織資料夾，以下為完整的資料夾樹狀圖與說明：

```text
web_app_development/
├── app/                      # 應用程式主目錄
│   ├── __init__.py           # Flask 應用程式初始化與設定
│   ├── models/               # 資料庫模型 (Model)
│   │   ├── __init__.py
│   │   ├── user.py           # 會員資料表
│   │   ├── recipe.py         # 食譜與食材資料表
│   │   └── comment.py        # 留言與收藏關聯表
│   ├── routes/               # Flask 路由處理 (Controller)
│   │   ├── __init__.py
│   │   ├── auth.py           # 註冊、登入相關路由
│   │   ├── recipe.py         # 搜尋、新增、收藏食譜相關路由
│   │   └── comment.py        # 留言相關路由
│   ├── templates/            # Jinja2 HTML 模板 (View)
│   │   ├── base.html         # 共用版型（導覽列、頁尾）
│   │   ├── index.html        # 首頁（搜尋與熱門食譜）
│   │   ├── auth/             # 認證相關頁面
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── recipe/           # 食譜相關頁面
│   │       ├── detail.html   # 食譜詳細內容
│   │       ├── create.html   # 新增食譜表單
│   │       └── list.html     # 搜尋結果列表
│   └── static/               # 靜態資源檔案
│       ├── css/
│       │   └── style.css     # 自訂樣式表
│       ├── js/
│       │   └── main.js       # 前端互動邏輯
│       └── img/              # 網站預設圖片或圖示
├── instance/                 # 放置不進入版控的實例檔案
│   └── database.db           # SQLite 資料庫檔案
├── docs/                     # 專案說明文件
│   ├── PRD.md                # 產品需求文件
│   └── ARCHITECTURE.md       # 系統架構文件
├── app.py                    # 專案啟動入口點
├── config.py                 # 環境變數與組態設定檔
└── requirements.txt          # Python 依賴套件清單
```

---

## 3. 元件關係圖

以下展示使用者在瀏覽器操作時，系統各元件之間的互動流程：

```mermaid
flowchart TD
    Browser[瀏覽器 (Client)]
    
    subgraph 伺服器端 (Server - Flask)
        Controller[Flask Route (Controller)]
        Model[資料庫模型 (Model)]
        Template[Jinja2 模板 (View)]
    end
    
    DB[(SQLite 資料庫)]
    
    %% 流程線
    Browser -- "1. 發送 HTTP 請求\n(例如：搜尋番茄炒蛋)" --> Controller
    Controller -- "2. 查詢食譜資料" --> Model
    Model -- "3. 讀寫資料" --> DB
    DB -. "4. 回傳查詢結果" .-> Model
    Model -. "5. 將物件交給路由" .-> Controller
    Controller -- "6. 傳遞資料與變數" --> Template
    Template -. "7. 渲染出 HTML 網頁" .-> Controller
    Controller -. "8. 回傳 HTTP 回應\n(HTML)" .-> Browser
```

---

## 4. 關鍵設計決策

1. **採用 SQLAlchemy ORM 取代原生 SQL 語法**
   - **原因**：使用 ORM（如 `flask-sqlalchemy`）可以讓開發者用 Python 物件的方式操作資料庫，不只大幅提升開發速度、讓程式碼更具可讀性，更能自動處理字串跳脫，有效防範 SQL Injection 攻擊。
2. **採用 Blueprint (藍圖) 切分路由**
   - **原因**：如果將所有功能（認證、食譜、留言）都寫在同一個 `app.py` 中，檔案將會過於龐大難以維護。透過 Flask Blueprint，我們可以將 `auth`, `recipe`, `comment` 切分到獨立的檔案中，實現關注點分離。
3. **密碼加密機制**
   - **原因**：基於資安考量，資料庫絕不能儲存使用者的明文密碼。我們將使用 `werkzeug.security` 提供的 `generate_password_hash` 和 `check_password_hash` 功能，在儲存與驗證密碼時進行單向雜湊。
4. **集中式版型設計 (Template Inheritance)**
   - **原因**：每個網頁通常會有相同的導覽列（Navbar）與頁尾（Footer）。在 Jinja2 中我們建立一個 `base.html` 作為母版，其他頁面只需透過 `{% extends 'base.html' %}` 來繼承，即可避免重複撰寫相同的 HTML 程式碼，日後修改共用區塊也只需改一個地方。
