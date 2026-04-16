import sqlite3
from .db import get_db

class Activity:
    """活動資料存取模型"""

    @staticmethod
    def create(name, description, status='ongoing'):
        """
        新增一筆抽籤活動紀錄。
        參數:
            name (str): 活動名稱
            description (str): 活動描述
            status (str): 活動狀態，預設 'ongoing'
        回傳:
            int: 新活動的 ID，失敗則為 None
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO activity (name, description, status) VALUES (?, ?, ?)",
                (name, description, status)
            )
            conn.commit()
            last_id = cursor.lastrowid
            conn.close()
            return last_id
        except sqlite3.Error as e:
            print(f"Activity create error: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有活動記錄，預設依照建立時間反序排列。
        回傳:
            list: 包含多筆活動資訊字典的清單
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM activity ORDER BY created_at DESC")
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Activity get_all error: {e}")
            return []

    @staticmethod
    def get_by_id(activity_id):
        """
        取得單筆活動記錄。
        參數:
            activity_id (int): 設定的活動 ID
        回傳:
            dict: 若存在回傳該筆字典資訊，否則為 None
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM activity WHERE id = ?", (activity_id,))
            row = cursor.fetchone()
            conn.close()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Activity get_by_id error: {e}")
            return None

    @staticmethod
    def update(activity_id, name, description, status):
        """
        更新指定的活動資料。
        參數:
            activity_id (int): 設定的活動 ID
            name (str): 活動名稱
            description (str): 活動描述
            status (str): 狀態更新
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE activity SET name = ?, description = ?, status = ? WHERE id = ?",
                (name, description, status, activity_id)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Activity update error: {e}")
            return False

    @staticmethod
    def delete(activity_id):
        """
        刪除特定活動記錄。由於資料庫設定，連屬的參加者與中獎也會一起刪除 (CASCADE)。
        參數:
            activity_id (int): 指定的活動 ID
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM activity WHERE id = ?", (activity_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Activity delete error: {e}")
            return False
