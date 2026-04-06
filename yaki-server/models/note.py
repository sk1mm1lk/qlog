from pydantic import BaseModel
from typing import Optional
from models.tag import TagResponse

class NoteCreate(BaseModel):
    title: str
    project_title: str = 'yaki'
    relative_file_path: str
    status: str = "draft"
    visibility: str = "private"
    retention_period_days: int = 0
    contents: str
    last_confirmed_at: Optional[str]
    file_hash: str
    hash_algorithm: str
    created_at: Optional[str]
    modified_at: Optional[str]

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    project_title: Optional[str] = None
    relative_file_path: Optional[str] = None
    status: Optional[str] = None
    visibility: Optional[str] = None
    retention_period_days: Optional[int] = None
    contents: Optional[str] = None
    last_confirmed_at: Optional[str] = None
    file_hash: Optional[str] = None
    hash_algorithm: Optional[str] = None
    created_at: Optional[str]
    modified_at: Optional[str]

class NoteResponse(BaseModel):
    id: int
    title: str
    project_title: str
    relative_file_path: str
    status: str
    visibility: str
    retention_period_days: int
    last_confirmed_at: str
    file_hash: str
    hash_algorithm: str
    created_at: str
    modified_at: str

class NoteDetailResponse(NoteResponse):
    contents: str
    tags: list[TagResponse] = []
    forward_links: list[int] = []
    backward_links: list[int] = []
