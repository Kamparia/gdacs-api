from unittest import TestCase
from ..api import GDACSAPIReader, GDACSAPIError


class TestGDACSAPI(TestCase):
    def setUp(self):
        self.client = GDACSAPIReader()

    def test_latest_events_filter_by_event_types(self):
        self.client.latest_events(event_type="TC") # tropical cyclones
        self.client.latest_events(event_type="EQ") # earthquakes
        self.client.latest_events(event_type="VO") # volcanoes
        self.client.latest_events(event_type="DR") # droughts
        self.client.latest_events(event_type="FL") # floods
        self.client.latest_events(event_type="WF") # wild fires

    def test_get_event_for_different_events(self):
        self.client.get_event(event_type='TC', event_id='1000132', episode_id='8')
        self.client.get_event(event_type='DR', event_id='1012428', episode_id='10', data_format='geojson')

    def test_get_event_for_invalid_record(self):
        with self.assertRaises(GDACSAPIError):
            self.client.get_event(event_type='EQ', event_id='1000ACS')