# This program is free software; you can redistribute it and/or modify
# it under the terms of the (LGPL) GNU Lesser General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library Lesser General Public License for more details at
# ( http://www.gnu.org/licenses/lgpl.html ).
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# written by: Jeff Ortel ( jortel@redhat.com )

"""
Contains classes for basic HTTP transport implementations.
"""

from suds.transport import *
from suds.properties import Unskin
from urlparse import urlparse
from cookielib import CookieJar
from logging import getLogger

import base64
import httplib
import socket
import sys
import urllib2

log = getLogger(__name__)


class HttpTransport(Transport):
    """
    HTTP transport using urllib2.  Provided basic http transport
    that provides for cookies, proxies but no authentication.
    """

    def __init__(self, **kwargs):
        """
        @param kwargs: Keyword arguments.
            - B{proxy} - An http proxy to be specified on requests.
                 The proxy is defined as {protocol:proxy,}
                    - type: I{dict}
                    - default: {}
            - B{timeout} - Set the url open timeout (seconds).
                    - type: I{float}
                    - default: 90
        """
        Transport.__init__(self)
        Unskin(self.options).update(kwargs)
        self.cookiejar = CookieJar()
        self.proxy = {}
        self.urlopener = None

    def open(self, request):
        try:
            url = request.url
            log.debug('opening (%s)', url)
            u2request = urllib2.Request(url)
            self.proxy = self.options.proxy
            return self.u2open(u2request)
        except urllib2.HTTPError, e:
            raise TransportError(str(e), e.code, e.fp)

    def send(self, request):
        result = None
        url = request.url
        msg = request.message
        headers = request.headers
        try:
            u2request = urllib2.Request(url, msg, headers)
            self.addcookies(u2request)
            self.proxy = self.options.proxy
            request.headers.update(u2request.headers)
            log.debug('sending:\n%s', request)
            fp = self.u2open(u2request)
            self.getcookies(fp, u2request)
            if sys.version_info < (3, 0):
                headers = fp.headers.dict
            else:
                headers = fp.headers
            result = Reply(httplib.OK, headers, fp.read())
            log.debug('received:\n%s', result)
        except urllib2.HTTPError, e:
            if e.code in (httplib.ACCEPTED, httplib.NO_CONTENT):
                result = None
            else:
                raise TransportError(e.msg, e.code, e.fp)
        return result

    def addcookies(self, u2request):
        """
        Add cookies in the cookiejar to the request.
        @param u2request: A urllib2 request.
        @rtype: u2request: urllib2.Requet.
        """
        self.cookiejar.add_cookie_header(u2request)

    def getcookies(self, fp, u2request):
        """
        Add cookies in the request to the cookiejar.
        @param u2request: A urllib2 request.
        @rtype: u2request: urllib2.Requet.
        """
        self.cookiejar.extract_cookies(fp, u2request)

    def u2open(self, u2request):
        """
        Open a connection.
        @param u2request: A urllib2 request.
        @type u2request: urllib2.Requet.
        @return: The opened file-like urllib2 object.
        @rtype: fp
        """
        tm = self.options.timeout
        url = self.u2opener()
        if (sys.version_info < (3, 0)) and (self.u2ver() < 2.6):
            socket.setdefaulttimeout(tm)
            return url.open(u2request)
        return url.open(u2request, timeout=tm)

    def u2opener(self):
        """
        Create a urllib opener.
        @return: An opener.
        @rtype: I{OpenerDirector}
        """
        if self.urlopener is None:
            return urllib2.build_opener(*self.u2handlers())
        return self.urlopener

    def u2handlers(self):
        """
        Get a collection of urllib handlers.
        @return: A list of handlers to be installed in the opener.
        @rtype: [Handler,...]
        """
        handlers = []
        handlers.append(urllib2.ProxyHandler(self.proxy))
        return handlers

    def u2ver(self):
        """
        Get the major/minor version of the urllib2 lib.
        @return: The urllib2 version.
        @rtype: float
        """
        try:
            part = urllib2.__version__.split('.', 1)
            return float('.'.join(part))
        except Exception, e:
            log.exception(e)
            return 0

    def __deepcopy__(self, memo={}):
        clone = self.__class__()
        p = Unskin(self.options)
        cp = Unskin(clone.options)
        cp.update(p)
        return clone


class HttpAuthenticated(HttpTransport):
    """
    Provides basic HTTP authentication for servers that do not follow the
    specified challenge/response model. This implementation appends the
    I{Authorization} HTTP header with base64 encoded credentials on every HTTP
    request.
    """

    def open(self, request):
        self.addcredentials(request)
        return HttpTransport.open(self, request)

    def send(self, request):
        self.addcredentials(request)
        return HttpTransport.send(self, request)

    def addcredentials(self, request):
        credentials = self.credentials()
        if not (None in credentials):
            credentials = ':'.join(credentials)
            # Bytes and strings are different in Python 3 than in Python 2.x.
            if sys.version_info < (3,0):
                basic = 'Basic %s' % base64.b64encode(credentials)
            else:
                encodedBytes = base64.urlsafe_b64encode(credentials.encode())
                encodedString = encodedBytes.decode()
                basic = 'Basic %s' % encodedString
            request.headers['Authorization'] = basic

    def credentials(self):
        return (self.options.username, self.options.password)
