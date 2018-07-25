from ott.utils import db_utils
from ott.utils import object_utils
from ott.gtfsdb_realtime.model.database import Database

# TODO: move these to Database()  ?

def get_session(url, schema=None, is_geospatial=False, create=False):
    session = Database.make_session(url, schema, is_geospatial, create)
    return session


def get_session_via_cmdline(args):
    url = db_utils.check_localhost(args.database_url)
    return get_session(url, args.schema, args.is_geospatial, args.create)


def get_session_via_config(config):
    return make_db_via_config(config).get_session()


def make_db_via_config(config):
    u = object_utils.safe_dict_val(config, 'sqlalchemy.url')
    s = object_utils.safe_dict_val(config, 'sqlalchemy.schema')
    g = object_utils.safe_dict_val(config, 'sqlalchemy.is_geospatial', False)
    db = Database(u, s, g)
    return db
