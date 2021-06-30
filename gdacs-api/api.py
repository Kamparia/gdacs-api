import json
import requests
import xmltodict
from cachetools import cached, TTLCache

CACHE_TTL = 300 # 5minutes
DATA_FORMATS = ['xml', 'geojson']
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

    @cached(cache=TTLCache(maxsize=50000, ttl=CACHE_TTL))
    def latest_events(self, event_type:str=None, historical:str='default'):
        """ Get latest events from GDACS RSS feed. """
        if historical in RSS_FEED_URLS.keys():
            res = requests.get(RSS_FEED_URLS[historical])
            if res.status_code == 200:
                events = []
                xml_parser = xmltodict.parse(res.content)
                for item in xml_parser["rss"]["channel"]["item"]:
                    # filter by event type
                    if event_type != None and event_type != item["gdacs:eventtype"]:
                        continue
                    
                    events.append(item)
                return json.dumps(events)
            else:
                raise GDACSAPIError("API Error: GDACS RSS feed can not be reached.")
        else:
            raise GDACSAPIError("API Error: Used an invalid `historical` parameter in request.")

    @cached(cache=TTLCache(maxsize=50000, ttl=CACHE_TTL))
    def get_event(self, event_type: str, event_id: str, episode_id: str=None, data_format: str='xml'):
        """ Get record of a single event from GDACS API. """
        def handle_geojson(endpoint):
            res = requests.get(endpoint)
            if  res.status_code == 200:
                return json.dumps(json.loads(res.content))
            else:
                raise GDACSAPIError("API Error: Unable to read GeoJSON data for GDACS event.")

        def handle_xml(endpoint):
            res = requests.get(endpoint)
            if  res.status_code == 200:
                xml_parser = xmltodict.parse(res.content)
                content = xml_parser["rss"]["channel"]["item"]
                return json.dumps(content)
            else:
                raise GDACSAPIError("API Error: Unable to read XML data for GDACS event.")
        
        if data_format in DATA_FORMATS:
            if data_format == 'geojson':
                return handle_geojson(f"{BASE_URL}/{event_type}/{event_id}/geojson_{event_id}_{episode_id}.geojson")
            else:
                if episode_id == None:
                    return handle_xml(f"{BASE_URL}/{event_type}/{event_id}/rss_{event_id}.xml")
                else:
                    return handle_xml(f"{BASE_URL}/{event_type}/{event_id}/rss_{event_id}_{episode_id}.xml")
        else:
            raise GDACSAPIError("API Error: Used an invalid `data_format` parameter in request.")


class GDACSAPIError(RuntimeError):
    pass