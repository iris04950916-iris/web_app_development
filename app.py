import os
from dotenv import load_dotenv
from app import create_app

# 讀取環境變數 (如 .env 設定)
load_dotenv()

app = create_app()

if __name__ == '__main__':
    # 啟動開發伺服器
    app.run(debug=True)
