import sqlite3
from .db import get_db

class DrawResult:
    """抽籤紀錄結果存取模型"""

    @staticmethod
    def create(activity_id, participant_id, prize_name):
        """
        產生一筆抽籤得獎紀錄並將對應的參加者改為以得獎狀態。
        參數:
            activity_id (int): 關聯活動 ID
            participant_id (int): 得獎的參加者 ID
            prize_name (str): 得獎獎項名稱
        回傳:
            int: 產出的中獎紀錄 ID，失敗則返回 None
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO draw_result (activity_id, participant_id, prize_name) VALUES (?, ?, ?)",
                (activity_id, participant_id, prize_name)
            )
            # 同步將該參與者的中獎狀態打開
            cursor.execute(
                "UPDATE participant SET is_winner = 1 WHERE id = ?",
                (participant_id,)
            )
            conn.commit()
            last_id = cursor.lastrowid
            conn.close()
            return last_id
        except sqlite3.Error as e:
            print(f"DrawResult create error: {e}")
            return None

    @staticmethod
    def get_by_activity_id(activity_id):
        """
        取得特定活動所有中獎者的清單 (包含 JOIN 取得人名)。
        參數:
            activity_id (int): 活動 ID
        回傳:
            list: 中獎記錄包含人名字典
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT dr.*, p.name as participant_name 
                FROM draw_result dr 
                JOIN participant p ON dr.participant_id = p.id 
                WHERE dr.activity_id = ? 
                ORDER BY dr.created_at DESC
            ''', (activity_id,))
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"DrawResult get_by_activity_id error: {e}")
            return []

    @staticmethod
    def get_all():
        """
        取得全系統所有的活動中獎者名單。
        回傳:
            list: 包含中獎者細節與活動名稱的清單。
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT dr.*, p.name as participant_name, a.name as activity_name 
                FROM draw_result dr 
                JOIN participant p ON dr.participant_id = p.id
                JOIN activity a ON dr.activity_id = a.id
                ORDER BY dr.created_at DESC
            ''')
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"DrawResult get_all error: {e}")
            return []

    @staticmethod
    def get_by_id(result_id):
        """
        以中獎資料 ID 取出單筆中獎紀錄。
        參數:
            result_id (int): 定位的中獎紀錄 ID
        回傳:
            dict: 回傳資訊或失敗回傳 None
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM draw_result WHERE id = ?", (result_id,))
            row = cursor.fetchone()
            conn.close()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"DrawResult get_by_id error: {e}")
            return None

    @staticmethod
    def delete(result_id, participant_id):
        """
        移除該得獎紀錄並將該使用者的狀態回歸為未中獎。
        參數:
            result_id (int): 得獎紀錄 ID
            participant_id (int): 該使用者的 ID
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM draw_result WHERE id = ?", (result_id,))
            cursor.execute("UPDATE participant SET is_winner = 0 WHERE id = ?", (participant_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"DrawResult delete error: {e}")
            return False
