import gevent
from gevent.wsgi import WSGIServer
from gevent.queue import Queue
from gevent import pywsgi

from flask import Flask, Response, request

import time


class ServerSentEvent(object):

    def __init__(self, data):
        self.data = data
        self.event = None
        self.id = None
        self.desc_map = {
            self.data : "data",
            self.event : "event",
            self.id : "id"
        }

    def encode(self):
        if not self.data:
            return ""
        lines = ["%s: %s" % (v, k)
                 for k, v in self.desc_map.iteritems() if k]

        return "%s\n\n" % "\n".join(lines)

app = Flask(__name__)
subscriptions = []

# Client code consumes like this.
@app.route("/")
def index():
    debug_template = """
     <html>
       <head>
       </head>
       <body>
        <div style="vertical-align:middle">
            <div id="welcome">
                Welcome to Skill!
                <br>
                <img src="https://placeholdit.imgix.net/~text?txtsize=25&txt=Replace%20With%20Your%20Logo&w=180&h=120">
            </div>
            <div id="error">
                <span id="errMsg"></span>
                <br>
                <button onclick="goHome()">OK</button>
            </div>
            <div id="pay" style="display: none;">
                <span>Amount Due:</span> $ <span id="amount"></span>
                <br>
                <button onclick="payNow()">Pay Now</button>
                <button onclick="goHome()">Cancel</button>
            </div>
        </div>
        <script type="text/javascript">

        var timeoutID;
        var strAmount = '';
        var intAmount = 0;
        var evtSrc = new EventSource("/subscribe");

        evtSrc.onmessage = function(e) {
            console.log(e.data);
            strAmount = JSON.parse(e.data).amount
            intAmount = Math.round(strAmount * 100);
            document.getElementById("amount").innerHTML = strAmount;
            show(false, true, false);
            timeoutID = window.setTimeout(goHome, 60000);
        };

        var errorDesc = getUrlParameter('com.squareup.register.ERROR_DESCRIPTION');
        if(errorDesc) {
            document.getElementById("errMsg").innerHTML = errorDesc;
            show(false, false, true);
            timeoutID = window.setTimeout(goHome, 60000);
        }
        else {
            show(true, false, false);
        }

        function show(welcome, pay, error) {
            document.getElementById("welcome").style.display = (welcome ? 'block' : 'none');
            document.getElementById("pay").style.display = (pay ? 'block' : 'none');
            document.getElementById("error").style.display = (error ? 'block' : 'none');
        }

        function payNow() {
            window.clearTimeout(timeoutID);
            window.location = "intent:#Intent;" +
                "action=com.squareup.register.action.CHARGE;" +
                "package=com.squareup;" +
                "S.browser_fallback_url=https://192.168.4.69:5000;" +
                "S.com.squareup.register.WEB_CALLBACK_URI=https://192.168.4.69:5000;" +
                "S.com.squareup.register.CLIENT_ID=sq0idp-SN6X3UAclY2ZjF7PWfK2LQ;" +
                "S.com.squareup.register.API_VERSION=v1.3;" +
                "i.com.squareup.register.TOTAL_AMOUNT=" + intAmount +
                ";S.com.squareup.register.CURRENCY_CODE=USD;" +
                "S.com.squareup.register.TENDER_TYPES=com.squareup.register.TENDER_CARD;end";
        }

        function goHome() {
            window.clearTimeout(timeoutID);
            window.location = "/";
        }

        function getUrlParameter(name) {
            name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
            var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
            var results = regex.exec(location.search);
            return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
        };

        </script>
        <style>
            body {
                font-size: 30px;
                font-family: Helvetica
            }
            div {
                height: 200px;
                line-height: 200px;
                text-align: center;
                color: #89213a;
            }
            button {
                color: white;
                background-color: #89213a;
                border: 0;
                height: 50px;
                width: 200px;
                font-size: 20px;
            }
        </style>
       </body>
     </html>
    """
    return(debug_template)

@app.route("/debug")
def debug():
    return "Currently %d subscriptions" % len(subscriptions)

@app.route("/publish")
def publish():
    reqmsg = request.args.get('msg')
    if reqmsg is None:
        reqmsg = ''

    def notify():
        for sub in subscriptions[:]:
            sub.put(reqmsg)

    gevent.spawn(notify)

    return "OK"

@app.route("/subscribe")
def subscribe():
    def gen():
        q = Queue()
        subscriptions.append(q)
        try:
            while True:
                result = q.get()
                print result
                ev = ServerSentEvent(unicode(result))
                yield ev.encode()
        except GeneratorExit:
            subscriptions.remove(q)

    return Response(gen(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.debug = True
    server = pywsgi.WSGIServer(('', 5000), app, keyfile='server.key', certfile='server.crt')
    server.serve_forever()
    # Then visit https://localhost:5000 to subscribe
    # and send messages by visiting https://localhost:5000/publish?msg=<your message>
