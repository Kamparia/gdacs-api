import json
import requests
from os.path import join
from cachetools import cached, TTLCache

from gdacs.schemas import GeoJSON
from gdacs.utils import *


CACHE_TTL = 300  # secs
EVENT_TYPES = [None, 'TC', 'EQ', 'FL', 'VO', 'DR', 'WF']
DATA_FORMATS = [None, 'xml', 'geojson', 'shp']
LATEST_EVENTS_URL = 'https://www.gdacs.org/gdacsapi/api/events/geteventlist/EVENTS4APP'
BASE_URL = "https://www.gdacs.org/datareport/resources"


class GDACSAPIReader:
    def __init__(self):
        pass

    def __repr__(self) -> str:
        return "GDACS API Client."

    @cached(cache=TTLCache(maxsize=500, ttl=CACHE_TTL))
    def latest_events(self,
                      event_type: str = None,
                      limit: int = None
                      ):
        """ Get latest events from GDACS RSS feed. """
        if event_type not in EVENT_TYPES:
            raise GDACSAPIError("API Error: Used an invalid `event_type` parameter in request.")

        res = requests.get(LATEST_EVENTS_URL)
        if res.status_code != 200:
            raise GDACSAPIError("API Error: GDACS RSS feed can not be reached.")

        events = [
            event for event in res.json()['features']
            if event_type in [None, event['properties']['eventtype']]
        ]
        features = json.loads(json.dumps(events[:limit]))
        return GeoJSON(features=features)

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
            return self.__get_geojson_event(event_type, event_id, episode_id)
        elif source_format == 'shp':
            return self.__get_shp_event(event_type, event_id, episode_id)
        else:
            return self.__get_xml_event(event_type, event_id, episode_id, cap_file)

    def __get_geojson_event(self, event_type: str, event_id: str, episode_id: str = None):
        file_name = f"geojson_{event_id}_{episode_id}.geojson"
        geojson_path = join(BASE_URL, event_type, event_id, file_name).replace("\\", "/")
        return handle_geojson(geojson_path)        

    def __get_shp_event(self, event_type: str, event_id: str, episode_id: str = None):
        file_name = f"Shape_{event_id}_{episode_id}.zip"
        shp_path = join(BASE_URL, event_type, event_id, file_name).replace("\\", "/")
        return download_shp(shp_path)

    def __get_xml_event(self, event_type: str, event_id: str, episode_id: str = None, cap_file: bool = False):
        if cap_file:
            file_name = f"cap_{event_id}.xml"
        elif not episode_id:
            file_name = f"rss_{event_id}.xml"
        else:
            file_name = f"rss_{event_id}_{episode_id}.xml"

        xml_path = join(BASE_URL, event_type, event_id, file_name).replace("\\", "/")
        return handle_xml(xml_path)