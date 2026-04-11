from pathlib import Path
from services import database, config
import os
import yaml
import tomllib

config = config.get_config()

def parse_str_value(value: str):
    return value

def parse_list_value(value: list):
    return ','.join(value)

def parse_dict_value(value: dict):
    return str(value)

def parse_frontmatter(id, frontmatter, frontmatter_format):
    frontmatter_dict = {}

    if frontmatter_format == 'yaml':
        try:
            frontmatter_dict = yaml.safe_load(frontmatter)
        except yaml.YAMLError:
            print(f'Failed to parse note #{id}')
    elif frontmatter_format == 'toml':
        frontmatter_dict = tomllib.loads(frontmatter)

    # TODO: parse dict
    notes_keys = [
        'namespace',
        'status',
        'visibility'
    ]

    notes_query = 'UPDATE notes SET '
    notes_params = []

    value_type_conversion = {
        str: parse_str_value,
        list: parse_list_value,
        dict: parse_dict_value
    }

    value_type_str = {
        str: 'str',
        list: 'list',
        dict: 'dict'
    }

    notes_key_value = []

    for key, value in frontmatter_dict.items():
        if key in notes_keys:
            # Notes params
            notes_query += f'{key} = ?,'
            notes_params.append(value)
        else:
            # Tags
            converted_func = value_type_conversion.get(type(value))

            if converted_func:
                key_value = {
                    'note_id': id,
                    'key': key,
                    'value': converted_func(value),
                    'value_type': value_type_str.get(type(value))
                }
                notes_key_value.append(key_value)

    db = database.get_db()

    # Notes params
    if len(notes_params) > 0:
        notes_query.strip(',')
        notes_query += ' WHERE id = ?'
        notes_params.append(id)

        db.execute(notes_query, notes_params)

    if len(notes_key_value) > 0:
        for key_value in notes_key_value:
            query = f"INSERT INTO notes_key_value (note_id, note_key, note_value, value_type) VALUES (?, ?, ?, ?)"
            note_id = key_value['note_id']
            key = key_value['key']
            value = key_value['value']
            value_type = key_value['value_type']
            db.execute(query, [note_id, key, value, value_type])

def parse_links(source_note_id, links):
    db = database.get_db()

    check_exists_query = """
        SELECT * FROM links
        WHERE source_note_id = ?
        AND target_note_id = ?
    """
    query = """
        INSERT INTO links (
            source_note_id,
            target_note_id
        ) VALUES (?, ?)
    """

    for link in links:
        get_id_query = """
            SELECT
                id
            FROM notes
            WHERE title = ?
        """
        rows = db.execute(get_id_query, [link]).fetchall()

        for row in rows:
            target_note_id = row[0]
            params = [source_note_id, target_note_id]
            if not db.execute(check_exists_query, params).fetchall():
                db.execute(query, params)

    db.close()

def parse_dir(target_dir: Path, rebuild: bool, is_parse_frontmatter: bool, is_parse_links: bool):
    target_dir = target_dir.expanduser()

    if not target_dir.is_dir():
        raise FileNotFoundError(target_dir)

    if rebuild:
        database.truncate('notes_key_value')
        database.truncate('links')

    # TODO: need to handle non rebuild logic

    db = database.get_db()

    query = """
        SELECT
            id,
            relative_file_path
        FROM notes
    """

    notes = db.execute(query).fetchall()
    breaks = {
        '---': 'yaml',
        '+++': 'toml'
        # '```yaki': 'yaki', # For future in note code block
        # '```': 'code'
    }

    for id, relative_file_path in notes:
        file_path = target_dir / relative_file_path

        with open(file_path, 'r') as file:
            first_line = True
            in_frontmatter = False

            frontmatter_lines = []
            frontmatter_format = ''
            links = []

            for line in file:
                stripped_line = line.strip()
                no_whitespace_line = stripped_line.replace(' ', '')
                break_type = breaks.get(no_whitespace_line)

                # Fontmatter
                if is_parse_frontmatter:
                    if in_frontmatter:
                        if break_type:
                            in_frontmatter = False
                        else:
                            frontmatter_lines.append(line)

                    if first_line and break_type:
                        in_frontmatter = True
                        frontmatter_format = break_type

                # TODO: handle link processing and frontmatter processing
                #       as separate functions and exclude link processing
                #       from code blocks

                # Links
                if is_parse_links:
                    if not in_frontmatter:
                        in_link = False
                        first_link_char = False
                        last_link_char = False

                        temp_links = []

                        for char in list(stripped_line):
                            if char == '[':
                                if first_link_char:
                                    first_link_char = False
                                    in_link = True
                                    temp_links.append('')
                                else:
                                    # TODO: doesn't handle nested [[ text [[ text ]] ]] cases
                                    first_link_char = True
                            elif char == ']':
                                if last_link_char:
                                    last_link_char = False
                                    in_link = False
                                else:
                                    last_link_char = True
                            else:
                                if first_link_char:
                                    first_link_char = False
                                elif in_link:
                                    temp_links[-1] = temp_links[-1] + char

                        if in_link:
                            temp_links.pop()

                        for link in temp_links:
                            link = link.strip()

                            if len(link) != 0 and ' ' not in link:
                                links.append(link)

                first_line = False

            if in_frontmatter:
                # If frontmatter never ended, don't accept
                frontmatter_lines = []

            if len(frontmatter_lines) > 0 and is_parse_frontmatter:
                frontmatter = ''.join(frontmatter_lines)
                parse_frontmatter(id, frontmatter, frontmatter_format)

            if len(links) > 0 and is_parse_links:
                parse_links(id, links)
