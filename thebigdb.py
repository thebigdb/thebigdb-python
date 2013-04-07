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
            ):
        self.apiKey=apiKey
        self.connection=HTTPConnection("api.thebigdb.com")

    def search(self, params, successCallback, errorCallback):
        """
        " Searches TheBigDB
        """
        requestString='/v1/statements/search?'
        for i in range(len(params)):
            if (params[i] != ''):
                requestString += 'nodes[%d]=%s&' % (i, quote(params[i]))
            else:
                requestString += 'nodes[%d][search]=&' % (i)

        if self.apiKey != '':
            requestString += 'api_key=' + self.apiKey + '&'
        #do the actual request
        print(requestString)
        self.connection.request('GET', requestString)
        response=self.connection.getresponse()
        if response.status != 200 : #Something went wrong!
            errorCallback(response)
        else:
            successCallback(response.read().decode("UTF-8"))

    def add_nodes(self, nodes):
        """
        " Attempts to add a node to TheBigDB
        """
        requestString='/v1/statements/create'
        requestData=''
        if self.apiKey != '':
            requestData += 'api_key=' + self.apiKey + '&'
        for i in range(len(nodes)):
            requestData += 'nodes[%d]=%s&' % (i, quote(nodes[i]))
#        print(requestData)
        self.connection.request('POST', requestString, requestData)
        return self.connection.getresponse().read().decode('UTF-8')
