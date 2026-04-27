from flask import Blueprint

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/profile', methods=['GET'])
def profile():
    """
    個人頁面。
    必須登入。
    顯示使用者上傳的食譜與收藏的食譜清單。
    輸出：渲染 profile.html
    """
    pass
