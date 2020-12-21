# Guildagram

A Flask app that implements a highly simplified messaging API.

## Install

    # clone the repository
    $ git clone https://github.com/nathan-contino/guildagram
    $ cd guildagram

Create a virtualenv and activate it:

    $ python3 -m venv venv
    $ . venv/bin/activate

Or on Windows cmd:

    $ py -3 -m venv venv
    $ venv\Scripts\activate.bat

Install Guildagram:

    $ pip install -e .
    $ pip install flask_api

Install MongoDB (trust me, this is fewer steps than the docs indicate)
following the instructions [here](https://docs.mongodb.com/manual/installation/). Once you've installed mongodb, you can start a local instance with
the ``mongod`` command:

    $ mongod --dbpath db/

Starting a mongodb instance by default uses your current directory for
all of the files used to run mongodb. So I *highly* recommend passing
the db/ directory as the dbpath when you start up your local instance!

## Run

    $ export FLASK_APP=guildagram
    $ export FLASK_ENV=development
    $ flask run -p 1337

Or on Windows cmd::

    > set FLASK_APP=guildagram
    > set FLASK_ENV=development
    > flask run -p 1337

You can use your browser's developer tools or
[Postman](https://www.postman.com/) to test the
``getMessages`` and ``sendMessage`` endpoints
at ``http://127.0.0.1:1337``.

## Test

    $ pip install '.[test]'
    $ pytest

## API

Guildagram provides two API methods to send and receive messages:

1) To send a message, you should send a ``POST`` request to ``http://127.0.0.1:1337/sendMessage/``
    with a body containing JSON with the following schema:
    
        {
            sender: "your_username",
            receiver: "who_you_would_like_to_message",
            content: "message text",
        }

    Fill in the sender, receiver, and content fields for the message you would like to send.

    If your message sends successfully, you'll receive a response with response code 201: Created
    and a JSON response body containing the field ``success`` with a value of ``true``.
    If your message does not send successfully, you will either receive:

        - a response with response code 400: Bad request and a JSON request body
          containing the field ``success`` with a value of ``false`` and a
          field called ``message`` with a detailed description of what was wrong
          with your request

        - a 404/500 error in the case of an unexpected error

2) To view messages, send a ``GET`` request to ``http://127.0.0.1:1337/getMessages/<receiver>/<sender (optional)>``
   The ``receiver`` parameter is required -- typically, you'd send your own username (though because this API lacks
   authentication, you can send any username). You can also include an optional ``sender`` parameter, which filters
   the returned messages to only messages that originated from the specified user. The getMessages API only returns
   up to 100 messages from the last 30 days, with messages ordered from newest to oldest.

   If your message sends successfully, you'll receive a response with response code 200: OK and
   a JSON response body containing the field "messages" which contains a list of messages that
   matched your specified receiver and sender (if you specified a sender). Messages adhere to the
   following schema:

        {
            "_id": {
                "$oid": <a unique Object ID>
            },
            "content": <your message text>,
            "receiver": <receiver username>,
            "sender": <sender username>,
            "when": {
                "$date": <UTC unix epoch timestamp of the time the message was received by Guildagram to the nearest second>
            }
        }
