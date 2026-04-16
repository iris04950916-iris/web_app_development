import sqlite3
from .db import get_db

class Admin:
    """管理員資料存取模型"""

    @staticmethod
    def create(username, password_hash):
        """
        建立新管理員帳號。
        參數:
            username (str): 登入帳號
            password_hash (str): 已雜湊的密碼
        回傳:
            int: 新紀錄的 id，若失敗回傳 None。
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO admin (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
            last_id = cursor.lastrowid
            conn.close()
            return last_id
        except sqlite3.Error as e:
            print(f"Admin create error: {e}")
            return None

    @staticmethod
    def get_by_username(username):
        """
        依帳號查詢管理員。
        參數:
            username (str): 登入帳號
        回傳:
            dict: 包含管理員資訊，若找不到或失敗回傳 None。
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM admin WHERE username = ?", (username,))
            row = cursor.fetchone()
            conn.close()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Admin get_by_username error: {e}")
            return None

    @staticmethod
    def get_by_id(admin_id):
        """
        依 ID 查詢管理員。
        參數:
            admin_id (int): 管理員 ID
        回傳:
            dict: 包含管理員資訊，若找不到或失敗回傳 None。
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM admin WHERE id = ?", (admin_id,))
            row = cursor.fetchone()
            conn.close()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Admin get_by_id error: {e}")
            return None
