import urllib
import urllib2

from pprint import pformat
from sfbulk.exceptions import BulkException


class Callout(object):
    """
    Helper class to easily do GET / POST method along with the encoded data.
    """
    headerAuth = None
    sessionid = None

    AUTHORIZATION = u'Authorization'

    def __init__(self, header={}, logger=None):
        if self.AUTHORIZATION in header:
            self.headerAuth = header['Authorization']
        self.logger = logger

    def docall(self, url, method, tdata=None, headers=None):
        """
        Initiate http call (get / post) along with the data.

        @type: string
        @param url: server url information for the callout destination
        @type: string
        @param method: "GET" or "POST"
        @type: string
        @param tdata: data information which will be submitted on the BODY
        @type: headers
        @param headers: header information
        """
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)
        if tdata is not None:
            if type(tdata) == dict:
                data = urllib.urlencode(tdata)
            else:
                data = tdata
        else:
            data = urllib.urlencode({})
        request = urllib2.Request(url, data)

        if headers is not None:
            for keyh, valueh in headers.iteritems():
                request.add_header(keyh, valueh)
        request.get_method = lambda: method

        try:
            connection = opener.open(request)
        except urllib2.HTTPError as e:
            self.logger.info(
                "Request url: \n %s" % pformat(request.get_full_url()))
            self.logger.info(
                "Request headers: \n %s" % pformat(request.headers))
            self.logger.info("Request data: \n %s" % pformat(request.data))
            message = "Http error occurred on doing API call: %s" % e
            raise BulkException(message)
        return connection.read()
