from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    首頁。
    輸入：無
    處理邏輯：取得最新/熱門食譜列表
    輸出：渲染 index.html
    """
    pass
