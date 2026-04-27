from flask import Blueprint, render_template
from app.models.recipe import Recipe

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    # 取得最新發布的食譜 (限制前 6 筆)
    recent_recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(6).all()
    return render_template('index.html', recent_recipes=recent_recipes)
