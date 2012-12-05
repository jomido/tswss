**tswss** is a Twisted Static & WebSocket Server. That is, it's a web server in Twisted (Python) that:

1. serves up initial static app content, and
2. communicates with that app via websockets thereafter

It's a minimal implementation.

It seems to me that Twisted ain't the cool kid on the block anymore. But at work I need a robust server that's proven. Twisted fits the bill.

This isn't meant to be a library that you just import and use. Rather, you're supposed to grab the code and run with it. (SLOC is itty-bitty.) The example works, huzzah!, but typically you'd use it as a base to make something real.

For my use case, I just want to write desktop apps going forward with web technologies. Twisted allows me to connect up any existing enterprise services to my web apps easily.

## Install'n It

1. Install [Python 2.7.x](http://www.python.org/download/releases/2.7.3/)
2. Install [Twisted](http://twistedmatrix.com/trac)
3. Install [Zope.Interface](http://pypi.python.org/pypi/zope.interface) (required by Twisted)
4. Install [AutobahnPython](http://www.autobahn.ws/python)

## Run'n It

1. You will need a web browser that [supports WebSockets](http://caniuse.com/#search=websocket)
2. Navigate to the directory where you installed/placed tswss
3. Enter the /test-app directory
4. Open app.html
5. Change 'my-machine-name' in the line 'App.connect("ws://my-machine-name:6789")' to whatever the name of your local machine is
6. Navigate to the root directory where server.py is located (one up)
7. Enter the command 'python server.py'
8. Open a WebSocket compatible browser and hit http://localhost:8000

## Configurin' It

1. Open server.py
2. Read, understand, and change - you can do it!

## Date'n It

This was made on the 5th of December, 2012. The versions of the software used at that time were:

1. Python: 2.7.3
2. Twisted: 12.0.0
3. Zope.Interface: 4.0.1
4. AutobahnPython: 0.5.2
5. Browser: Chrome 23.0, Firefox 15.0-18.0, Opera 12.11, Blackberry 7.0+, IE10 (not in Compat View - must be running in full IE10 mode (hit F12 for developer tools to make sure))

### Other Browsers

#### Safari/iOS

Safari 5.1.7 would not work (I believe due to it implementing an older version of the WebSocket spec). I hear Safari 6.0 works fine. Unfortunately I do not have access to an Apple OS to test this.

#### Android

No. I hear that either the latest Firefox, or Firefox dev channel for Android [has support for WebSockets](https://wiki.mozilla.org/Mobile/Platforms/Android). Unfortunately, I do not have access to an Android device to test this.
