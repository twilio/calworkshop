.. _voting:

SMS Polling and Voting
======================

Whether at a hackathon or a student group meeting, you'll often need to vote on
items. Elections, food, or nominations - all these situations can be handled via
SMS voting. 

We'll create a simple Twilio application to record and report votes
via SMS. 

Ballot Format
-------------

For this poll, ballots don't need a format. To vote, text your choice to your
Twilio number.

For example, to vote for Cal, text the following::

    cal

To see all the votes, we'll use a simple Python script and the `twilio-python
<https://github.com/twilio/twilio-python>`_ helper library.

.. code-block:: python

   from twilio.rest import TwilioRestClient

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   for msg in client.sms.messages.iter():
       print msg.body

The ``iter`` function efficiently fetches all your SMS messages via the Twilio
REST API. Under the covers, the function fetches pages of the `SMS
Messages list resource <http://www.twilio.com/docs/api/rest/sms#list>`_ as they
are needed.

However, this script will fail if you have multiple Twilio phone numbers. To
fix this, we'll filter messages based on the phone number they were sent to.

.. code-block:: python
   :emphasize-lines: 3, 7

   from twilio.rest import TwilioRestClient

   TWILIO_PHONE_NUMBER = "(999) 999 - 9999"

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   for msg in client.sms.messages.iter(to=TWILIO_PHONE_NUMBER):
       print msg.body

Still, we're only seeing the contents of the messages.

Tallying Votes
--------------

In our election, participants can only vote once. Therefore, each message
should count for a single vote. We'll use a default dictionary to keep track of
votes.

A Python ``defaultdict`` is a regular dictionary, but with default values for the keys.
For example, a regular dictionary will throw a ``KeyError`` if you access a key that
doesn't exist.

.. code-block:: python

    >>> s = {}
    >>> s['hey']
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    KeyError: 'hey'

A ``defaultdict`` will instead return the default value for the type of object it
contains.

.. code-block:: python

    >>> s = defaultdict(int)
    >>> s['hey']
    0

Instead of just printing the message body, we now use the message body as a key
for the vote dictionary.

.. code-block:: python
   :emphasize-lines: 2,6,10-

   from twilio.rest import TwilioRestClient
   from collections import defaultdict

   TWILIO_PHONE_NUMBER = "(999) 999 - 9999"

   votes = defaultdict(int)

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   for msg in client.sms.messages.iter(to=TWILIO_PHONE_NUMBER):
       votes[msg.body] += 1

   for vote, total in votes.items():
       print "{} {}".format(vote, total)

We can now see tallies for each vote. However, this code is very brittle. 
Let's normalize the message bodies so that similar votes (like for ``foo``
and ``Foo``) count for the same option.

.. code-block:: python
   :emphasize-lines: 11

   from twilio.rest import TwilioRestClient
   from collections import defaultdict

   TWILIO_PHONE_NUMBER = "(999) 999 - 9999"

   votes = defaultdict(int)

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   for msg in client.sms.messages.iter(to=TWILIO_PHONE_NUMBER):
       votes[msg.body.upper()] += 1

   for vote, total in votes.items():
       print "{} {}".format(vote, total)


Preventing Cheaters
-------------------

Cheaters never prosper, and currently they don't get caught either. Any person
can vote any number of times. We'll keep track of every number that's voted,
only allowing them a single vote. To do this, phone numbers will be added to a
set and checked before each vote is tallied.


.. code-block:: python
   :emphasize-lines: 7,12,13,16

   from twilio.rest import TwilioRestClient
   from collections import defaultdict

   TWILIO_PHONE_NUMBER = "(999) 999 - 9999"

   votes = defaultdict(int)
   voted = set()

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   for msg in client.sms.messages.iter(to=TWILIO_PHONE_NUMBER):
       if msg.from_ in voted:
           continue

       votes[msg.body.upper()] += 1
       voted.add(msg.from_)

   for vote, total in votes.items():
       print "{} {}".format(vote, total)


Graphing the Results
--------------------

No election is complete without graphs. Let's take the results from the
previous section and make some pretty graphs. We'll use the `Google Graph API
<https://developers.google.com/chart/image/docs/making_charts>`_ due to its
simplicity and price (free).

.. code-block:: python
   :emphasize-lines: 1,19-

   import urllib
   from twilio.rest import TwilioRestClient
   from collections import defaultdict

   TWILIO_PHONE_NUMBER = "(999) 999 - 9999"

   votes = defaultdict(int)
   voted = set()

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   for msg in client.sms.messages.iter(to=TWILIO_PHONE_NUMBER):
       if msg.from_ in voted:
           continue

       votes[msg.body.upper()] += 1
       voted.add(msg.from_)

   url = "https://chart.googleapis.com/chart"

   options = {
       "cht": "pc",
       "chs": "500x500",
       "chd": "t:" + ",".join(map(str, votes.values())),
       "chl": "|".join(votes.keys()),
   }

   print url + "?" + urllib.urlencode(options)


Existing Solutions
------------------

`Wedgies <http://wedgies.com/>`_ is a very similar concept built on top of
Twilio, but questions are limited to two answers. Great for simple surveys, but
not for elections.
