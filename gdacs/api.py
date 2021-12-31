import json
import requests
import xmltodict
from os.path import join
from cachetools import cached, TTLCache

from gdacs.utils import GDACSAPIError
from gdacs.utils import handle_xml, handle_geojson
from gdacs.utils import download_shp


CACHE_TTL = 300  # 5minutes
EVENT_TYPES = [None, 'TC', 'EQ', 'FL', 'VO', 'DR', 'WF']
DATA_FORMATS = [None, 'xml', 'geojson', 'shp']
BASE_URL = "https://www.gdacs.org/datareport/resources"
RSS_FEED_URLS = {
    "default": "https://www.gdacs.org/xml/rss.xml",
    "24h": "https://www.gdacs.org/xml/rss_24h.xml",
    "7d": "https://www.gdacs.org/xml/rss_7d.xml"
}


class GDACSAPIReader:
    def __init__(self):
        pass

    def __repr__(self) -> str:
        return "GDACS API Client."

    @cached(cache=TTLCache(maxsize=500, ttl=CACHE_TTL))
    def latest_events(self,
                      event_type: str = None,
                      historical: str = 'default',
                      limit: int = None
                      ):
        """ Get latest events from GDACS RSS feed. """
        if event_type not in EVENT_TYPES:
            raise GDACSAPIError("API Error: Used an invalid `event_type` parameter in request.")

        if historical not in RSS_FEED_URLS.keys():
            raise GDACSAPIError("API Error: Used an invalid `historical` parameter in request.")

        res = requests.get(RSS_FEED_URLS[historical])
        if res.status_code != 200:
            raise GDACSAPIError("API Error: GDACS RSS feed can not be reached.")

        xml_parser = xmltodict.parse(res.content)
        events = [
            item
            for item in xml_parser["rss"]["channel"]["item"]
            if event_type in [None, item["gdacs:eventtype"]]
        ]

        return json.loads(json.dumps(events[:limit]))

    @cached(cache=TTLCache(maxsize=500, ttl=CACHE_TTL))
    def get_event(self,
                  event_id: str,
                  event_type: str = None,
                  episode_id: str = None,
                  source_format: str = None,
                  cap_file: bool = False
                  ):
        """ Get record of a single event from GDACS API. """
        if event_type not in EVENT_TYPES:
            raise GDACSAPIError("API Error: Used an invalid `event_type` parameter in request.")

        if source_format not in DATA_FORMATS:
            raise GDACSAPIError("API Error: Used an invalid `data_format` parameter in request.")

        if source_format == 'geojson':
            file_name = "geojson_{}_{}.geojson".format(event_id, episode_id)
            geojson_path = join(BASE_URL, event_type, event_id, file_name).replace("\\", "/")
            return handle_geojson(geojson_path)

        elif source_format == 'shp':
            file_name = "Shape_{}_{}.zip".format(event_id, episode_id)
            shp_path = join(BASE_URL, event_type, event_id, file_name).replace("\\", "/")
            return download_shp(shp_path)

        else:
            if cap_file:
                file_name = "cap_{}.xml".format(event_id)
            elif not episode_id:
                file_name = "rss_{}.xml".format(event_id)
            else:
                file_name = "rss_{}_{}.xml".format(event_id, episode_id)

            xml_path = join(BASE_URL, event_type, event_id, file_name).replace("\\", "/")
            return handle_xml(xml_path)
