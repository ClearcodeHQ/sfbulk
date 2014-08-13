import requests

from sfbulk.exceptions import BulkException
from sfbulk.utils_xml import parseXMLResult


# XML CONSTANS

LOGIN_SOAP_REQUEST_HEADERS = {
    u'content-type': 'text/xml',
    u'charset': 'UTF-8',
    u'SOAPAction': 'login'
}

LOGIN_SOAP_REQUEST_BODY = u"""<?xml version="1.0" encoding="utf-8" ?>
<env:Envelope
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
        <n1:login xmlns:n1="urn:partner.soap.sforce.com">
            <n1:username>{username}</n1:username>
            <n1:password>{password}{token}</n1:password>
        </n1:login>
    </env:Body>
</env:Envelope>"""


class sf(object):
    """
    Base class with login method by Rest API.
    """

    # SOAP CONSTANS

    SOAP_URL = u'https://{domain}.salesforce.com/services/Soap/u/{sf_version}'
    DOMAIN = u'login'

    def login(self, username=u'', password=u'', security_token=u'',
              sf_version=u'26.0', sandbox=False):
        """
        Sets a sessionid and bulk_server
        where `sessionid` is the session ID to use
        for authentication to Salesforce
        and `bulk_server` is the domain of the instance
        of Salesforce to use for the session.

        @type username: string
        @param username: the Salesforce username to use for authentication
        @type password: string
        @param password: the password for the username
        @type security_token: string
        @param security_token: the security token for the username
        @type sf_version: string
        @param sf_version: the version of the Salesforce API to use,
                           for example "27.0"
        @type sf_version: boolean
        @pram sandbox: True if you want to login to `test.salesforce.com`,
                       False if you want to login to `login.salesforce.com`.

        @rtype: None

        Modified from Simple-Salesforce.
        """
        if username:
            self.USERNAME = username
        if password:
            self.PASSWORD = password
        if security_token:
            self.SECURITY_TOKEN = security_token

        self.SF_VERSION = sf_version
        self.SANDBOX = sandbox

        domain = self.DOMAIN
        if sandbox:
            domain = u'test'

        soap_url = \
            self.SOAP_URL.format(domain=domain, sf_version=sf_version)

        login_soap_request_body = LOGIN_SOAP_REQUEST_BODY.format(
            username=self.USERNAME,
            password=self.PASSWORD,
            token=self.SECURITY_TOKEN)

        response = self._send_login_request(soap_url, login_soap_request_body)
        self._check_response(response)
        self._set_credentials(response)

    # HELPERS

    def _send_login_request(self, soap_url, login_soap_request_body):
        return requests.post(soap_url,
                             login_soap_request_body,
                             headers=LOGIN_SOAP_REQUEST_HEADERS)

    def _set_credentials(self, response):
        dict_result = parseXMLResult(response.content)
        self.sessionid = dict_result['sessionId']
        self.soap_server = dict_result['serverUrl']
        self.bulk_server = dict_result['serverUrl'].split('services')[0]

    @staticmethod
    def _check_response(response):
        if response.status_code != 200:
            dict_result = parseXMLResult(response.content)
            except_msg = dict_result['sf:exceptionMessage']
            except_code = dict_result['sf:exceptionCode']
            raise BulkException('{message}: {code}'.format(
                message=except_msg, code=except_code))
