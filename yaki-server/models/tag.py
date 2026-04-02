from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TagResponse(BaseModel):
    id: int
    title: str
