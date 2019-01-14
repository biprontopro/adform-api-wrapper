import logging

import requests

from . import status


logger = logging.getLogger(__name__)


class AdformApi(object):
    '''
    Low-level API wrapper
    '''
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.authentication_base_url = 'https://id.adform.com'
        self.api_base_url = 'https://api.adform.com'
        self.api_version = 'v1'
        self.session = requests.Session()

    def get(self, path, params=None):
        return self._call('GET', path, params=params)

    def options(self, path):
        return self._call('OPTIONS', path)

    def head(self, path):
        return self._call('HEAD', path)

    def delete(self, path):
        return self._call('DELETE', path)

    def post(self, path, payload=None):
        return self._call('POST', path, payload)

    def put(self, path, payload=None):
        return self._call('PUT', path, payload)

    def patch(self, path, payload=None):
        return self._call('PATCH', path, payload)

    def _call(self, method, path, payload=None, params=None):
        if self.session.headers.get('Authorization') is None:
            logger.info('Authentication token not found. Obtaining authentication token')
            self._authenticate()

        url = '{}/{}{}'.format(self.api_base_url, self.api_version, path)
        response = self.session.request(method, url, json=payload, params=params)

        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            logger.info('HTTP_401_UNAUTHORIZED received from API. Refreshing authentication token')
            self._authenticate()
            response = self.session.request(method, url, data=payload)

        return response

    def _api_scope(self):
        scope_list = [
            'buyer.campaigns.api',
            'buyer.rtb.lineitem',
            'eapi',
        ]
        scope_base_url = '{api_base_url}/scope/'.format(api_base_url=self.api_base_url)
        scope_list_full_urls = [scope_base_url + scope for scope in scope_list]
        return ' '.join(scope_list_full_urls)

    def _authenticate(self):
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': self._api_scope(),
        }
        url = ('{authentication_base_url}/sts/connect/token'.
               format(authentication_base_url=self.authentication_base_url))

        response = self.session.post(url, data=payload)
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            logger.error('API returned HTTP_400_BAD_REQUEST')
            raise Exception('Please check your client_id and client_secret')

        authorization = '{} {}'.format(response.json().get('token_type'),
                                       response.json().get('access_token'))
        self.session.headers.update({'Authorization': authorization})
        logger.info('Authentication token updated')
