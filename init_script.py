from app.models.db import init_db
from app.models.admin import Admin

def setup():
    init_db("database/schema.sql")
    if not Admin.get_by_username("admin"):
        Admin.create("admin", "admin")
    print("DB initialized with default admin (admin/admin).")

if __name__ == "__main__":
    setup()
