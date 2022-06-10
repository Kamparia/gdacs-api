from unittest import TestCase
from gdacs.schemas import *


class TestSchemas(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass
    
    def test_geojson(self):
        """
        Test the GeoJSON class
        :return:
        """
        data = GeoJSON(type="FeatureCollection", features=[])
        self.assertIsInstance(data, GeoJSON)
        self.assertEqual(data.type, "FeatureCollection")
        self.assertEqual(type(data.features), list)
        self.assertEqual(len(data), 0)

    def test_feature(self):
        """
        Test the Feature class
        :return:
        """
        data = Feature(type="Feature", properties={}, geometry={}, bbox=[])
        self.assertIsInstance(data, Feature)
        self.assertEqual(data.type, "Feature")
        self.assertEqual(data.properties, {})
        self.assertEqual(data.geometry, {})
        self.assertEqual(data.bbox, [])
