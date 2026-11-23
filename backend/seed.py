"""Buat akun demo secara manual:  python -m backend.seed"""

from backend.config import load_config
from backend.db import init_db, seed_demo_users

if __name__ == "__main__":
    created = seed_demo_users(init_db(load_config()))
    print("Akun dibuat:", ", ".join(created) if created else "(semua sudah ada)")
