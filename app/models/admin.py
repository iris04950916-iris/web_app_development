from .db import get_db

class Admin:
    @staticmethod
    def create(username, password_hash):
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

    @staticmethod
    def get_by_username(username):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def get_by_id(admin_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE id = ?", (admin_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
