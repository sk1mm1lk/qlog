from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.tag import TagResponse

class NoteCreate(BaseModel):
    title: str
    project_title: str = 'yaki'
    relative_file_path: str
    status: str = "draft"
    visibility: str = "private"
    retention_period_days: int = 0
    contents: bytes
    last_confirmed_at: Optional[datetime]
    file_hash: bytes
    hash_algorithm: str
    created_at: Optional[datetime]
    modified_at: Optional[datetime]

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    project_title: Optional[str] = None
    relative_file_path: Optional[str] = None
    status: Optional[str] = None
    visibility: Optional[str] = None
    retention_period_days: Optional[int] = None
    contents: Optional[bytes] = None
    last_confirmed_at: Optional[datetime] = None
    file_hash: Optional[bytes] = None
    hash_algorithm: Optional[str] = None
    created_at: Optional[datetime]
    modified_at: Optional[datetime]

class NoteResponse(BaseModel):
    id: int
    title: str
    project_title: str
    relative_file_path: str
    status: str
    visibility: str
    retention_period_days: int
    last_confirmed_at: datetime
    file_hash: bytes
    hash_algorithm: str
    created_at: datetime
    modified_at: datetime

class NoteDetailResponse(NoteResponse):
    contents: bytes
    tags: list[TagResponse] = []
    forward_links: list[int] = []
    backward_links: list[int] = []
