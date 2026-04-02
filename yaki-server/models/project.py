from pydantic import BaseModel

class ProjectCreate(BaseModel):
    title: str
    root_file_path: str

class ProjectResponse(BaseModel):
    title: str
    root_file_path: str
    system: str
