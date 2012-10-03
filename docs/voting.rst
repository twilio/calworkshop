.. _voting:

SMS Polling and Voting
======================

Whether at a Hackathon or a student group meeting, you'll often need to vote on
items. Elections, food, or nominations, all these situatins can be hanlded via
SMS voting. 

We'll create a simple Twilio application to record and report votes
via SMS. Our poll will be for a fictious hackathon call 'Sir Hackalot`. We'll
be voting on our favorite entries.

Ballot Format
-------------

For this poll, ballots don't need a format. You'll be voting for your favorite hacks at the 'Sir Hackalot' hackthon. To vote, just text in the name of your favorite hack.

For example, to vote for Twitter CLone team, text the following::

    twitter clone

To see all the votes, we'll use a simple Python script and the `twilio-python
<https://github.com/twilio/twilio-python>`_ helper library.

.. code-block:: python

   from twilio.rest import TwilioRestClient

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   for msg in client.sms.messages.iter():
       print msg

However, this script will fail if you have multiple Twilio phone numbers. To
fix this, we'll filter messages based on the phone number they were sent to.

.. code-block:: python
   :emphasize-lines: 5

   from twilio.rest import TwilioRestClient

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   for msg in client.sms.messages.iter(to="TWILIO PHONE NUMBER"):
       print msg.body

If we get enough votes, this script's output will be very difficult to understand.

Tallying Votes
--------------

.. code-block:: python
   :emphasize-lines: 2,4,7,8-10

   from twilio.rest import TwilioRestClient
   from collections import defaultdict

   votes = defaultdict(int)

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   for msg in client.sms.messages.iter(to="TWILIO PHONE NUMBER"):
       votes[msg.body] += 1

   for vote, total in votes.items():
       print "{} {}".format(vote, total)

validation and normalization

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


.. code-block:: python
   :emphasize-lines: 5,10,11,14

   from twilio.rest import TwilioRestClient
   from collections import defaultdict

   votes = defaultdict(int)
   voted = defaultdict(int)

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   for msg in client.sms.messages.iter(to="TWILIO PHONE NUMBER"):
       if voted[msg.from_] > 0:
           continue

       votes[msg.body.upper()] += 1
       voted[msg.from_] += 1

   for vote, total in votes.items():
       print "{} {}".format(vote, total)


Graphing the Results
--------------------

No election is complete without graphs. Let's take the results from the
previous section and make some pretty graphs. We'll use the `Google Graph API
<https://developers.google.com/chart/image/docs/making_charts>`_ due to its
simplicity and price (free).

.. code-block:: python

   from twilio.rest import TwilioRestClient
   from collections import defaultdict

   votes = defaultdict(int)
   voted = defaultdict(int)

   client = TwilioRestClient("ACCOUNT_SID", "AUTH_TOKEN")

   for msg in client.sms.messages.iter(to="TWILIO PHONE NUMBER"):
       if voted[msg.from_] > 0:
           continue

       votes[msg.body.upper()] += 1
       voted[msg.from_] += 1

   url = "https://chart.googleapis.com/chart"

   options = {
       "cht": "pc",
       "chs": "500x500",
       "chd": "t:" + ",".join(votes.values()),
       "chl": "|".join(votes.keys()),
   }

   print url + urlencode(options)


Existing Solutions
------------------

`Wedgies <http://wedgies.com/>`_ is a very similar concept build on top of
Twilio, but questions are limited to two answers. Great for simple surveys, but
not for elections.
