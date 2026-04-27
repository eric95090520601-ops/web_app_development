from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models.user import User

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/profile', methods=['GET'])
def profile():
    if 'user_id' not in session:
        flash('請先登入。', 'warning')
        return redirect(url_for('auth.login'))
        
    user = User.get_by_id(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))
        
    # 取得我的食譜
    my_recipes = user.recipes
    # 取得我的收藏 (找出 collection 對應的 recipe)
    collected_recipes = [collection.recipe for collection in user.collections]
    
    return render_template('user/profile.html', user=user, my_recipes=my_recipes, collected_recipes=collected_recipes)
