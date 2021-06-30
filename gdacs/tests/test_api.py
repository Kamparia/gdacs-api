from unittest import TestCase
from gdacs.api import GDACSAPIReader, GDACSAPIError


class TestGDACSAPI(TestCase):
    def setUp(self):
        self.client = GDACSAPIReader()

    def test_latest_events_filter_by_event_types(self):
        self.assertTrue(self.client.latest_events(event_type="TC")) # tropical cyclones
        self.assertTrue(self.client.latest_events(event_type="EQ")) # earthquakes
        self.assertTrue(self.client.latest_events(event_type="VO")) # volcanoes
        self.assertTrue(self.client.latest_events(event_type="DR")) # droughts
        self.assertTrue(self.client.latest_events(event_type="FL")) # floods
        self.assertTrue(self.client.latest_events(event_type="WF")) # wild fires

    def test_get_event_for_different_events(self):
        self.assertTrue(
            self.client.get_event(event_type='TC', event_id='1000132')
        ) # xml event without episode_id

        self.assertTrue(
            self.client.get_event(event_type='TC', event_id='1000132', episode_id='8')
        ) # xml event with episode id

        self.assertTrue(
            self.client.get_event(event_type='DR', event_id='1012428', episode_id='10', source_format='geojson')
        ) # geojson

        self.assertEqual(
            self.client.get_event(event_type='DR', event_id='1012428', episode_id='10', source_format='shp'), 
            'Downloaded Shape_1012428_10.zip in directory.'
        ) # shapefile

    def test_get_event_for_invalid_record(self):
        with self.assertRaises(GDACSAPIError):
            self.client.get_event(event_type='EQ', event_id='1000ACS')