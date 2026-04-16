from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: 顯示管理員登入表單。
    POST: 接收帳號密碼進行驗證。若正確則寫入 Session 並重導向至 dashboard()，否則提示錯誤。
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    清除 Session 中的使用者登入資訊，確保登出狀態。
    最後重導向回 login() 頁面。
    """
    pass
