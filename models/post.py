from typing import Optional, Text
from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: Text
    author_id: Optional[dict[str, str]] = None