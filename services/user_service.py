def get_user_by_id(user_id: str) -> str:
    # Simulasi ambil dari database
    fake_db = {
        "SV24-1": {"name": "Steven", "status": "Active"},
        "SV24-2": {"name": "Liem", "status": "Inactive"},
    }
    data = fake_db.get(user_id)
    if not data:
        return f"User with ID '{user_id}' not found."
    
    return f"User ID: {user_id}\nName: {data['name']}\nStatus: {data['status']}"   