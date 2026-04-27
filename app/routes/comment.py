from flask import Blueprint

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/recipes/<int:recipe_id>/comment', methods=['POST'])
def create_comment(recipe_id):
    """
    新增留言。
    必須登入。
    接收留言內容，關聯當前使用者與該食譜。
    處理完畢後重導向回食譜詳細頁面。
    """
    pass
