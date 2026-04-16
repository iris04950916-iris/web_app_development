from .db import get_db

class Participant:
    @staticmethod
    def create(activity_id, name):
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

    @staticmethod
    def get_by_activity_id(activity_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM participant WHERE activity_id = ? ORDER BY id", (activity_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
        
    @staticmethod
    def get_eligible_participants(activity_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM participant WHERE activity_id = ? AND is_winner = 0", (activity_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(participant_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM participant WHERE id = ?", (participant_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def update(participant_id, name, is_winner):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE participant SET name = ?, is_winner = ? WHERE id = ?",
            (name, is_winner, participant_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(participant_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM participant WHERE id = ?", (participant_id,))
        conn.commit()
        conn.close()
