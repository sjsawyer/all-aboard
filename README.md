# all-aboard

A sketchy bot which proved to be successful in discovering the sudden
availability of train tickets for a certain train.

![train](http://clipart-library.com/newhp/0-9960_train-clipart-steam-train-clipart.png)

## What Do It Do?

It was scheduled to poll a dynamic website via the selenium library using a
chrome webdriver in search of ticket availability for a certain date. Indeed,
we were only interested in a single date. Various channels were set up to
receive the output of certain events (literally Discord channels), including
the odd exception which popped up due to the target site receiving too much
traffic.

## Complexities?

This masterpiece was thrown together on WSL without an IDE, which proved to be
quite difficult -- the WSL part, that is. Turns out I needed to use WSL 2 which
uses an actual running VM. I did not even attempt to get any live demo using a
non-headless web browser working, but exporting the odd PNG did prove to be
useful. Oh, and note the version of the webdriver needs to match that of the
web browser exactly.

## Scheduling Via Cron (TLDR)

To start cron:

    sudo /etc/init.d/cron start

To edit cron:

    crontab -e

For example, to run every 5 minutes,

    */5 * * * * /path/to/all-aboard/cron.sh
