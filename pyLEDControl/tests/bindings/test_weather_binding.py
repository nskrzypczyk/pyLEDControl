import unittest

from bindings.weather_binding import WeatherBinding, _get_all_weather_icons
from misc.logging import Log


class TestWeatherBinding(unittest.TestCase):
    def setUp(self) -> None:
        self.weather_binding = WeatherBinding()

    def test_response(self):
        res = self.weather_binding.get()
        print(res)
        self.assertNotEquals(res, [], "Response list should not be empty")

    def test_get_all_icons(self):
        png_files = _get_all_weather_icons()
        expected = {'sunny': 'display/weather-icons/sunny.png',
                    'rain': 'display/weather-icons/rain.png',
                    'cloudy': 'display/weather-icons/cloudy.png',
                    'snow': 'display/weather-icons/snow.png',
                    'covered': 'display/weather-icons/covered.png',
                    'shower': 'display/weather-icons/shower.png'
                    }
        print(png_files)
        self.assertDictEqual(
            png_files, expected, "Icon dict does not match the expected value")
