What is gcsms?
==============

gcsms allows you to programmatically send SMS for free to anyone who has
a Google account. gcsms is written to present Google Calendars as
messaging lists, something akin to regular mailing lists, where users
who subscribe receive all the messages sent to the mailing list. In this
case, anyone who is subscribed to a messaging list will receive SMSes.
gcsms uses Google Calendar API v3 to create/delete calendars and events.
Everything that gcsms can do, can also be done through Google Calendar's
web interface. 

Why bother?
===========

Initially, this project came to being to cut on costs of monitoring the
health of a website by making use of the free SMS notification service
offered by Google Calendar, instead of using an SMS gateway like twilio
or tropo. Bells and whistles, such as ability to send to multiple
recipients was later added in order to create a generic multipurpose
tool.

Sold. How do I do it?
=====================

There are various scenarios in which gcsms can be used. We start with
the most simple one and build on that.

Scenario A (single subscriber)
------------------------------
You want to get an SMS every time your website returns a 5xx HTTP code.

You must set up a few things before using gcsms to send SMS:

1. Setup a Google account if you don't already have one
   (https://gmail.com).
2. In Google Calendar (https://calendar.google.com),
   under 'Calendar Settings' -> 'Mobile Setup', enter your mobile number
   and verify it.
3. In API Console (https://code.google.com/apis/console), under
   Services, enable 'Calendar API'.
4. In API Console, under 'API Access', create a new
   'Client ID for installed applications' with application type of
   'other' and note down the 'Client ID' and 'Client Secret'.
5. Edit `~/.gcsms` and enter the 'Client ID' and 'Client Secret' and
   save - see `sample.config` for the format of the config file
6. Run `python gcsms.py auth` and follow the instructions, granting
   calendar access to gcsms.

At this point, you no longer need to use the web interface - everything
can be done using gcsms commands. To avoid typing `python gcsms.py`, you
should put a link to gcsms.py in one of the appropriate directories in
`PATH`. Here's one way to do it, assuming `gcsms.py` is in your home
directory:

    $ GCSMS=~/gcsms.py
    $ chmod +x $GCSMS
    $ mkdir -p ~/bin
    $ ln -s $GCSMS ~/bin/gcsms
    $ echo 'export PATH="$PATH:~/bin"' >> ~/.bashrc

Let's create a new messaging list (ie Calendar):

    $ gcsms create web-health
    :hwernow_235nkjg@group.calendar.google.com

That long and ugly output that starts with `:` is the messaging list ID.
It's unique and is the preferred way of referring to messaging lists
when using gcsms in other scripts for automation. IDs always start with
`:`. Also, you can have multiple messaging lists with identical names
but each will have a unique ID.

You can see a list of all the messaging lists you have joined (which
includes all the ones you create/own):

    $ gcsms ls
    web-health

Using `ls` with `-l` option gives you a more detailed view:

    $ gcsms ls -l
    rwom  web-health  :hwernow_235nkjg@group.calendar.google.com

The first three letters indicate your access to the messaging list:

*  `r` means you can receive messages
*  `w` means you can send messages
*  `o` means you can manage other people's access and also delete the
   messaging list (using `gcsms rm`) which will delete it for everyone

`m` indicates that the messaging list is silenced (muted). In this mode,
you will not receive any SMSes until you _unmute_ the messaging list:

    $ gcsms unmute web-health
    $ gcsms ls -l
    rwo-  web-health  :hwernow_235nkjg@group.calendar.google.com

_Note: All messaging lists you create or join are muted by default._

At this stage, you can send yourself a message:

    $ gcsms send web-health 'Site down: 502'

You should receive an SMS shortly after the above command returns. But
have patience. There might be 5 to 30 seconds delay or sometimes more.
From time to time, you may receive multiple copies of the same message.
Unfortunately the promptness of the delivery cannot be controlled and if
your application requires a more timely delivery, you should consider an
SMS gateway service like twilio.

Scenario B (multiple subscribers)
---------------------------------

Alice, your business partner would also like to know when the website is
not feeling well.

First, Alice needs to do the steps to set up her API access (see the six
steps in scenario A). Next, you need to give her access to your
messaging list:

    [you]$ gcsms acl-set web-health alice.cooper@veryimp.bizo reader

The above command gives Alice permission to _only_ receive messages.

Alice needs to join your messaging list. She will need its unique ID.
You can find that out by using `gcsms ls -l`. Once Alice has the ID, she
can join and subsequently unmute the newly joined messaging list, ready
to receive SMSes:

    [alice]$ gcsms join :hwernow_235nkjg@group.calendar.google.com
    [alice]$ gcsms unmute web-health

Now, if you run `gcsms send web-health 'Site down: 502'`, both you and
Alice will receive an SMS.

A while later, Alice gets annoyed by all the SMSes and wants to stop
receiving them. She can either `gcsms mute` the messaging list. This
allows her to easily `unmute` it later. She could also `gcsms leave` the
messaging list. She can always `join` later provided her access is not
revoked by you (using `gcsms acl-rm`).

Scenario C (multiple subscribers using web interface)
-----------------------------------------------------

There are situations where the receivers don't have their API access
setup or don't have the environment to run gcsms. That is OK. You can
still use gcsms to send SMS to them. But they need to setup somethings
manually through the web interface.

As per scenario B, you must give each user access:

    $ gcsms acl-set web-health poor.david@veryimp.bizo reader
    $ gcsms acl-set web-health poorer.jimmy@veryimp.bizo reader

Now, if David and Jimmy log into their Google account and navigate to
https://calendar.google.com, they will see a new calendar named
`gcsms:web-health` added to their list of calendars. All calendars used
as messaging lists by gcsms are named with a prefix of `gcsms:`. In
fact, `gcsms ls` will not show you any calendars that doesn't follow
this convention.

David and Jimmy need to add an 'SMS Event reminder' with exactly '1
minute' setting. They can do that by going into 'Calendar Settings' >
'Calendars' > 'gcsms:web-health' > 'Reminders and notifications' tab.
It is needless to say, they must have already setup their mobile phone
number and verified it (see steps 1 and 2 in scenario A).

That's it! Like Alice, David and Jimmy will now receive an SMS every
time you issue `gcsms send web-health`.

Other matters
=============

We have pretty much covered all the commands. There are few more but you
can figure them out yourselves. Just run `gcsms -h` to find out more.

There are some caveats to using gcsms:

* Renaming a messaging list using `gcsms rename` only affects the name
  in your list.
* More to go here ...
