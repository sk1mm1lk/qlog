-- Drop existing objects incase they exist
DROP TABLE IF EXISTS links;
DROP TABLE IF EXISTS notes_tags;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS notes;
DROP SEQUENCE IF EXISTS notes_id_seq;

-- Create the objects
CREATE SEQUENCE IF NOT EXISTS notes_id_seq START 1;

CREATE TABLE IF NOT EXISTS notes (
    id                    INTEGER PRIMARY KEY DEFAULT nextval('notes_id_seq'),
    title                 VARCHAR NOT NULL,
    relative_file_path    VARCHAR NOT NULL,
    namespace             VARCHAR DEFAULT 'me',
    status                VARCHAR DEFAULT 'draft',
    visibility            VARCHAR DEFAULT 'private',
    file_hash             VARCHAR NOT NULL,
    created_at            TIMESTAMP,
    modified_at           TIMESTAMP,
    last_indexed_at       TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tags (
    id     INTEGER PRIMARY KEY,
    title  VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS notes_tags (
    note_id     INTEGER NOT NULL,
    tag_id      INTEGER NOT NULL,
    PRIMARY KEY (note_id, tag_id)
);

CREATE TABLE IF NOT EXISTS links (
    source_note_id INTEGER REFERENCES notes(id),
    target_note_id INTEGER REFERENCES notes(id),
    PRIMARY KEY (source_note_id, target_note_id)
);
