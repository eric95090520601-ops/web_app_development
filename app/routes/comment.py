from flask import Blueprint, request, redirect, url_for, flash, session
from app.models.comment import Comment
from app.models.recipe import Recipe

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/recipes/<int:recipe_id>/comment', methods=['POST'])
def create_comment(recipe_id):
    if 'user_id' not in session:
        flash('請先登入後再留言。', 'warning')
        return redirect(url_for('auth.login'))
        
    content = request.form.get('content')
    if not content or not content.strip():
        flash('留言內容不能為空。', 'danger')
        return redirect(url_for('recipe.detail', id=recipe_id))
        
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        flash('找不到該食譜。', 'danger')
        return redirect(url_for('main.index'))
        
    try:
        Comment.create(user_id=session['user_id'], recipe_id=recipe_id, content=content.strip())
        flash('留言成功！', 'success')
    except Exception as e:
        flash('留言失敗。', 'danger')
        
    return redirect(url_for('recipe.detail', id=recipe_id))
