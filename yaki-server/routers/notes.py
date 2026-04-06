from fastapi import APIRouter, HTTPException 
from models.note import NoteCreate, NoteUpdate, NoteResponse, NoteDetailResponse
from models.tag import TagResponse
from models.link import LinkResponse
from models.project import ProjectCreate, ProjectResponse
from data.database import get_db
from datetime import datetime, timezone
from typing import Optional
import base64
import uuid

router = APIRouter(prefix='/notes', tags=['notes'])

@router.get('/', response_model=list[NoteResponse])
def list_notes(
    status: Optional[str] = None,
    visibility: Optional[str] = None,
    project_title: Optional[str] = None,
    tag: Optional[str] = None
):
    db = get_db()

    query = '''
        SELECT DISTINCT
            n.id,
            n.title,
            n.project_title,
            n.relative_file_path,
            n.status,
            n.visibility,
            n.retention_period_days,
            --n.contents,  --  Don't want to be sending so much information for just listing
            n.last_confirmed_at,
            n.file_hash,
            n.hash_algorithm,
            n.created_at,
            n.modified_at
        FROM notes n
        LEFT JOIN notes_tags nt
            ON n.id = nt.note_id
        LEFT JOIN tags t
            ON nt.tag_id = t.id
        WHERE 1=1
    '''
    params = []

    if status:
        query += ' AND status = ?'
        params.append(status)

    if visibility:
        query += ' AND visibility = ?'
        params.append(visibility)

    if project_title:
        query += ' AND project_title = ?'
        params.append(project_title)

    if tag:
        query += ' AND tag = ?'
        params.append(tag)

    results = db.execute(query, params).fetchall()
    return results

@router.get('/{note_id}', response_model=NoteDetailResponse)
def get_note(note_id: int):
    db = get_db()

    columns = [
        'id',
        'title',
        'project_title',
        'relative_file_path',
        'status',
        'visibility',
        'retention_period_days',
        'contents',
        'last_confirmed_at',
        'file_hash',
        'hash_algorithm',
        'created_at',
        'modified_at'
    ]

    query = f'''
        SELECT
            {','.join(columns)}
        FROM notes
        WHERE id = ?
    '''
    params = [note_id]
    note = db.execute(query, params).fetchone()

    if not note:
        raise HTTPEXception (status_code=404, detail="Note not found")

    note_dict = {}

    for i, cell in enumerate(note):
        note_dict[columns[i]] = cell

    # last_confirmed_at
    note_dict['last_confirmed_at'] = note_dict['last_confirmed_at'].strftime('%Y-%m-%d %H:%M:%S')

    # created_at
    note_dict['created_at'] = note_dict['created_at'].strftime('%Y-%m-%d %H:%M:%S')

    # modified_at
    note_dict['modified_at'] = note_dict['modified_at'].strftime('%Y-%m-%d %H:%M:%S')

    # contents
    note_dict['contents'] = base64.b64encode(note_dict['contents']).decode('ascii')

    # file_hash
    note_dict['file_hash'] = base64.b64encode(note_dict['file_hash']).decode('ascii')

    query = '''
        SELECT
            t.id, t.title
        FROM tags t
        JOIN notes_tags nt
            ON t.id = nt.tag_id
        WHERE nt.note_id = ?
    '''
    params = [note_id]
    tags = db.execute(query, params).fetchall()

    query = '''
        SELECT target_note_id
        FROM links
        WHERE source_note_id = ?
    '''
    params = [note_id]
    forward_links = db.execute(query, params).fetchall()

    query = '''
        SELECT source_note_id
        FROM links
        WHERE target_note_id = ?
    '''
    params = [note_id]
    backward_links = db.execute(query, params).fetchall()

    return {
        **note_dict,
        'tags': [TagResponse(id=t[0], title=t[1]) for t in tags],
        'forward_links': [r[0] for r in forward_links],
        'backward_links': [r[0] for r in backward_links]
    }

@router.post('/', response_model=NoteDetailResponse, status_code=201)
def create_note(note: NoteCreate):
    db = get_db()

    current_timestamp = datetime.now(timezone.utc)

    query = '''
        INSERT INTO notes (
            title,
            project_title,
            relative_file_path,
            status,
            visibility,
            retention_period_days,
            contents,
            last_confirmed_at,
            file_hash,
            hash_algorithm,
            created_at,
            modified_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        RETURNING id
    '''
    params = [
        note.title,
        note.project_title,
        note.relative_file_path,
        note.status,
        note.visibility,
        note.retention_period_days,
        note.contents,
        note.last_confirmed_at if note.last_confirmed_at else current_timestamp,
        note.file_hash,
        note.hash_algorithm,
        note.created_at if note.created_at else current_timestamp,
        note.modified_at if note.modified_at else current_timestamp
    ]
    result = db.execute(query, params).fetchone()

    return get_note(result[0])

@router.patch('/{note_id}', response_model=NoteDetailResponse)
def update_note(note_id: int, note: NoteUpdate):
    db = get_db()

    is_existing = db.execute('SELECT id FROM notes WHERE id = ?', [note_id]).fetchone()

    if not is_existing:
        raise HTTPException(status_code=404, detail='Note not found')

    fields = note.model_dump(exclude_none=True)

    if not fields:
        raise HTTPException(status_code=400, detail='No fields provided')

    set_clause = ', '.join(f'{field} = ?' for field in fields)
    # TODO: Add a check for modified_at being changed, and if not set as current timestamp
    query = f'''
        UPDATE notes SET
            {set_clause}
        WHERE id = ?
    '''
    params = list(fields.values()) + [note_id]

    db.execute(query, params)

    return get_note(note_id)

@router.delete('/{note_id}', status_code=204)
def delete_note(note_id: int):
    db = get_db()

    is_existing = db.execute('SELECT id FROM notes WHERE id = ?', [note_id]).fetchone()

    if not is_existing:
        raise HTTPException(status_code=404, detail='Note not found')

    db.execute('DELETE FROM notes_tags WHERE note_id = ?', [note_id])
    db.execute('DELETE FROM links WHERE source_note_id = ? OR target_note_id = ?', [note_id, note_id])
    db.execute('DELETE FROM notes WHERE note_id = ?', [note_id])
