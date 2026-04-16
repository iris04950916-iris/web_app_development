from .db import get_db

class DrawResult:
    @staticmethod
    def create(activity_id, participant_id, prize_name):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO draw_result (activity_id, participant_id, prize_name) VALUES (?, ?, ?)",
            (activity_id, participant_id, prize_name)
        )
        # Update participant's is_winner status simultaneously
        cursor.execute(
            "UPDATE participant SET is_winner = 1 WHERE id = ?",
            (participant_id,)
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    @staticmethod
    def get_by_activity_id(activity_id):
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

    @staticmethod
    def get_all():
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

    @staticmethod
    def get_by_id(result_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM draw_result WHERE id = ?", (result_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def delete(result_id, participant_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM draw_result WHERE id = ?", (result_id,))
        # Optional depending on business logic: rollback participant is_winner flag
        cursor.execute("UPDATE participant SET is_winner = 0 WHERE id = ?", (participant_id,))
        conn.commit()
        conn.close()
