-- Drop existing objects incase they exist
DROP TABLE IF EXISTS links;
DROP TABLE IF EXISTS notes_key_value;
DROP TABLE IF EXISTS notes;
DROP SEQUENCE IF EXISTS notes_id_seq;
DROP SEQUENCE IF EXISTS notes_key_value_id_seq;

-- Create the objects
CREATE SEQUENCE IF NOT EXISTS notes_id_seq START 1;
CREATE SEQUENCE IF NOT EXISTS notes_key_value_id_seq START 1;

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

CREATE TABLE IF NOT EXISTS notes_key_value (
    id         INTEGER PRIMARY KEY DEFAULT nextval('notes_key_value_id_seq'),
    note_id    INTEGER REFERENCES notes(id),
    note_key   VARCHAR,
    note_value VARCHAR,
    value_type VARCHAR
);

CREATE TABLE IF NOT EXISTS links (
    source_note_id INTEGER REFERENCES notes(id),
    target_note_id INTEGER REFERENCES notes(id),
    PRIMARY KEY (source_note_id, target_note_id)
);
