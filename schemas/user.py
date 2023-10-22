def user_entity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "email": item["email"],
        "password": item["password"]
    }


def users_entity(items) -> list:
    return [user_entity(item) for item in items]