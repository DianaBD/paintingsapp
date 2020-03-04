from flask import Flask, render_template, request, make_response, g
from redis import Redis
import os
import socket
import random
import json

option_a1 = os.getenv('OPTION_A1', "")
option_r1 = os.getenv('OPTION_R1', "")
hostname = socket.gethostname()

app = Flask(__name__)

def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis

@app.route("/", methods=['POST','GET'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote11 = None

    if request.method == 'POST':
        redis = get_redis()
        vote11 = request.form['vote11']
        data = json.dumps({'voter_id': voter_id, 'vote11': vote11})
        redis.rpush('votes', data)

    resp = make_response(render_template(
        'index.html',
        option_a1=option_a1,
        option_r1=option_r1,
        hostname=hostname,
        vote11=vote11,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
