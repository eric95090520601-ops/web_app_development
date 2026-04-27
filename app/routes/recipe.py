from flask import Blueprint

recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')

@recipe_bp.route('/search', methods=['GET'])
def search():
    """
    搜尋食譜。
    依據 query string 參數 (關鍵字或食材) 搜尋。
    輸出：渲染 list.html
    """
    pass

@recipe_bp.route('/create', methods=['GET', 'POST'])
def create():
    """
    新增食譜。
    必須登入。
    GET: 顯示新增表單
    POST: 驗證表單，儲存食譜，重導向至食譜詳細頁面
    """
    pass

@recipe_bp.route('/<int:id>', methods=['GET'])
def detail(id):
    """
    食譜詳細內容。
    顯示單一食譜與其留言。
    輸出：渲染 detail.html
    """
    pass

@recipe_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    編輯食譜。
    必須登入，且為該食譜作者。
    GET: 顯示編輯表單
    POST: 更新食譜，重導向至食譜詳細頁面
    """
    pass

@recipe_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除食譜。
    必須登入，且為該食譜作者。
    刪除後重導向至個人頁面。
    """
    pass

@recipe_bp.route('/<int:id>/collect', methods=['POST'])
def collect(id):
    """
    收藏/取消收藏食譜。
    必須登入。
    切換該食譜的收藏狀態，重導向回原頁面。
    """
    pass
