from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash('所有欄位都是必填的！', 'danger')
            return render_template('auth/register.html')

        # 檢查是否重複
        if User.query.filter_by(username=username).first():
            flash('使用者名稱已被註冊。', 'danger')
            return render_template('auth/register.html')
        if User.query.filter_by(email=email).first():
            flash('電子信箱已被註冊。', 'danger')
            return render_template('auth/register.html')

        password_hash = generate_password_hash(password)
        try:
            User.create(username=username, email=email, password_hash=password_hash)
            flash('註冊成功！請登入。', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('註冊失敗，請稍後再試。', 'danger')

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('登入成功！', 'success')
            return redirect(url_for('main.index'))
        
        flash('電子信箱或密碼錯誤。', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash('您已成功登出。', 'success')
    return redirect(url_for('main.index'))
