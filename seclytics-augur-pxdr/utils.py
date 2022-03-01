"""This is the utility module that contains some common functionalities.

Copyright (C) 2014 - 2022 Seclytics Inc. All rights reserved.
"""
import requests
from connectors.core.connector import get_logger, ConnectorError # pylint: disable=E0401
from .constants import LOGGER_NAME # pylint: disable=E0402

logger = get_logger(LOGGER_NAME)


class Seclytics():
    """Main Module for calling the Seclytics API
    Attributes:
        access_token (str): Seclytics Access Token
        base_url (str): API URL
        session (Session): requests session
    """
    def __init__(self, config, session=None):
        """Init function."""
        self.access_token = config.get('access_token')
        self.base_url = config.get('api_hostname')

        if not self.base_url:
            raise ConnectorError('Missing required parameters')

        # setup the session
        # allow users to pass in a session for proxy support
        self.session = session
        if not self.session:
            self.session = requests.Session()
        self.session.headers.update(self.default_headers)
        self.session.verify = config.get('verify_ssl', True)
        self.timeout = 60

    @property
    def default_headers(self):
        """Set default headers for the API."""
        return {'accept': 'application/json'}

    def api_get(self, endpoint):
        """Call our rest api to retrieve data."""
        url = 'https://{fqhn}{endpoint}?access_token={access_token}'.\
        	format(
                fqhn=self.base_url,
                endpoint=endpoint,
                access_token=self.access_token
            )
        logger.debug(url)

        try:
            response = self.session.get(url, timeout=self.timeout)
            if response.status_code in [404]:
                return {'Message': 'Not Found'}

            if response.status_code not in [200, 201]:
                error = response.json()
                error_msg = error.get('error')['message']
                message = 'HTTP Status Code {0}: {1} Details:{2}'.format(response.status_code, response.reason
                                                                         , error_msg if error_msg else "None")
                raise ConnectorError(message)
            else:
                json_response = response.json()
                logger.debug('Response: {0}'.format(json_response))
                if json_response:
                    return json_response

        except requests.exceptions.SSLError:
            logger.error('An SSL error occurred.')
            raise ConnectorError('An SSL error occurred.')
        except requests.exceptions.ConnectionError:
            logger.error('A connection error occurred.')
            raise ConnectorError('A connection error occurred.')
        except Exception as err:
            logger.error(err)
            raise ConnectorError(err)
