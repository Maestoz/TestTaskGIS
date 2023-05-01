import json
import requests
from datetime import datetime
import pytz
import pytest
import random
import string
import time


class TestSuite:
    main_url = "https://regions-test.2gis.com"
    cookies_token = ""
    colors = [
        ("BLUE"),
        ("GREEN"),
        ("RED"),
        ("YELLOW")
    ]
    colors_negative = [
        ("PURPLE"),
        (""),
        ("#0000FF")
    ]
    titles = [
        (''.join(random.choice(string.printable) for i in range(1))),
        (''.join(random.choice(string.printable) for i in range(500))),
        (''.join(random.choice(string.printable) for i in range(999)))
    ]
    titles_negative = [ # TODO: Need to remove
        (""),
        (''.join(random.choice(string.printable) for i in range(1000)))
    ]
    lat_available = [
        (-90.000000),
        (-50.555555),
        (-0.000001),
        (0.000000),
        (0.000001),
        (50.555555),
        (90.000000)
    ]
    lon_available = [
        (-180.000000),
        (-90.555555),
        (-0.000001),
        (0.000000),
        (0.000001),
        (90.555555),
        (180.000000)
    ]
    lat_wrong = [
        (-150),
        (-90.000001),
        (-91),
        (90.000001),
        (91),
        (150)
    ]
    lon_wrong = [
        (-200),
        (-181),
        (-180.000001),
        (180.000001),
        (181),
        (200)
    ]


    def setup_method(self):
        mthd = "/v1/auth/tokens"
        try:
            session = requests.Session()
            response = session.post(TestSuite.main_url + mthd)
        except requests.exceptions.ConnectionError:
            assert False, "Connection error by server"
        else:
            assert "token" in response.cookies, "There is not token in the response"
            self.auth_cookies = session.cookies.get_dict()
            # print(f"\n {mthd}'s cookies: {response.cookies}\n") # The prints like this are used for debugging via -rA key

    def test_set_favorite(self):
        mthd = "/v1/favorites"
        title_value = "TestTitle"
        lat_value = 50.0 # The valid values are between -90 and 90
        lon_value = 50.0 # The valid values are between -180 and 180
        color_value = "BLUE"
        body = {
            "title": title_value,
            "lat": lat_value,
            "lon": lon_value,
            "color": color_value
        }
        try:
            response = requests.post(TestSuite.main_url + mthd, data=body, cookies=self.auth_cookies)
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"
        else:
            assert response.status_code == 200, f"Unexpected status code {response.status_code}"
            assert "id" in response.json(), "The 'id' field is missed"
            assert "title" in response.json(), "The 'title' field is missed"
            assert "lat" in response.json(), "The 'lat' field is missed"
            assert "lon" in response.json(), "The 'lon' field is missed"
            assert "color" in response.json(), "The 'color' field is missed"
            assert "created_at" in response.json(), "The 'created_at' field is missed" # TODO: create a BaseAssertion Class for this list
            assert response.json()["id"] > 0, "The 'id' value is less than 0"
            assert response.json()["title"] == title_value, "The 'title' value is not equal to requests"
            assert response.json()["lat"] == lat_value, "The 'lat' value is not equal to requests"
            assert response.json()["lon"] == lon_value, "The 'lon' value is not equal to requests"
            assert response.json()["color"] == color_value, "The 'color' value is not equal to requests"
            parsed_time = response.json()["created_at"].rsplit(':', 2)  # Comparison with accuracy to minutes
            created_at_without_seconds = parsed_time[0]
            datetime_server = datetime.now(pytz.timezone('Europe/London'))  # Switch to server time from local
            formatted_date = datetime_server.strftime("%Y-%m-%dT%H:%M")
            assert created_at_without_seconds == formatted_date, "Unexpected time in 'created_at'" # TODO: To solve a problem of minutes inaccuracy
            print(f"\n {mthd}'s response: {response.json()}\n")

    def test_set_favorite_without_color(self):
        mthd = "/v1/favorites"
        title_value = "TestTitle"
        lat_value = 50.0  # The valid values are between -90 and 90
        lon_value = 50.0  # The valid values are between -180 and 180
        body = {
            "title": title_value,
            "lat": lat_value,
            "lon": lon_value,
        }
        response = requests.post(TestSuite.main_url + mthd, data=body, cookies=self.auth_cookies)
        assert response.status_code == 200, f"Unexpected status code {response.status_code}"
        assert response.json()["id"] > 0, "The 'id' value is less than 0"
        assert response.json()["title"] == title_value, "The 'title' value is not equal to requests"
        assert response.json()["lat"] == lat_value, "The 'lat' value is not equal to requests"
        assert response.json()["lon"] == lon_value, "The 'lon' value is not equal to requests"
        assert response.json()["color"] == None, "The 'color' value is not equal to None"
        print(f"\n {mthd}'s response: {response.json()}\n")

    @pytest.mark.parametrize('color', colors)
    def test_all_available_colors(self, color):
        mthd = "/v1/favorites"
        title_value = "TestTitle"
        lat_value = 50.0  # The valid values are between -90 and 90
        lon_value = 50.0  # The valid values are between -180 and 180
        body = {
            "title": title_value,
            "lat": lat_value,
            "lon": lon_value,
            "color": color
        }
        response = requests.post(TestSuite.main_url + mthd, data=body, cookies=self.auth_cookies)
        assert response.status_code == 200, f"Unexpected status code {response.status_code}"
        assert response.json()["id"] > 0, "The 'id' value is less than 0"
        assert response.json()["title"] == title_value, "The 'title' value is not equal to requests"
        assert response.json()["lat"] == lat_value, "The 'lat' value is not equal to requests"
        assert response.json()["lon"] == lon_value, "The 'lon' value is not equal to requests"
        assert response.json()["color"] == color, "The 'color' value is not equal to requests"
        print(f"\n {mthd}'s response: {response.json()}\n")

    @pytest.mark.parametrize('title', titles)
    def test_all_available_titles(self, title):
        mthd = "/v1/favorites"
        lat_value = 50.0  # The valid values are between -90 and 90
        lon_value = 50.0  # The valid values are between -180 and 180
        body = {
            "title": title,
            "lat": lat_value,
            "lon": lon_value,
        }
        response = requests.post(TestSuite.main_url + mthd, data=body, cookies=self.auth_cookies)
        assert response.status_code == 200, f"Unexpected status code {response.status_code}"
        assert response.json()["id"] > 0, "The 'id' value is less than 0"
        assert response.json()["title"] == title, "The 'title' value is not equal to requests"
        assert response.json()["lat"] == lat_value, "The 'lat' value is not equal to requests"
        assert response.json()["lon"] == lon_value, "The 'lon' value is not equal to requests"
        assert response.json()["color"] == None, "The 'color' value is not equal to None"
        print(f"\n {mthd}'s response: {response.json()}\n")

    @pytest.mark.parametrize('color', colors_negative)
    def test_negative_colors(self, color):
        mthd = "/v1/favorites"
        title_value = "TestTitle"
        lat_value = 50.0  # The valid values are between -90 and 90
        lon_value = 50.0  # The valid values are between -180 and 180
        body = {
            "title": title_value,
            "lat": lat_value,
            "lon": lon_value,
            "color": color
        }
        response = requests.post(TestSuite.main_url + mthd, data=body, cookies=self.auth_cookies)
        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        print(f"\n {mthd}'s response: {response.json()}\n")
        assert "error" in response.json(), "There is no 'error' for a wrong request"
        assert (json.loads(response.text).get('error').get('message')) == "Параметр 'color' может быть одним из следующих значений: BLUE, GREEN, RED, YELLOW", "There is no 'message' for a wrong request"
        # TODO: To figure out negative asserts
        # TODO: To fix this trash with assert message

    @pytest.mark.parametrize('title', titles_negative)
    def test_all_available_titles(self, title):  # TODO: divide on 2 tests, validate it
        mthd = "/v1/favorites"
        lat_value = 50.0  # The valid values are between -90 and 90
        lon_value = 50.0  # The valid values are between -180 and 180
        body = {
            "title": title,
            "lat": lat_value,
            "lon": lon_value,
        }
        response = requests.post(TestSuite.main_url + mthd, data=body, cookies=self.auth_cookies)
        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        assert "error" in response.json(), "There is no 'error' for a wrong request"
        print(f"\n {mthd}'s response: {response.json()}\n")

    def COMMENTtest_lifetime_of_token(self):
        mthd = "/v1/favorites"
        title_value = "TestTitle"
        lat_value = 50.0  # The valid values are between -90 and 90
        lon_value = 50.0  # The valid values are between -180 and 180
        body = {
            "title": title_value,
            "lat": lat_value,
            "lon": lon_value,
        }
        time.sleep(2001/1000) # error at 2959 ms
        response = requests.post(TestSuite.main_url + mthd, data=body, cookies=self.auth_cookies)
        assert response.status_code == 401, f"Unexpected status code {response.status_code}"

    @pytest.mark.parametrize('lat', lat_available) # TODO: To figure out with exponential format of numbers
    def test_available_lat(self, lat):
        mthd = "/v1/favorites"
        title_value = "TestTitle"
        lon_value = 50.0  # The valid values are between -180 and 180
        body = {
            "title": title_value,
            "lat": lat,
            "lon": lon_value,
        }
        response = requests.post(TestSuite.main_url + mthd, data=body, cookies=self.auth_cookies)
        assert response.status_code == 200, f"Unexpected status code {response.status_code}"
        assert response.json()["lat"] == lat, "The 'lat' value is not equal to requests"
        print(f"\n {mthd}'s response: {response.json()}\n")

    @pytest.mark.parametrize('lon', lon_available)  # TODO: To figure out with exponential format of numbers
    def test_available_lat(self, lon):
        mthd = "/v1/favorites"
        title_value = "TestTitle"
        lat_value = 50.0  # The valid values are between -90 and 90
        body = {
            "title": title_value,
            "lat": lat_value,
            "lon": lon,
        }
        response = requests.post(TestSuite.main_url + mthd, data=body, cookies=self.auth_cookies)
        assert response.status_code == 200, f"Unexpected status code {response.status_code}"
        assert response.json()["lon"] == lon, "The 'lon' value is not equal to requests"
        print(f"\n {mthd}'s response: {response.json()}\n")

    @pytest.mark.parametrize('lat', lat_wrong)
    def test_lat_wrong(self, lat):
        mthd = "/v1/favorites"
        title_value = "TestTitle"
        lon_value = 50.0  # The valid values are between -180 and 180
        body = {
            "title": title_value,
            "lat": lat,
            "lon": lon_value,
        }
        response = requests.post(TestSuite.main_url + mthd, data=body, cookies=self.auth_cookies)
        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        assert "должен быть" in response.json(), "There is not correct 'message'"
        # assert response.json()["lat"] == lat, "The 'lat' value is not equal to requests"
        print(f"\n {mthd}'s response: {response.json()}\n")