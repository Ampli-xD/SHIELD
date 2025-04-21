import csv
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
            try:
                message = self.subs.receive()
                timestamp = message["timestamp"]
                module = message["module"]
                objective = message["objective"]
                data = message["data"]
                extra = message["extra"]
                if data != "":
                    self.append_to_csv("storage.csv", data)

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
            except:
                pass

    @staticmethod
    def append_to_csv(file_path, data):
        file_exists = os.path.exists(file_path)
        header = ['serial_id', 'filename', 'sexually_explicit_material', 'violence_and_terrorism',
                  'self_harm_and_suicide',
                  'child_abuse_and_exploitation', 'racial_slurs', 'hate_speeches', 'substance_abuse', 'body_shaming',
                  'homophobic_content', 'transphobic_content', 'sexist_content', 'harassment', 'cyberbullying',
                  'misinformation_and_fake_news', 'invasive_privacy_violation', 'type', 'time']

        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)

            if not file_exists and header:
                writer.writerow(header)

            row = [data['serial_id'], data['filename']]
            for key, value in data['score'].items():
                row.append(value)
            row.append(data['type'])
            row.append(data['time'])

            writer.writerow(row)


if __name__ == "__main__":
    monitor = Monitor()
    monitor.start_monitoring()

