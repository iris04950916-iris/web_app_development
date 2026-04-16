import sqlite3
import os
from pathlib import Path

# 取 instance 的位置，並將 db 檔案建立在裡面
DB_FOLDER = Path(os.getcwd()) / "instance"
DB_PATH = DB_FOLDER / "database.db"

def get_db():
    """
    取得 SQLite 資料庫連線，並設定 row_factory 讓查詢結果能以字典欄位方式取值。
    """
    try:
        DB_FOLDER.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def init_db(schema_path):
    """
    讀取 SQL 檔案並初始化資料庫與資料表。
    參數:
        schema_path (str): schema SQL 檔案的相對或絕對路徑。
    """
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        conn = get_db()
        if conn:
            conn.executescript(schema_sql)
            conn.commit()
            conn.close()
    except Exception as e:
        print(f"Failed to initialize db: {e}")
