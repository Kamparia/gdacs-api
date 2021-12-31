import json
import requests
import xmltodict


class GDACSAPIError(RuntimeError):
    pass


def handle_geojson(endpoint):
    res = requests.get(endpoint)
    if res.status_code != 200:
        raise GDACSAPIError("API Error: Unable to read GeoJSON data for GDACS event.")

    return json.loads(res.content)


def handle_xml(endpoint):
    res = requests.get(endpoint)
    if res.status_code != 200:
        raise GDACSAPIError("API Error: Unable to read XML data for GDACS event.")

    xml_parser = xmltodict.parse(res.content)
    content = xml_parser["rss"]["channel"]["item"]
    return json.loads(json.dumps(content))


def download_shp(endpoint):
    res = requests.get(endpoint, allow_redirects=True)
    if res.status_code != 200:
        raise GDACSAPIError("API Error: Unable to read SHP data for GDACS event.")

    try:
        shp_file_name = endpoint.split('/')[-1]
        with open(shp_file_name, 'wb') as download:
            download.write(res.content)
            return "Downloaded {} in directory.".format(shp_file_name)
    except Exception as error:
        raise error
