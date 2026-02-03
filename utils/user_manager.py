"""
Управление пользователями системы
"""

import json
import os

USERS_FILE = "data/users.json"


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users: dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def add_user(username: str, role: str):
    users = load_users()

    if username in users:
        raise ValueError("Пользователь уже существует")

    users[username] = role
    save_users(users)


def remove_user(username: str):
    users = load_users()

    if username not in users:
        raise ValueError("Пользователь не найден")

    del users[username]
    save_users(users)


def get_role(username: str) -> str:
    users = load_users()
    return users.get(username, "Пользователь")
