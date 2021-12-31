from unittest import TestCase

from gdacs.utils import GDACSAPIError, handle_geojson
from gdacs.utils import handle_xml, download_shp


class TestUtils(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        # delete temporary files
        pass

    def test_handle_geojson(self):
        """
        Test the handle_geojson function with valid geojson url
        :return:
        """
        data = handle_geojson('https://www.gdacs.org/datareport/resources/TC/1000194/geojson_1000194_1.geojson')
        self.assertIsInstance(data, dict)
        self.assertEqual(data['type'], 'FeatureCollection')

    def test_handle_geojson_error(self):
        """
        Test the handle_geojson function with invalid geojson url
        :return:
        """
        url = 'https://www.gdacs.org/datareport/resources/TC/1000194/geojson_1000194_41.geojson'
        with self.assertRaises(GDACSAPIError):
            handle_geojson(url)

    def test_handle_xml(self):
        """
        Test the handle_xml function with valid xml url
        :return:
        """
        data = handle_xml('https://www.gdacs.org/datareport/resources/TC/1000194/rss_1000194_20.xml')
        self.assertIsInstance(data, dict)

    def test_handle_xml_error(self):
        """
        Test the handle_xml function with invalid xml url
        :return:
        """
        url = 'https://www.gdacs.org/datareport/resources/TC/1000194/rss_1000194_41.xml'
        with self.assertRaises(GDACSAPIError):
            handle_xml(url)

    def test_download_shp(self):
        """
        Test the download_shp function with valid shp url
        :return:
        """
        data = download_shp('https://www.gdacs.org/datareport/resources/TC/1000194/Shape_1000194_20.zip')
        self.assertEqual(data, "Downloaded Shape_1000194_20.zip in directory.")

    def test_download_shp_error(self):
        """
        Test the download_shp function with invalid shp url
        :return:
        """
        url = 'https://www.gdacs.org/datareport/resources/TC/1000194/Shape_1000194_41.zip'
        with self.assertRaises(GDACSAPIError):
            download_shp(url)
