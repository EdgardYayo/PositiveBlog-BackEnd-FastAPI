def post_entity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "title" : item["title"],
        "content": item["content"],
        "author_id": item["author_id"]
    }


def posts_entity(items) -> list:
    posts = []
    for item in items:
        item["author_id"]["_id"] = str(item["author_id"]["_id"])
        del item["author_id"]["password"]
        posts.append(post_entity(item))
    return posts