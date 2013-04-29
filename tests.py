import requests
import logging
from sure import expect
import httpretty
import sys
import json
import re
from thebigdb import TheBigDB

requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)

logging.warning(sys.version)


# Class
def test_thebigdb_class_has_settable_configuration():
    thebigdb = TheBigDB()
    thebigdb2 = TheBigDB()
    thebigdb.api_host = "foobar"
    thebigdb.api_port = 1337
    thebigdb.api_version = "1337"
    thebigdb.api_key = "your-private-api-key"
    thebigdb.raise_on_api_status_error = True

    def before_request_exec():
        pass

    def after_request_exec():
        pass

    thebigdb.before_request_execution = before_request_exec
    thebigdb.after_request_execution = after_request_exec

    expect(thebigdb.api_host).to.equal("foobar")
    expect(thebigdb2.api_host).to.equal("api.thebigdb.com")
    expect(thebigdb.api_port).to.equal(1337)
    expect(thebigdb.api_version).to.equal("1337")
    expect(thebigdb.api_key).to.equal("your-private-api-key")
    expect(thebigdb.raise_on_api_status_error).to.equal(True)

    expect(thebigdb.before_request_execution).to.equal(before_request_exec)
    expect(thebigdb.after_request_execution).to.equal(after_request_exec)

    # autoset the port when using SSL
    thebigdb = TheBigDB(use_ssl = True)
    expect(thebigdb.api_port).to.equal(443)

# Abstract requests
@httpretty.activate
def test_executing_get_requests_sends_the_correct_http_request():
    httpretty.register_uri(httpretty.GET, re.compile("api.thebigdb.com"))

    thebigdb = TheBigDB()
    thebigdb.request("get", "/abc", {"foo": "bar"})

    expect(httpretty.httpretty.last_request.method).to.equal("GET")
    expect(httpretty.httpretty.last_request.path).to.equal("/v1/abc?foo=bar")
    expect(httpretty.httpretty.last_request).to.have.property("querystring").being.equal({
        "foo": ["bar"],
    })


@httpretty.activate
def test_executing_post_requests_sends_the_correct_http_request():
    httpretty.register_uri(httpretty.POST, re.compile("api.thebigdb.com"))

    thebigdb = TheBigDB()
    thebigdb.request("post", "/abc", {"foo": "bar"})

    expect(httpretty.httpretty.last_request.method).to.equal("POST")
    expect(httpretty.httpretty.last_request.path).to.equal("/v1/abc")
    expect(httpretty.httpretty.last_request).to.have.property("body").being.equal(
        "foo=bar"
    )


@httpretty.activate
def test_executing_requests_sends_the_correct_http_headers():
    httpretty.register_uri(httpretty.GET, re.compile("api.thebigdb.com"))

    thebigdb = TheBigDB()
    thebigdb.request("get", "/abc", {"foo": "bar"})

    expect(httpretty.httpretty.last_request.headers["user-agent"]).to.equal("TheBigDB PythonWrapper/" + thebigdb.wrapper_version)
    client_user_agent = {
        "publisher": "thebigdb",
        "version": thebigdb.wrapper_version,
        "language": "python",
        "language_version": sys.version,
    }
    expect(httpretty.httpretty.last_request.headers["x-thebigdb-client-user-agent"]).to.equal(json.dumps(client_user_agent))


@httpretty.activate
def test_executing_requests_returns_the_correct_json():
    httpretty.register_uri(httpretty.GET, re.compile("api.thebigdb.com"),
                           body = '{"server_says": "hello world", "status": true}')

    thebigdb = TheBigDB()
    response = thebigdb.request("get", "/abc", {"foo": "bar"})

    expect(response).to.equal({"server_says": "hello world", "status": True})


@httpretty.activate
def test_executing_requests_returns_the_correct_json_even_if_server_fails():
    httpretty.register_uri(httpretty.GET, re.compile("api.thebigdb.com"),
                           body = 'invalid json')

    thebigdb = TheBigDB()
    response = thebigdb.request("get", "/abc", {"foo": "bar"})

    expect(response).to.equal({'error': {'code': '0000', 'description': u'The server gave an invalid JSON body:\ninvalid json'}, 'status': 'error'})


