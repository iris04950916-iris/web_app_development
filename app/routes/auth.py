from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.admin import Admin

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: 顯示管理員登入表單。
    POST: 接收帳號密碼進行驗證。若正確則寫入 Session 並重導向至 dashboard()，否則提示錯誤。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 進行基本的輸入驗證
        if not username or not password:
            flash('請輸入帳號與密碼。', 'warning')
            return redirect(url_for('auth.login'))
            
        admin = Admin.get_by_username(username)
        # 簡單驗證：此為概念驗證專案，直接對比 hash 欄位 (若系統採用明碼或簡易雜湊)。
        if admin and admin['password_hash'] == password:
            session['admin_id'] = admin['id']
            session['username'] = admin['username']
            flash('登入成功！', 'success')
            return redirect(url_for('activity.dashboard'))
        else:
            flash('帳號或密碼錯誤。', 'danger')
            return redirect(url_for('auth.login'))
            
    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    清除 Session 中的使用者登入資訊，確保登出狀態。
    最後重導向回 login() 頁面。
    """
    session.clear()
    flash('您已成功登出系統。', 'info')
    return redirect(url_for('auth.login'))
