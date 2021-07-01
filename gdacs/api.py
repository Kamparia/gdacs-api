import json
import requests
import xmltodict
from cachetools import cached, TTLCache

CACHE_TTL = 300 # 5minutes
EVENT_TYPES = ['TC', 'EQ', 'FL', 'VO', 'DR', 'WF']
DATA_FORMATS = ['xml', 'geojson', 'shp']
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
    def latest_events(self, event_type:str=None, historical:str='default', limit:int=None):
        """ Get latest events from GDACS RSS feed. """
        if event_type not in EVENT_TYPES:
            raise GDACSAPIError("API Error: Used an invalid `event_type` parameter in request.")

        if historical not in RSS_FEED_URLS.keys():
            raise GDACSAPIError("API Error: Used an invalid `historical` parameter in request.")
            
        res = requests.get(RSS_FEED_URLS[historical])
        if res.status_code == 200:
            events = []
            xml_parser = xmltodict.parse(res.content)
            for item in xml_parser["rss"]["channel"]["item"]:
                # filter by event type
                if event_type != None and event_type != item["gdacs:eventtype"]:
                    continue
                
                events.append(item)
            return json.dumps(events[:limit])
        else:
            raise GDACSAPIError("API Error: GDACS RSS feed can not be reached.")

    @cached(cache=TTLCache(maxsize=500, ttl=CACHE_TTL))
    def get_event(self, event_type: str, event_id: str, episode_id: str=None, source_format: str='xml', cap_file: bool=False):
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

        def download_shp(endpoint):
            res = requests.get(endpoint, allow_redirects=True)
            if  res.status_code == 200:
                try:
                    shp_file_name = endpoint.split('/')[-1]
                    with open(shp_file_name, 'wb') as download:
                        download.write(res.content)
                        return f"Downloaded {shp_file_name} in directory."
                except Exception as error:
                    raise error
            else:
                raise GDACSAPIError("API Error: Unable to read SHP/KML data for GDACS event.")
        
        if event_type not in EVENT_TYPES:
            raise GDACSAPIError("API Error: Used an invalid `event_type` parameter in request.")

        if source_format not in DATA_FORMATS:
            raise GDACSAPIError("API Error: Used an invalid `data_format` parameter in request.")

        if source_format == 'geojson':
            return handle_geojson(f"{BASE_URL}/{event_type}/{event_id}/geojson_{event_id}_{episode_id}.geojson")
        elif source_format == 'shp':
            return download_shp(f"{BASE_URL}/{event_type}/{event_id}/Shape_{event_id}_{episode_id}.zip")
        else:
            if cap_file == True:
                return handle_xml(f"{BASE_URL}/{event_type}/{event_id}/cap_{event_id}.xml")
            elif episode_id == None:
                return handle_xml(f"{BASE_URL}/{event_type}/{event_id}/rss_{event_id}.xml")
            else:
                return handle_xml(f"{BASE_URL}/{event_type}/{event_id}/rss_{event_id}_{episode_id}.xml")


class GDACSAPIError(RuntimeError):
    pass