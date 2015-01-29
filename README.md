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

But before anything, install gcsms:

    $ pip install gcsms

gcsms is also available in [AUR][].

Scenario A (single subscriber)
------------------------------
You want to get an SMS every time your website returns a 5xx HTTP code.

You must set up a few things before using gcsms to send SMS:

1. Setup a Google account if you don't already have one
   (https://gmail.com).
2. In Google Calendar (https://calendar.google.com),
   under 'Calendar Settings' -> 'Mobile Setup', enter your mobile number
   and verify it.
3. In API Console (https://code.google.com/apis/console), click 'Create
   Project'
   and enable 'Calendar API'.
4. In API Console, under 'API Access', click 'Create an OAuth 2.0 client
   ID...' and input 'gcsms' as Product Name. Click 'Next' and under
   'Application type' choose 'Installed application'. It should default
   to 'Other' in 'Installed application type' section. Finalize by
   clicking 'Create Client ID' and note down 'Client ID' and 'Client
   Secret' from the following window.
5. Edit `~/.gcsms` and enter the 'Client ID' and 'Client Secret' and
   save - see [sample.config][sample] for the format of the config file
6. Run `gcsms.py auth` and follow the instructions, granting calendar
   access to gcsms.

At this point, you no longer need to use the web interface - everything
can be done using gcsms commands. Let's create a new messaging list (ie
Calendar):

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

**Note: All messaging lists you create or join are muted by default.**

At this stage, you can send yourself a message:

    $ gcsms send web-health 'Site down: 502'

You should receive an SMS shortly after the above command returns. But
have patience. There might be 5 to 30 seconds delay or sometimes more.
From time to time, you may receive multiple copies of the same message.
Unfortunately the promptness of the delivery cannot be controlled and if
your application requires a more timely delivery, you should consider
paying for use of an SMS gateway service like twilio.

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

Notes:

* Renaming a messaging list using `gcsms rename` only affects the name
  in your list.
* You can import `gcsms` as a python module and use `GCSMS` class to do
  anything you can do with the command line program.
* If you have a Google Apps for Business account, in order to be able to
  allow users outside of your domain to receive SMS or send SMS to
  messaging lists you create, you must do the following:
  - Go to Google Apps cpanel (https://www.google.com/a/cpanel/name.com)
  - Go to 'Settings' tab > 'Calendar' settings
  - Under 'External Sharing options for primary calendars', select any
    option other than the first one ('Only free/busy information')
    depending on the extent you wish to give outsiders access.

Contributing
============

_contribution instructions originally written by Linus Torvalds_

If you want to contribute code, please either send signed-off patches or
a pull request with signed-off commits. If you don't sign off on them,
we will not accept them. This means adding a line that says
"Signed-off-by: Name <email>" at the end of each commit, indicating that
you wrote the code and have the right to pass it on as an open source
patch.

See: http://gerrit.googlecode.com/svn/documentation/2.0/user-signedoffby.html

Also, please write good git commit messages. A good commit message
looks like this:

    Header line: explaining the commit in one line
    
    Body of commit message is a few lines of text, explaining things
    in more detail, possibly giving some background about the issue
    being fixed, etc etc.
    
    The body of the commit message can be several paragraphs, and
    please do proper word-wrap and keep columns shorter than about
    74 characters or so. That way "git log" will show things
    nicely even when it's indented.
    
    Reported-by: whoever-reported-it
    Signed-off-by: Your Name <youremail@yourhost.com>

where that header line really should be meaningful, and really should be
just one line.  That header line is what is shown by tools like gitk and
shortlog, and should summarize the change in one readable line of text,
independently of the longer explanation.

[sample]: https://github.com/oxplot/gcsms/blob/master/sample.config
[AUR]: https://aur.archlinux.org/packages/gcsms-git/
