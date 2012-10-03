.. _quickstart:

Twilio Quickstart
=================

The next section will take you on a whirlwind tour of the features of the
Twilio API. You'll learn how to make phones ring, send text messages, and
record voice messages. 

Make sure you've completed the :ref:`setup` section before continuing.

Create a Twilio Account
-----------------------

First, `sign up`_ for a free Twilio account. You won't need a credit card, but
you will need a phone number to prove you aren't a robot. Once you've signed
up, you'll have your own Twilio phone number. We'll use this number for the
rest of the workshop.

.. _sign up: https://www.twilio.com/try-twilio

After you've created your account and verified your phone number, you should
end up at a screen that looks like this.

.. image:: _static/testdrive.png

This is your first chance to test out what Twilio can do. Go ahead and setup a
thing for each button. You should send yourself a text message, recieve a call, and text in.

These things are great, but how do you do them from code, not a web page?


Hello World
-----------

You've recieved your own text message, now let's send it your self. Open the
``send_sms.py`` file in your text editor. First, replace the dummy account
credentials with those of your own. Your account credentials can be found `on
your Twilio account dashboard <>`, right at the top

.. code-block:: python

    import twilio

    TWILIO_ACCOUNT_SID = "YOUR ACCOUNT SID"
    TWILIO_AUTH_TOKEN = "YOUR AUTH TOKEN"

On the next line, replace the ``to`` number with the number you used to sign up
with Twilio. The ``from_`` number should be your new Twilio number. If you
can't remember it, will be in the entry in the `numbers <>`_ section of your
account dashbouad.

Pick any message less than 140 characters to serve as the body.

.. code-block:: python

    client.sms.messages.create(to='', from_='', body='')

We're now ready to send that SMS message

.. code-block:: bash

    $ python send_sms.py

Your phone should be getting a message in a few seconds.

Hello Monkey
------------

Making a phone call is just as easy. First
Just use the demo url


Introduction to TwiML
---------------------

* Say
* Play
* Gather
* Record
* Dial

Twimlbin
~~~~~~~~
Custom TwiML yo
handle errors here


Call Forwarding
---------------

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
      <Dial>YOUR PHONE NUMBER</Dial>
    </Resposne>

Save this URL, as we'll be using it later


Voicemail
---------

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
      <Say>After the beep, record your message</Say>
      <Record/>
    </Resposne>


Again, save this URL.


Private Conference Line
-----------------------

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
      <Dial>
        <Conference>vip</Conference>
      </Dial>
    </Resposne>

And no surprise here, but save this URL as well.

Swiss-Army Phone Number
-----------------------

Equipped with the knowledge of TwiML, you can now bend your Twilio phone number to your will. You've forwarded a call, recorded a message, and started a private conference line. Your phone is now your's to control.

But don't think we're done yet, our second act will be creating application for :ref:`voting`.
