#!/bin/env python
import os
from gevent import monkey
monkey.patch_all()
from app import create_app, socketio

app = create_app(True)

if __name__ == '__main__':

    socketio.run(app, **{"heartbeat_interval": 1, "heartbeat_timeout": 10})
