import sqlite3
from .db import get_db

class Participant:
    """參加者資料存取模型"""

    @staticmethod
    def create(activity_id, name):
        """
        新增單一參加者紀錄對應到特定活動。
        參數:
            activity_id (int): 活動的 ID
            name (str): 參加者名稱
        回傳:
            int: 新參加者的 ID，失敗則為 None
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO participant (activity_id, name) VALUES (?, ?)",
                (activity_id, name)
            )
            conn.commit()
            last_id = cursor.lastrowid
            conn.close()
            return last_id
        except sqlite3.Error as e:
            print(f"Participant create error: {e}")
            return None

    @staticmethod
    def get_by_activity_id(activity_id):
        """
        取得特定活動下的所有參加者名單。
        參數:
            activity_id (int): 指定活動 ID
        回傳:
            list: 參與者字典的 list 集合
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM participant WHERE activity_id = ? ORDER BY id", (activity_id,))
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Participant get_by_activity_id error: {e}")
            return []
        
    @staticmethod
    def get_eligible_participants(activity_id):
        """
        取得特定活動下「尚未中獎」的使用者，作為抽籤候選清單。
        參數:
            activity_id (int): 指定活動 ID
        回傳:
            list: 參與者字典的 list 集合
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM participant WHERE activity_id = ? AND is_winner = 0", (activity_id,))
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Participant get_eligible_participants error: {e}")
            return []

    @staticmethod
    def get_by_id(participant_id):
        """
        取得單筆參加者紀錄。
        參數:
            participant_id (int): 指定參加者 ID
        回傳:
            dict: 若存在回傳該筆字典資訊，否則為 None
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM participant WHERE id = ?", (participant_id,))
            row = cursor.fetchone()
            conn.close()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Participant get_by_id error: {e}")
            return None

    @staticmethod
    def update(participant_id, name, is_winner):
        """
        修改參加者的相關資料與是否中獎標記。
        參數:
            participant_id (int): 參加者 ID
            name (str): 參加者姓名
            is_winner (int): 0 為未中獎，1 為已中獎
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE participant SET name = ?, is_winner = ? WHERE id = ?",
                (name, is_winner, participant_id)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Participant update error: {e}")
            return False

    @staticmethod
    def delete(participant_id):
        """
        刪除特定參加者，防呆移除特定名單。
        參數:
            participant_id (int): 參與者 ID
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM participant WHERE id = ?", (participant_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Participant delete error: {e}")
            return False
