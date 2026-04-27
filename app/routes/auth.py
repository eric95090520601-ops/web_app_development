from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    註冊頁面與處理。
    GET: 顯示註冊表單
    POST: 接收資料，驗證與 hash 密碼，建立 User，重導向至登入頁
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    登入頁面與處理。
    GET: 顯示登入表單
    POST: 驗證帳密，設定 session，重導向至首頁
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    登出處理。
    清除 session，重導向至首頁
    """
    pass
