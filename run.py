#!/bin/env python
from gevent import monkey
monkey.patch_all()
from app import create_app, socketio

app = create_app(True)

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    socketio.run(app)
