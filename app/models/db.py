import sqlite3
import os
from pathlib import Path

# 取 instance 的位置，並將 db 檔案建立在裡面
DB_FOLDER = Path(os.getcwd()) / "instance"
DB_PATH = DB_FOLDER / "database.db"

def get_db():
    """取得資料庫連線"""
    DB_FOLDER.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 允許使用欄位名稱存取資料
    return conn

def init_db(schema_path):
    """初始化資料庫與資料表"""
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn = get_db()
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