# Statements
@httpretty.activate
def test_searching_sends_the_correct_http_request():
    httpretty.register_uri(httpretty.GET, re.compile("api.thebigdb.com"),
                           body = '{"server_says": "hello world"}')

    thebigdb = TheBigDB()
    thebigdb.search([{"match": "X"}, "Y", {"match": "Z"}], {"page": 2})

    expect(httpretty.httpretty.last_request.method).to.equal("GET")
    expect(httpretty.httpretty.last_request.path).to.equal("/v1/statements/search?nodes%5B0%5D%5Bmatch%5D=X&nodes%5B1%5D=Y&nodes%5B2%5D%5Bmatch%5D=Z&page=2")
    expect(httpretty.httpretty.last_request).to.have.property("querystring").being.equal({
        "nodes[0][match]": ["X"],
        "nodes[1]": ["Y"],
        "nodes[2][match]": ["Z"],
        "page": ["2"],
    })

@httpretty.activate
def test_creating_sends_the_correct_http_request():
    httpretty.register_uri(httpretty.POST, re.compile("api.thebigdb.com"),
                           body = '{"server_says": "hello world"}')

    thebigdb = TheBigDB(api_key = "foobarkey")
    thebigdb.create(["A", "B", "C"], {"period": {"from": "2013-01-01", "to": "2014-01-01"}})

    expect(httpretty.httpretty.last_request.method).to.equal("POST")
    expect(httpretty.httpretty.last_request.path).to.equal("/v1/statements/create")
    expect(httpretty.httpretty.last_request).to.have.property("body").being.equal("nodes%5B0%5D=A&nodes%5B1%5D=B&nodes%5B2%5D=C&api_key=foobarkey&period%5Bto%5D=2014-01-01&period%5Bfrom%5D=2013-01-01")


@httpretty.activate
def test_upvoting_sends_the_correct_http_request():
    httpretty.register_uri(httpretty.POST, re.compile("api.thebigdb.com"),
                           body = '{"server_says": "hello world"}')

    thebigdb = TheBigDB(api_key = "foobarkey")
    thebigdb.upvote("statement-id")

    expect(httpretty.httpretty.last_request.method).to.equal("POST")
    expect(httpretty.httpretty.last_request.path).to.equal("/v1/statements/upvote")
    expect(httpretty.httpretty.last_request).to.have.property("body").being.equal("api_key=foobarkey&id=statement-id")


@httpretty.activate
def test_showing_sends_the_correct_http_request():
    httpretty.register_uri(httpretty.GET, re.compile("api.thebigdb.com"),
                           body = '{"server_says": "hello world"}')

    thebigdb = TheBigDB(api_key = "foobarkey")
    thebigdb.show("statement-id")

    expect(httpretty.httpretty.last_request.method).to.equal("GET")
    expect(httpretty.httpretty.last_request.path).to.equal("/v1/statements/show?api_key=foobarkey&id=statement-id")
    expect(httpretty.httpretty.last_request).to.have.property("querystring").being.equal({
        "id": ["statement-id"],
        "api_key": ["foobarkey"]
    })


# correct and equivalent:
# requests.get("http://api.thebigdb.com/x?a=b&c=d", params={"nodes[0][match]": "foo", "nodes[1]": "bar", "page": 2})
# requests.get("http://api.thebigdb.com/x?a=b&c=d", params="nodes%5B1%5D=bar&nodes%5B0%5D%5Bmatch%5D=foo&page=2")

# Helpers
@httpretty.activate
def test_serialize_query_params_works_with_simple_params():
    thebigdb = TheBigDB()
    params = {"a": "b", "c": "d"}
    expect(thebigdb.serialize_query_params(params)).to.equal("a=b&c=d")

def test_serialize_query_params_works_with_imbricated_params():
    same_expected_result = "house=brick%20and%20mortar&computers%5Bdrives%5D%5B0%5D=hard&computers%5Bdrives%5D%5B1%5D=flash&computers%5Bcool%5D=True&animals%5B0%5D=cat&animals%5B1%5D=dog"

    thebigdb = TheBigDB()

    params = {"house": "brick and mortar", "animals": ["cat", "dog"], "computers": {"cool": True, "drives": ["hard", "flash"]}}

    # sadly, the dict has been deordered by python
    expect(thebigdb.serialize_query_params(params)).to.equal("house=brick%20and%20mortar&computers%5Bdrives%5D%5B0%5D=hard&computers%5Bdrives%5D%5B1%5D=flash&computers%5Bcool%5D=True&animals%5B0%5D=cat&animals%5B1%5D=dog")

    # and with a dict instead of an array for animals
    params = {"house": "brick and mortar", "animals": {"0": "cat", "1": "dog"}, "computers": {"cool": True, "drives": ["hard", "flash"]}}
    expect(thebigdb.serialize_query_params(params)).to.equal("house=brick%20and%20mortar&computers%5Bdrives%5D%5B0%5D=hard&computers%5Bdrives%5D%5B1%5D=flash&computers%5Bcool%5D=True&animals%5B1%5D=dog&animals%5B0%5D=cat")



