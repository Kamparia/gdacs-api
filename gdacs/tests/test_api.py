from unittest import TestCase
from gdacs.api import GDACSAPIReader, GDACSAPIError


class TestGDACSAPI(TestCase):
    def setUp(self):
        self.client = GDACSAPIReader()

    def test_latest_events_no_args(self):
        '''Test latest_events() without any arguments.'''
        events = self.client.latest_events()
        self.assertTrue(events) if len(events) > 0 else self.assertFalse(events)

    def test_latest_events_limit(self):
        ''' Test latest_events() set limit for returned events. '''
        limit = 5
        events = self.client.latest_events(limit=limit)
        self.assertEqual(len(events), limit)

    def test_latest_events_historical(self):
        ''' Test latest_events() with historical arguments. '''
        day_events = self.client.latest_events(historical='24h') # 24 hours
        self.assertTrue(day_events) if len(day_events) > 0 else self.assertFalse(day_events)

        week_events = self.client.latest_events(historical='7d') # 7 days
        self.assertTrue(week_events) if len(week_events) > 0 else self.assertFalse(week_events)

    def test_latest_events_event_types(self):
        ''' Test latest_events() filter by event_types argument. '''
        tc_events = self.client.latest_events(event_type="TC") # tropical cyclones
        self.assertTrue(tc_events) if len(tc_events) > 0 else self.assertFalse(tc_events)

        eq_events = self.client.latest_events(event_type="EQ") # earthquakes
        self.assertTrue(eq_events) if len(eq_events) > 0 else self.assertFalse(eq_events)

        fl_events = self.client.latest_events(event_type="FL") # floods
        self.assertTrue(fl_events) if len(fl_events) > 0 else self.assertFalse(fl_events)

        dr_events = self.client.latest_events(event_type="DR") # droughts
        self.assertTrue(dr_events) if len(dr_events) > 0 else self.assertFalse(dr_events)

        wf_events = self.client.latest_events(event_type="WF") # wild fires
        self.assertTrue(wf_events) if len(wf_events) > 0 else self.assertFalse(wf_events)

        vo_events = self.client.latest_events(event_type="VO") # volcanoes
        self.assertTrue(vo_events) if len(vo_events) > 0 else self.assertFalse(vo_events)
    
    def test_latest_events_multiple_args(self):
        ''' Test latest_events() with multiple argumnets defined. '''
        events = self.client.latest_events(event_type="TC", historical='24h', limit=5)
        self.assertTrue(events) if len(events) > 0 else self.assertFalse(events)
        self.assertEqual(len(events), 5) if len(events) >= 5 else self.assertTrue(events)

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
            self.client.get_event(event_type='TC', event_id='1000132', episode_id='8', source_format='shp'), 
            'Downloaded Shape_1000132_8.zip in directory.'
        ) # shapefile

    def test_exception_errors(self):
        ''' Testing for exceptions and errors '''
        with self.assertRaises(GDACSAPIError): # missing event record
            self.client.get_event(event_type='DR', event_id='1012428', source_format='geojson')

        with self.assertRaises(GDACSAPIError): # invalid argument
            self.client.get_event(event_type='DH', event_id='1012428', source_format='geojson') # no event type of DH