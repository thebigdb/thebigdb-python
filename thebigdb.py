import requests
import json
import sys
import urllib
import logging

class TheBigDB:
    default_configuration = {
        "api_key": None,
        "api_host": "api.thebigdb.com",
        "api_port": 80,
        "api_version": "1",
        "use_ssl": False,
        "verify_ssl_certificates": False, # Not implemented yet
        "before_request_execution": None, # Not implemented yet
        "after_request_execution": None, # Not implemented yet
        "raise_on_api_status_error": False, # Not implemented yet
        "debug": False # Not implemented yet
    }

    wrapper_version = "0.0.3"

    def __init__(self, **kwargs):
        for key, value in self.default_configuration.items():
            setattr(self, key, kwargs.get(key, value))

        if kwargs.get("use_ssl") == True and kwargs.get("api_port") == None:
            self.api_port = 443

        self.response = None


    ##############################
    # Shortcuts to actions on Statements
    ##############################

    # GET
    def search(self, nodes = {}, other_params = {}):
        params = {"nodes": nodes}
        params.update(other_params)
        return self.request("get", "/statements/search", params)

    def show(self, id, other_params = {}):
        params = {"id": id}
        params.update(other_params)
        return self.request("get", "/statements/show", params)

    # POST
    def create(self, nodes = {}, other_params = {}):
        params = {"nodes": nodes}
        params.update(other_params)
        return self.request("post", "/statements/create", params)

    def upvote(self, id, other_params = {}):
        params = {"id": id}
        params.update(other_params)
        return self.request("post", "/statements/upvote", params)

    def downvote(self, id, other_params = {}):
        params = {"id": id}
        params.update(other_params)
        return self.request("post", "/statements/downvote", params)


    ##############################
    # Other actions
    ##############################

    def user(self, action, params):
        return self.request("get", "/users/"+action, params)


    ##############################
    # Engine
    ##############################

    def request(self, method, request_uri, params = {}):
        method = method.lower()
        scheme = "https" if self.use_ssl else "http"

        url = scheme + "://" + self.api_host + ":" + str(self.api_port) + "/v" + self.api_version + request_uri

        headers = {
            "user-agent": "TheBigDB PythonWrapper/"+self.wrapper_version,
            "x-thebigdb-client-user-agent": json.dumps({
                "publisher": "thebigdb",
                "version": self.wrapper_version,
                "language": "python",
                "language_version": sys.version,
            })
        }

        if self.api_key:
            params.update({"api_key": self.api_key})

        params = self.serialize_query_params(params)

        if method == "get":
            self.response = requests.get(url, headers = headers, params = params)
        elif method == "post":
            self.response = requests.post(url, headers = headers, data = params)

        try:
            self.response_json = self.response.json()
        except ValueError:
            self.response_json = {"status": "error", "error": {"code": "0000", "description": "The server gave an invalid JSON body:\n%s" % self.response.text}} 
        
        return self.response_json



    ##############################
    # Helpers
    ##############################

    # serialize_query_params({"house": "brick and mortar", "animals": ["cat", "dog"], "computers": {"cool": True, "drives": ["hard", "flash"]}})
    # => house=brick%20and%20mortar&computers%5Bdrives%5D%5B0%5D=hard&computers%5Bdrives%5D%5B1%5D=flash&computers%5Bcool%5D=True&animals%5B0%5D=cat&animals%5B1%5D=dog
    # which will be read by the server as:
    # => house=brick%20and%20mortar&computers[drives][0]=hard&computers[drives][1]=flash&computers[cool]=True&animals[0]=cat&animals[1]=dog
    def serialize_query_params(self, params, prefix = None):
        ret = []

        if isinstance(params, dict):
            for i, (key, value) in enumerate(params.items()):
                ret.append(self.serialize_query_params_processing(prefix, key, value))
        elif isinstance(params, (list, tuple)):
            for key, value in enumerate(params):
                ret.append(self.serialize_query_params_processing(prefix, key, value))

        return "&".join(ret)

    def serialize_query_params_processing(self, prefix, key, value):
        param_key = "%s[%s]" % (prefix, key) if prefix else key

        if isinstance(value, dict):
            return self.serialize_query_params(value, param_key)
        elif isinstance(value, (list, tuple)):
            sub_dict = {}
            for i, value_item in enumerate(value):
                sub_dict[str(i)] = value_item
            return self.serialize_query_params(value, param_key)
        else:
            return urllib.quote(str(param_key)) + "=" + urllib.quote(str(value))


