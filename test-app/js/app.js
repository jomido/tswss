/* ////////////////////////////////////////////////////////////////////////////

A minimal websocket enabled app                copyright Jonathan Dobson, 2012
------------------------------------------------------------------------------
                                                                  LICENSE: MIT

//////////////////////////////////////////////////////////////////////////// */

var App = (function (me) {

	// App Variables
	// ========================================================================

	// Substitute the name of your local machine or domain here:
	//
	//  "ws://mycomp:6789"
	//  "ws://www.mysite.com:6789"

	me._default_ws_uri = "ws://my-machine-name:6789";

	me.init = function () {

		// Initialize the app
		// ====================================================================

		// Nothing to initialize yet
	}

	me.connect = function (ws_uri) {

		// Connect the App to server via WebSocket, and hook up the websocket's
		// callbacks for onmessage, onopen, onclose, and onerror.
		// ====================================================================

		if (!("WebSocket" in window)) {
			console.log("No WebSocket support.");
			return;
	    }

	    if (me.webSocket !== undefined) {

			if (me.webSocket.readyState === WebSocket.CONNECTING) {
			  	console.log("Already connecting...");
			  	return;
			}

			if (me.webSocket.readyState === WebSocket.OPEN) {
			  	console.log("Already open...");
			  	return;
			}

			me.disconnect();
	    }

	    if (ws_uri === undefined) {

			ws_uri = me._default_ws_uri;
	    }

	    console.log("Attempting to connect to...", ws_uri);
		me.webSocket = new WebSocket(ws_uri);

	    if (me.webSocket === undefined) return;

	    me.webSocket.onmessage = function(e) {
			try {
			    var jsonData = JSON.parse(e.data);
			}
			catch (err) {
			    console.log(err);
			    console.log("Received bad data:");
			    console.log(e.data);
			    return;
			}

			me.receive(jsonData);
	    }

	    me.webSocket.onopen = function() {
			 console.log("webSocket opened");

			 msg = {
				content: "I am alive!"
			 }

			 me.send(msg)
	    }

	    me.webSocket.onclose = function() {
	    	// One could possible attempt reconnects here
			console.log("webSocket closed");
	    }

	    me.webSocket.onerror = function (e) {
			me.handleErrors(e);
	    }

	}

	me.isConnected = function () {
	    return me.webSocket.readyState === 1;
	}

	me.receive = function (msg) {

	    // Receive messages from the server
	    // ====================================================================

	    console.log("Received message: ");
	    console.log(msg);

	    if ("number" in msg) {
	    	var magicNumber = document.getElementById('magic-number');
	    	magicNumber.innerHTML = "My magic number is " + msg.number + ".";
	    }

	}

	me.send = function (msg) {

	    // Send messages to the server
	    // ====================================================================

	    if (!me.isConnected()) me.connect();

	    // NOTE: will this lose messages, because there's no guarantee on how
	    // long it may take to connect? Messages should be buffered if they
	    // cannot be sent immediately.

	    // NOTE: apparently, if the socket is closed the ws.bufferedAmount
	    // property continues to climb when calling send(). So perhaps this is
	    // already taken care of?

	    me.webSocket.send(JSON.stringify(msg))
	    console.log("Sent server a message:");
	    console.log(msg);

	}

	me.handleErrors = function (e) {

		// Handle comm errors
		// ====================================================================

	    // TODO: handle them
	    console.log("WebSocket error:");
	    console.log(e.data);
	}

	me.disconnect = function () {

		// Disconnect the app from the server
		// ====================================================================

	    me.webSocket.close();

	}

	return me;

})(App || {});