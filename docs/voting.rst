.. _voting:

SMS Polling and Voting
======================

Whether at a Hackathon or a student group meeting, you'll often need to vote on
items. Elections, food, or nominations, all these situatins can be hanlded via
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

However, this script will fail if you have multiple Twilio phone numbers. To
fix this, we'll filter messages based on the phone number they were sent to.

.. code-block:: python
   :emphasize-lines: 5

   from twilio.rest import TwilioRestClient

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   for msg in client.sms.messages.iter(to="TWILIO PHONE NUMBER"):
       print msg.body

Still, we're only seeing the contents of the messages.

Tallying Votes
--------------

In our election, participants can only vote once. Therefore, each message
should count for a single vote. We'll use a default dictionary to keep track of
votes.

A defaultdict is a regular dictionary, but with default values for the keys.
For example, a regular dicionary will throw a KeyError if you access a key that
doesn't exist.

.. code-block:: python

    >>> s = {}
    >>> s['hey']
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    KeyError: 'hey'

A defaultdict will instead return the default value for the type of object it
contains.

.. code-block:: python

    >>> s = defaultdict(int)
    >>> s['hey']
    0

Instead of just printing the message body, we now use the message body as a key
for the vote dictionary.

.. code-block:: python
   :emphasize-lines: 2,4,7,8-

   from twilio.rest import TwilioRestClient
   from collections import defaultdict

   votes = defaultdict(int)

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   for msg in client.sms.messages.iter(to="TWILIO PHONE NUMBER"):
       votes[msg.body] += 1

   for vote, total in votes.items():
       print "{} {}".format(vote, total)

We can now see tallies. However, this code is very brittle. Votes for ``foo``
and ``Foo``. Let's normalize the message bodies so that similar votes count for
the same option.

.. code-block:: python
   :emphasize-lines: 9

   from twilio.rest import TwilioRestClient
   from collections import defaultdict

   votes = defaultdict(int)

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   for msg in client.sms.messages.iter(to="TWILIO PHONE NUMBER"):
       votes[msg.body.upper()] += 1

   for vote, total in votes.items():
       print "{} {}".format(vote, total)


Preventing Cheaters
-------------------

Cheaters never propser, and currently thet don't get caught either. Any person
can vote any number of times. We'll keep track of every number that's voted,
only allowing them a single vote. To do this, phone numbers will be added to a
set and checked before each vote is tallied.


.. code-block:: python
   :emphasize-lines: 5,10,11,14

   from twilio.rest import TwilioRestClient
   from collections import defaultdict

   votes = defaultdict(int)
   voted = set()

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   for msg in client.sms.messages.iter(to="TWILIO PHONE NUMBER"):
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
   :emphasize-lines: 1,17-

   import urllib
   from twilio.rest import TwilioRestClient
   from collections import defaultdict

   votes = defaultdict(int)
   voted = set()

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   for msg in client.sms.messages.iter(to="TWILIO PHONE NUMBER"):
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

`Wedgies <http://wedgies.com/>`_ is a very similar concept build on top of
Twilio, but questions are limited to two answers. Great for simple surveys, but
not for elections.
