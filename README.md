# gdacs-api
Unofficial python library for working with [Global Disaster Alert and Coordination System (GDACS)](https://www.gdacs.org/) API.

## Setup
If you already have `pip` installed, use the commands below to install the `gdacs-api` python library.

From pypi.org:
```shell
(venv)$ pip install gdacs-api
```

From GitHub with pip:
```shell
(venv)$ pip install git+https://github.com/Kamparia/gdacs-api.git
```

From cloned GitHub repo for development:
```shell
(venv)$ git clone https://github.com/Kamparia/gdacs-api.git
(venv)$ cd ./gdacs-api
(venv)$ pip install -e .
```

The installation of `gdacs-api v.1.0.6` package depends on the following packages.
- Python >=3.6
- Requests >=2.10.0
- Xmltodict
- Cachetools

## Getting Started
### Import Library

To access the API functionalities of this libray, you need to import it into the Python script where it will be called.

```python
from gdacs.api import GDACSAPIReader
```

### Setup API Client

You need to setup an API client to interact with the GDACS API. You can do so by simply using the code snippet below.

```python
client = GDACSAPIReader()
```

### Get Latest Events

Use the code snippet below to retrieve latets disaster events from the [GDACS RSS Feed](https://www.gdacs.org/xml/rss.xml).

```python
events = client.latest_events() # all recent events
events = client.latest_events(limit=10) # 10 most events
```

You can also filter by event types or historical timeline. E.g. In the code snippet below, the first statement will return only Tropical Cyclone (TC) events that occured within the last 24 hours while the second statement will return Flooding (FL) events that occured within the last 7 days.

```python
tc_events = client.latest_events(event_type="TC", historical="24h")
fl_events = client.latest_events(event_type="FL", historical="7d")
```

Optional parameters:
- `event_type` (str): TC (Tropical Cyclones), EQ (Earthquakes), FL (Floods), VO (Volcanoes), WF (Wild Fires) and DR (Droughts)
- `historical` (str): 24h (Last 24 hours), 7d (Last 7 days)
- `limit` (int): returned events count.

### Get Single Event Record

The python library also supports the retrieval of single event with a known GDACS Event ID.

```python
event = client.get_event(event_type='TC', event_id='1000132')
```

To retrieve the record of a particular event episode, include `episode_id` in your code as shown below.

```python
event = client.get_event(event_type='TC', event_id='1000132', episode_id='8')
```

The library supports the retrieval of data in different formats provided by the GDACS API. The default source format for all retrievals is `xml` but you can also make use of `geojson` or `shp`.

```python
event = client.get_event(event_type='DR', event_id='1012428', episode_id='10', source_format='geojson')
```

Required parameters:
- `event_type` (str): TC (Tropical Cyclones), EQ (Earthquakes), FL (Floods), VO (Volcanoes), WF (Wild Fires) and DR (Droughts)
- `event_id` (str): GDACS Event ID

Optional parameters:
- `episode_id` (str): GDACS Event Episode ID
- `source_format` (str): xml, geojson or shp (Shapefile)
- `cap_file` (bool)

### Handling Errors

Invalid arguments or retrieval of missing records from the GDACS API may result in an error. You can catch them with `GDACSAPIError` which includes the error message returned.
```python
from gdacs.api import GDACSAPIError
try:
    # try to retrieve an invalid/missing event
    client.get_event(event_type='DR', event_id='1012428', source_format='geojson')
except GDACSAPIError as error:
    print(error)
```

### Testing

The project uses `unittest` (Python inbuilt testing library) to run its suite of unit tests.
```shell
(venv)$ cd ./gdacs/tests
(venv)$ python -m unittest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) for details.