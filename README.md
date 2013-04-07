IMPORTANT NOTE
===============

This is an experimental python wrapper for [TheBigDB.com API](http://thebigdb.com). It is currently under heavy development by the community and can change radically at any moment. As said in the [original README](https://github.com/thebigdb/thebigdb-python/blob/1d7b48b1e4d6e213167b26e1170c837e05553ba0/README.md), it is mainly inspired by the [Ruby](https://github.com/thebigdb/thebigdb-ruby) and the [Javascript](https://github.com/thebigdb/thebigdb-js) wrappers. You are more than welcome to improve it, by submitting a pull request.

Usage
===============

Using TheBigDB's python client is very simple.

First, create an instance of TheBigDB:

    db=TheBigDB('YOUR_API_KEY_GOES_HERE')

To search TheBigDB:

The empty string is treated as a wildcard.

    def success_callback(response):
        #Here you can proccess the response to your query.
        #response is the JSON string that TheBigDB returned
        #success in this case only means that the HTTP request did not error out
        #it does not mean that TheBigDB has not returned an error code.

    def failure_callback(response):
        #Called on HTTP request failure.
        #response is an object of type http.client.HTTPResponse

    db.search(['', 'atomic radius'], success_callback, failure_callback)
    # Returns all facts with 'atomic radius' as the second node.

To insert data into TheBigDB:
    
    #inserts the atomic radius of iron into TheBigDB
    db.create(['Iron', 'atomic radius', '140 pm'], success_callback, failure_callback)

To upvote/downvote a node:
    
    db.upvote('NODE_ID') #Get the NodeID from db.search
    db.downvote('NODE_ID')
