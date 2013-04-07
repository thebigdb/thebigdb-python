"""
 The Big DB python API
 Written to follow the Javascript API as closely as possible.
"""
from http.client import HTTPConnection
from urllib.parse import quote

class TheBigDB:
    """
    Represents a connection to TheBigDB
    """
    def __init__(
            self,
            apiKey="",
            useSSL=False,                #Not implemented.
            verifySSLCertificates=False, #Not implemented.
            beforeRequestExecution=False,#Not implemented.
            afterRequestExecution=False, #Not implemented.
            debug=False,
            ):
        self.apiKey=apiKey
        self.connection=HTTPConnection("api.thebigdb.com")
        self.debug=debug

    def search(self, params, successCallback, errorCallback):
        """
        " Searches TheBigDB
        """
        requestString='/v1/statements/search?'
        for i in range(len(params)):
            if (params[i] != ''):
                requestString += 'nodes[%d]=%s&' % (i, quote(params[i]))
            else:
                requestString += 'nodes[%d][match]=&' % (i)

        if self.apiKey != '':
            requestString += 'api_key=' + self.apiKey + '&'
        #do the actual request
        if self.debug: print(requestString)
        self.connection.request('GET', requestString)
        response=self.connection.getresponse()
        if response.status != 200 : #Something went wrong!
            errorCallback(response)
        else:
            successCallback(response.read().decode("UTF-8"))

    def create(self, nodes, successCallback, errorCallback):
        """
        " Attempts to add a node to TheBigDB
        """
        requestData=''
        if self.apiKey != '':
            requestData += 'api_key=' + self.apiKey + '&'
        for i in range(len(nodes)):
            requestData += 'nodes[%d]=%s&' % (i, quote(nodes[i]))
        if self.debug:print(requestData)
        self.connection.request('POST','/v1/statements/create',requestData)
        response=self.connection.getresponse()
        if response.status != 200 : #Something went wrong!
            errorCallback(response)
        else:
            successCallback(response.read().decode("UTF-8"))

    def _vote(self, nodeid, successCallback, errorCallback, url):
        requestData=''
        if self.apiKey != '':
            requestData += 'api_key=' + self.apiKey + '&'
        requestData += 'id=%s&' % (nodeid)
        self.connection.request('POST',url,requestData)
        response=self.connection.getresponse()
        if response.status != 200 : #Something went wrong!
            errorCallback(response)
        else:
            successCallback(response.read().decode("UTF-8"))


    def upvote(self, nodeid, successCallback, errorCallback):
        """
        " Upvotes a node.
        """
        self._vote(nodeid, successCallback, errorCallback, '/v1/statements/upvote')
    
    def downvote(self, nodeid, successCallback, errorCallback):
        """
        " Downvotes a node.
        """
        self._vote(nodeid, successCallback, errorCallback, '/v1/statements/downvote')
