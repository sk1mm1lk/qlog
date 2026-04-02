CREATE SEQUENCE IF NOT EXISTS notes_id_seq START 1;

CREATE TABLE IF NOT EXISTS notes (
    id                    INTEGER PRIMARY KEY DEFAULT nextval('notes_id_seq'),
    title                 VARCHAR NOT NULL,
    project_title         VARCHAR NOT NULL,
    relative_file_path    VARCHAR NOT NULL,
    status                VARCHAR DEFAULT 'draft',
    visibility            VARCHAR DEFAULT 'private',
    retention_period_days INTEGER DEFAULT 0,
    last_confirmed_at     TIMESTAMP,
    file_hash             BLOB NOT NULL,
    hash_algorithm        VARCHAR NOT NULL,
    created_at            TIMESTAMP,
    modified_at           TIMESTAMP
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

CREATE TABLE IF NOT EXISTS projects (
    title           VARCHAR PRIMARY KEY,
    root_file_path  VARCHAR NOT NULL,
    system          VARCHAR NOT NULL
);
