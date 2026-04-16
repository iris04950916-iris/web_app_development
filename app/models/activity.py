from .db import get_db

class Activity:
    @staticmethod
    def create(name, description, status='ongoing'):
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

    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activity ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(activity_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activity WHERE id = ?", (activity_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def update(activity_id, name, description, status):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE activity SET name = ?, description = ?, status = ? WHERE id = ?",
            (name, description, status, activity_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(activity_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM activity WHERE id = ?", (activity_id,))
        conn.commit()
        conn.close()
