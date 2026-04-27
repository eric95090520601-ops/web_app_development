from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from app.models.recipe import Recipe
from app.models.collection import Collection

recipe_bp = Blueprint('recipe', __name__, url_prefix='/recipes')

@recipe_bp.route('/search', methods=['GET'])
def search():
    ingredient = request.args.get('ingredient', '').strip()
    q = request.args.get('q', '').strip()
    
    recipes = []
    if ingredient:
        recipes = Recipe.query.filter(Recipe.ingredients.ilike(f'%{ingredient}%')).order_by(Recipe.created_at.desc()).all()
    elif q:
        recipes = Recipe.query.filter(Recipe.title.ilike(f'%{q}%')).order_by(Recipe.created_at.desc()).all()
    else:
        recipes = Recipe.get_all()
        
    return render_template('recipe/list.html', recipes=recipes, ingredient=ingredient, q=q)

@recipe_bp.route('/create', methods=['GET', 'POST'])
def create():
    if 'user_id' not in session:
        flash('請先登入才能新增食譜。', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')

        if not title or not ingredients or not steps:
            flash('標題、食材與步驟都是必填欄位。', 'danger')
            return render_template('recipe/create.html', title=title, description=description, ingredients=ingredients, steps=steps)

        try:
            recipe = Recipe.create(
                user_id=session['user_id'],
                title=title,
                ingredients=ingredients,
                steps=steps,
                description=description
            )
            flash('食譜發布成功！', 'success')
            return redirect(url_for('recipe.detail', id=recipe.id))
        except Exception as e:
            flash('食譜發布失敗，請稍後再試。', 'danger')

    return render_template('recipe/create.html')

@recipe_bp.route('/<int:id>', methods=['GET'])
def detail(id):
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜。', 'danger')
        return redirect(url_for('main.index'))
        
    is_collected = False
    if 'user_id' in session:
        collection = Collection.query.filter_by(user_id=session['user_id'], recipe_id=id).first()
        if collection:
            is_collected = True
            
    return render_template('recipe/detail.html', recipe=recipe, is_collected=is_collected)

@recipe_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    if 'user_id' not in session:
        flash('請先登入。', 'warning')
        return redirect(url_for('auth.login'))
        
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜。', 'danger')
        return redirect(url_for('main.index'))
        
    if recipe.user_id != session['user_id']:
        flash('您沒有權限編輯此食譜。', 'danger')
        return redirect(url_for('recipe.detail', id=id))
        
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        
        if not title or not ingredients or not steps:
            flash('標題、食材與步驟都是必填欄位。', 'danger')
            return render_template('recipe/edit.html', recipe=recipe)
            
        success = recipe.update(title=title, description=description, ingredients=ingredients, steps=steps)
        if success:
            flash('食譜更新成功！', 'success')
            return redirect(url_for('recipe.detail', id=recipe.id))
        else:
            flash('食譜更新失敗。', 'danger')
            
    return render_template('recipe/edit.html', recipe=recipe)

@recipe_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    if 'user_id' not in session:
        flash('請先登入。', 'warning')
        return redirect(url_for('auth.login'))
        
    recipe = Recipe.get_by_id(id)
    if recipe and recipe.user_id == session['user_id']:
        if recipe.delete():
            flash('食譜已刪除。', 'success')
        else:
            flash('食譜刪除失敗。', 'danger')
    else:
        flash('您沒有權限刪除此食譜或食譜不存在。', 'danger')
        
    return redirect(url_for('user.profile'))

@recipe_bp.route('/<int:id>/collect', methods=['POST'])
def collect(id):
    if 'user_id' not in session:
        flash('請先登入才能收藏食譜。', 'warning')
        return redirect(url_for('auth.login'))
        
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜。', 'danger')
        return redirect(url_for('main.index'))
        
    collection = Collection.query.filter_by(user_id=session['user_id'], recipe_id=id).first()
    if collection:
        collection.delete()
        flash('已取消收藏。', 'info')
    else:
        try:
            Collection.create(user_id=session['user_id'], recipe_id=id)
            flash('收藏成功！', 'success')
        except Exception as e:
            flash('收藏失敗。', 'danger')
            
    # Redirect back to the referrer or recipe detail
    referrer = request.referrer
    if referrer:
        return redirect(referrer)
    return redirect(url_for('recipe.detail', id=id))
