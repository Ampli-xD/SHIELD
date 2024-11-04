import json
import os

from PubSub import Subscriber


class Monitor:
    def __init__(self):
        self.subs = Subscriber()
        os.system("cls")

    def start_monitoring(self):
        self.receiver()

    def receiver(self):
        while True:
            message = self.subs.receive()
            timestamp = message["timestamp"]
            module = message["module"]
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

            output = f"""
[{timestamp}] [{module}] [{objective}]"""

            if data != "":
                output += f"Data:\n{json.dumps(data, indent=4)}\n"

            if extra != "":
                output += f"Extra: {extra}\n"

            print(output)


if __name__ == "__main__":
    monitor = Monitor()
    monitor.start_monitoring()
