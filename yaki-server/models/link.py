from pydantic import BaseModel

class LinkResponse(BaseModel):
    source_note_id: int
    target_note_id: int
