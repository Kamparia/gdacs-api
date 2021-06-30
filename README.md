# gdacs-api
Unofficial python library for working with [Global Disaster Alert and Coordination System (GDACS)](https://www.gdacs.org/) API.

## Setup
Use the command below to install the `gdacs-api` python library.

```
pip install gdacs-api
```

## Getting Started
### Import Library

To access the API functionalities of this libray, you need to import it into the Python script where it will be called.

```
from gdacs import GDACSAPIReader
```

### Setup API Client

You need to setup an API client to interact with the GDACS API. You can do so by simply using the code snippet below.

```
client = GDACSAPIReader()
```

### Get Latest Events

Use the code snippet below to retrieve latets disaster events from the GDACS API.

```
events = client.latest_events()
```

You can also filter by event types or historical timeline. E.g. In the code snippet below, the first statement will return only Tropical Cyclone (TC) events that occured within the last 24 hours while the second statement will return Flooding (FL) events that occured within the last 7 days.

```
tc_events = client.latest_events(event_type="TC", historical="24h")
fl_events = client.latest_events(event_type="FL", historical="7d")
```

Optional parameters:
- `event_type` (str): Tropical Cyclones (`TC`), Earthquakes (`EQ`), Floods (`FL`), Volcanoes (`VO`), Wild Fires (`WF`) and Droughts (`DR`).
- `historical` (str): Last 24 hours (`24h`), Last 7 days (`7d`).

### Get Single Event Record

The python library also supports the retrieval of single event with a known GDACS Event ID.

```
event = client.get_event(event_type='TC', event_id='1000132')
```

To retrieve the record of a particular event episode, include `episode_id` in your code as shown below.

```
event = client.get_event(event_type='TC', event_id='1000132', episode_id='8')
```

The library supports the retrieval of data in different formats provided by the GDACS API. The default source format for all retrievals is `xml` but you can also make use of `geojson` or `shp`.

```
event = client.get_event(event_type='DR', event_id='1012428', episode_id='10', source_format='geojson')
```

Required parameters:
- `event_type` (str): Tropical Cyclones (`TC`), Earthquakes (`EQ`), Floods (`FL`), Volcanoes (`VO`), Wild Fires (`WF`) and Droughts (`DR`)
- `event_id` (str): GDACS Event ID

Optional parameters:
- `episode_id` (str): GDACS Event Episode ID
- `source_format` (str): XML (`xml`), GeoJSON (`geojson`) or Shapefile (`shp`)
- `cap_file` (bool)

### Handling Errors

Invalid arguments or retrieval of missing records from the GDACS API may result in an error. You can catch them with `GDACSAPIError` which includes the error message returned.
```
from gdacs import GDACSAPIError
try:
    # try to retrieve an invalid/missing event
    client.get_event(event_type='DR', event_id='1012428', source_format='geojson')
except GDACSAPIError as error:
    print(error)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) for details.