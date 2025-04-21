import json
from datetime import datetime

import zmq

log_port = 5555


class Publisher:
    def __init__(self, port=log_port):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.address = f"tcp://*:{port}"
        self.socket.bind(self.address)
        data_to_send = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "objective": "MONITOR LOG",
            "module": "PubSub",
            "data": {".": f"Publisher initialized on port {port}"},
            "extra": ""
        }
        self.socket.send(json.dumps(data_to_send).encode('utf-8'))

    def publish(self, timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), objective="log", module="", data="",
                extra=""):
        data_to_send = {
            "timestamp": timestamp,
            "objective": objective,
            "module": module,
            "data": data,
            "extra": extra
        }
        self.socket.send(json.dumps(data_to_send).encode('utf-8'))

    # {
    #     "timestamp": timestamp,
    #     "objective": objective,
    #     "module": module,
    #     "data": data,
    #     "extra":extra
    # }

    def close(self):
        self.socket.close()
        self.context.term()


class Subscriber:
    def __init__(self, port=log_port):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(f"tcp://localhost:{port}")
        self.socket.subscribe("")
        print(f"Subscriber initialized on port {port}")

    def receive(self):
        while True:
            try:
                message = self.socket.recv_json()
                return message
            except zmq.ZMQError as e:
                pass
                # print(f"Error receiving message: {e}")
                # break

    def close(self):
        self.socket.close()
        self.context.term()
