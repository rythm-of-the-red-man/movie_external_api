from django.conf import settings
from rest_framework.exceptions import NotFound, APIException
from rest_framework import status
import requests
from requests.exceptions import HTTPError


class MovieService(object):
    """This service fetch data from
    external API."""

    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url

    def get_movie(self, title):

        # Initialize params for external API get request
        params = {
            'apikey': self.api_key,
            't': title
        }
        # Fetch data from external API, and handle eventual errors
        try:
            response = requests.get(self.api_url, params=params)
        except HTTPError:
            raise APIException(detail={
                               'message': 'External API unavailable'}, code=status.HTTP_503_SERVICE_UNAVAILABLE)

        # Checks if API responded without errors.
        if 'Error' in response.json().keys():
            raise NotFound(detail=response.json(),
                           code=status.HTTP_404_NOT_FOUND)

        return self.sanitize_data(response.json())

    def sanitize_data(self, not_sanitized_data):
        """Make all keys lowercase, change 'N/A' key for None, and handle
         thousands separator in imdbvotes."""

        def lower_keys(data):
            return {k.lower(): v for k, v in data.items()}

        data = lower_keys(not_sanitized_data)
        data['ratings'] = [lower_keys(val) for val in data['ratings']]
        data['imdbvotes'] = data['imdbvotes'].replace(',', '')
        data['boxoffice'] = data['boxoffice'].replace('$', '').replace(',', '')
        for key, value in data.items():
            if value == 'N/A':
                data[key] = None
        return data
