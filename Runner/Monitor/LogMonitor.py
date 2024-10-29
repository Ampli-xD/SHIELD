import json

from PubSub import Subscriber


class Monitor:
    def __init__(self):
        self.subs = Subscriber()

    def start_monitoring(self):
        self.receiver()

    def receiver(self):
        while True:
            message = self.subs.receive()
            timestamp = message["timestamp"]
            objective = message["objective"]
            data = message["data"]
            extra = message["extra"]
            # {
            #     "timestamp": timestamp,
            #     "objective": objective,
            #     "module": module,
            #     "data": data,
            #     "extra":extra
            # }
            print(f"""
[{timestamp}] [{objective}]
Data:
{json.dumps(data, indent=4)}

Extra: {extra}
""")


if __name__ == "__main__":
    monitor = Monitor()
    monitor.start_monitoring()
