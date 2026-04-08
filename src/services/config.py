from pathlib import Path
import tomllib

config_data = None

def get_config():
    global config_data
    if config_data is None:
        config_data = Config()
    return config_data

class Default():
    # Directories
    CONFIG_DIR  = Path.home() / '.config' / 'yaki'
    DATA_DIR    = Path.home() / '.local' / 'share' / 'yaki'
    PLUGINS_DIR = CONFIG_DIR / 'plugins'
    NOTES_DIR  = DATA_DIR / 'notes'
    # Paths
    CONFIG_PATH = CONFIG_DIR / 'config.toml'
    DB_PATH     = DATA_DIR / 'yaki.db'
    SCHEMA_PATH = Path(__file__).parent.parent / 'data' / 'schema.sql'

class Config():
    def __init__(self):
        self.config = None

        self.read_config()

    def set_defaults(self):
        self.config = {
            'dirs': {
                'config_dir':  str(Default.CONFIG_DIR),
                'data_dir':    str(Default.DATA_DIR),
                'plugins_dir': str(Default.PLUGINS_DIR),
                'notes_dir':   str(Default.NOTES_DIR)
            },
            'paths': {
                'config_path': str(Default.CONFIG_PATH),
                'db_path':     str(Default.DB_PATH),
                'schema_path': str(Default.SCHEMA_PATH)
            },
            'indexer': {
                'ignore_relative_dirs': []
            }
        }

    def assign_key_values(self, root_key, target_dict: dict):
        for key, value in target_dict.items():
            # No recursion here, defaults should only nest one layer
            self.config[root_key][key] = value

    def read_config(self):
        self.set_defaults()

        file_path = Default.CONFIG_PATH

        if not file_path.exists():
            # TODO: Provide verbosity that config file doesn't exist
            return

        with open(file_path, 'rb') as file:
            config_dict = tomllib.load(file)

        for key, value in config_dict.items():
            if type(value) == dict:
                self.assign_key_values(key, value)
            else:
                self.config[key] = value

    def ensure_dir_created(self, target_dir: Path): # TODO: move to utils.py
        # TODO: add try except here
        target_dir = Path(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)

    def get_dir(self, target_dir_key, not_exists_ok=False, mkdir=False):
        # TODO: I don't know if this belongs in config?

        if target_dir_key not in self.config['dirs'].keys():
            # TODO: more useful error message
            raise KeyError(target_dir_key)

        target_dir = Path(self.config['dirs'][target_dir_key])

        if not target_dir.exists() and not not_exists_ok:
            raise FileNotFoundError(target_dir)

        if mkdir:
            self.ensure_dir_created(target_dir)

        return target_dir

    def get_path(self, target_path_key, not_exists_ok=False, mkdir=False):
        # TODO: I don't know if this belongs in config?

        if target_path_key not in self.config['paths'].keys():
            # TODO: more useful error message
            raise KeyError(target_path_key)

        target_path = Path(self.config['paths'][target_path_key])

        if not target_path.exists() and not not_exists_ok:
            raise FileNotFoundError(target_path)

        if mkdir:
            self.ensure_path_created(target_path.parent)

        return target_path

    def get(self, root_key, key):
        if root_key not in self.config.keys():
            raise KeyError(root_key)

        if key is not None and type(self.config[root_key]) != dict:
            raise KeyError(root_key)

        if key not in self.config[root_key].keys():
            raise KeyError(root_key)

        return self.config[root_key][key]

