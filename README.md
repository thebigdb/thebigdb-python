# TheBigDB Python Wrapper

A simple python wrapper for making requests to the API of [TheBigDB.com](http://thebigdb.com). [Full API documentation](http://developers.thebigdb.com/api).

## Install

Just grab the file ``thebigdb.py``. You'll only need to have the package [requests](http://docs.python-requests.org/en/latest/user/install/) intalled.

## Simple usage

First, you need to initialize the class with:
    
    from thebigdb import TheBigDB
    thebigdb = TheBigDB()

The following actions return a dict object from the parsed JSON the server answered.

### Search \([api doc](http://developers.thebigdb.com/api#statements-search)\)

    thebigdb.search([{"match": "James"}, "job", "President of the United States"])
    thebigdb.search([{"match": "Facebook"}, "job", {"match": "Executive"}])

### Create \([api doc](http://developers.thebigdb.com/api#statements-create)\)
    
    thebigdb.api_key = "your-private-api-key"

    thebigdb.create(["iPhone 5", "weight", "112 grams"])
    thebigdb.create(["Bill Clinton", "job", "President of the United States"], {"period": {"from": "1993-01-20 12:00:00", "to": "2001-01-20 12:00:00"}})

### Show \([api doc](http://developers.thebigdb.com/api#statements-show)\), Upvote \([api doc](http://developers.thebigdb.com/api#statements-upvote)\) and Downvote \([api doc](http://developers.thebigdb.com/api#statements-downvote)\)

    thebigdb.show("id-of-the-sentence")

    thebigdb.upvote("id-of-the-sentence") # don't forget to set your API key
    thebigdb.downvote("id-of-the-sentence") # don't forget to set your API key

That's it!


## Response object

If you want more details on what has been received, you can check ``thebigdb.response`` after each request.
It is the object returned by the ``requests`` package after each request.

It has several readable attributes:
    
    thebigdb.show("id-of-the-sentence")
    thebigdb.response.content       # String of the actual content received from the server
    thebigdb.response.headers       # Dict of the headers received from the server

[More details](http://docs.python-requests.org/en/latest/user/quickstart/#response-content)

## Other Features

You can access other parts of the API in the same way as statements:
    
    thebigdb.user(action, parameters)

    # Examples
    thebigdb.user("show", {"login": "christophe"})["user"]["karma"]


## Requirements

- Python 2.7+

## Contributing

Don't hesitate to send a pull request !

## Testing

First, install the required packages:

    pip install -r requirements.pip

Then, run the tests in the ``tests.py`` file with:

    nosetests


# Thanks
- [bobtwinkles](https://github.com/bobtwinkles) for creating the first version of this wrapper
- The community for their invaluable feedback!
