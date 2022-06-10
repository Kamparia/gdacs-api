from unittest import TestCase

from gdacs.api import GDACSAPIReader, GDACSAPIError
from gdacs.utils import delete_downloads


class TestGDACSAPI(TestCase):
    def setUp(self):
        self.client = GDACSAPIReader()

    def tearDown(self):
        self.client = None
        delete_downloads()

    def test_latest_events_no_args(self):
        '''Test latest_events() without any arguments.'''
        events = self.client.latest_events()
        self.assertTrue(events) if len(events) > 0 else self.assertFalse(events)

    def test_latest_events_limit(self):
        ''' Test latest_events() set limit for returned events. '''
        limit = 5
        events = self.client.latest_events(limit=limit)
        self.assertEqual(len(events), limit)

    def test_latest_events_event_types(self):
        ''' Test latest_events() filter by event_types argument. '''
        for event_type in ["TC", "EQ", "FL", "DR", "WF", "VO"]:
            events = self.client.latest_events(event_type=event_type) 
            self.assertTrue(events) if len(events) > 0 else self.assertFalse(events)
    
    def test_latest_events_multiple_args(self):
        ''' Test latest_events() with multiple argumnets defined. '''
        events = self.client.latest_events(event_type="EQ", limit=5)
        self.assertTrue(events) if len(events) > 0 else self.assertFalse(events)
        self.assertEqual(len(events), 5) if len(events) == 5 else self.assertFalse(events)

    def test_get_event_for_different_events(self):
        self.assertTrue(
            self.client.get_event(event_type='TC', event_id='1000132')
        )  # xml event without episode_id

        self.assertTrue(
            self.client.get_event(event_type='TC', event_id='1000132', episode_id='8')
        )  # xml event with episode id

        self.assertTrue(
            self.client.get_event(event_type='DR', event_id='1012428', episode_id='10', source_format='geojson')
        )  # geojson
        
        self.assertEqual(
            self.client.get_event(event_type='TC', event_id='1000132', episode_id='8', source_format='shp'), 
            'Downloaded Shape_1000132_8.zip in directory.'
        )  # shapefile

    def test_exception_errors(self):
        ''' Testing for exceptions and errors '''
        with self.assertRaises(GDACSAPIError): # missing event record
            self.client.get_event(event_type='DR', event_id='1012428', source_format='geojson')

        with self.assertRaises(GDACSAPIError): # invalid argument
            self.client.get_event(event_type='DH', event_id='1012428', source_format='geojson')  # no event type of DH