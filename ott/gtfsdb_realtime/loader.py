from ott.gtfsdb_realtime.model.database import Database
from ott.gtfsdb_realtime.model.base import Base

from ott.utils.parse.cmdline import db_cmdline

import logging
logging.basicConfig()
log = logging.getLogger(__file__)


def parse(session, agency_id, feed_url, clear_first=False):
    from google.transit import gtfs_realtime_pb2
    import urllib

    ret_val = True
    log.warn("agency: {} ... feed url: {}".format(agency_id, feed_url))
    feed = gtfs_realtime_pb2.FeedMessage()
    response = urllib.urlopen(feed_url)
    feed.ParseFromString(response.read())
    feed_type = Base.get_feed_type(feed)
    if feed_type:
        if clear_first:
            feed_type.clear_tables(session, agency_id)
        feed_type.parse_gtfsrt_feed(session, agency_id, feed)
        ret_val = True
    else:
        log.warn("not sure what type of data we've got")
        ret_val = False
    return ret_val


def make_session(url, schema, is_geospatial=False, create_db=False):
    return Database.make_session(url, schema, is_geospatial, create_db)


def load_agency_data(session, agency_id, trips_url, alerts_url, vehicles_url):
    ret_val = True

    if trips_url:
        r = parse(session, agency_id, trips_url)
        if not r:
            ret_val = False

    if alerts_url:
        r = parse(session, agency_id, alerts_url)
        if not r:
            ret_val = False

    if vehicles_url:
        r = parse(session, agency_id, vehicles_url)
        if not r:
            ret_val = False

    return ret_val


def main():
    cmdline = db_cmdline.gtfsdb_parser()
    args = cmdline.parse_args()
    print args

    session = Database.make_session(args.database_url, args.schema, args.geo, args.create)

    url = 'http://trimet.org/transweb/ws/V1/FeedSpecAlerts/appId/3819A6A38C72223198B560DF0/includeFuture/true'
    url = 'http://trimet.org/transweb/ws/V1/TripUpdate/appId/3819A6A38C72223198B560DF0/includeFuture/true'
    #url = 'http://developer.trimet.org/ws/gtfs/VehiclePositions/appId/3819A6A38C72223198B560DF0'
    if args.url and len(args.url) > 1:
        url = args.url
    parse(session, args.agency, url, args.clear)


if __name__ == '__main__':
    main()

