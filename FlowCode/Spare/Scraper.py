import requests
from bs4 import BeautifulSoup
import os
import uuid
from DataObjects.Event import EventData
from DataObjects.Text import TextData
from DataObjects.Audio import AudioData
from DataObjects.Video import VideoData
from DataObjects.Image import ImageData


class ScraperAndSplitter:
    def __init__(self, baseURL, eventID):
        self.base_url = baseURL
        self.event_id = eventID
        self.parsed_data_folder = f'../ParsedData/{eventID}'
        os.makedirs(self.parsed_data_folder, exist_ok=True)

    def scrape_content(self):
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return self.extract_and_save_content(soup)

    def extract_and_save_content(self, soup):
        content_list = []

        text_content = soup.get_text()
        content_list.append(('text', text_content))

        for img in soup.find_all('img'):
            img_url = img.get('src')
            content_list.append(('image', img_url))

        for audio in soup.find_all('audio'):
            audio_url = audio.get('src')
            content_list.append(('audio', audio_url))

        for video in soup.find_all('video'):
            video_url = video.get('src')
            content_list.append(('video', video_url))

        for content_type, content in content_list:
            if content_type == 'text':
                self.save_text(content)
            elif content_type == 'image':
                self.save_image(content)
            elif content_type == 'audio':
                self.save_audio(content)
            elif content_type == 'video':
                self.save_video(content)

        return self.create_event_data(content_list)

    def save_text(self, content):
        unique_name = f"{uuid.uuid4()}.txt"
        text_filename = os.path.join(self.parsed_data_folder, unique_name)
        with open(text_filename, 'w', encoding='utf-8') as file:
            file.write(content)

    def save_image(self, img_url):
        img_response = requests.get(img_url)
        img_name = os.path.join(self.parsed_data_folder, os.path.basename(img_url))
        with open(img_name, 'wb') as file:
            file.write(img_response.content)

    def save_audio(self, audio_url):
        audio_response = requests.get(audio_url)
        audio_name = os.path.join(self.parsed_data_folder, os.path.basename(audio_url))
        with open(audio_name, 'wb') as file:
            file.write(audio_response.content)

    def save_video(self, video_url):
        video_response = requests.get(video_url)
        video_name = os.path.join(self.parsed_data_folder, os.path.basename(video_url))
        with open(video_name, 'wb') as file:
            file.write(video_response.content)

    def create_event_data(self, content_list):
        event_data = EventData(self.event_id)

        for content_type, content in content_list:
            if content_type == 'text':
                text_data = TextData(content, self.event_id, uuid.uuid4())  # Create a TextData object
                event_data.add_data(text_data)  # Use the add_data method
            elif content_type == 'image':
                image_data = ImageData(content, self.event_id, uuid.uuid4())  # Create an ImageData object
                event_data.add_data(image_data)  # Use the add_data method
            elif content_type == 'audio':
                audio_data = AudioData(content, self.event_id, uuid.uuid4())  # Create an AudioData object
                event_data.add_data(audio_data)  # Use the add_data method
            elif content_type == 'video':
                video_data = VideoData(content, self.event_id, uuid.uuid4())  # Create a VideoData object
                event_data.add_data(video_data)  # Use the add_data method

        return event_data


# Usage
if __name__ == "__main__":
    base_url = 'https://linkedin.com'  # Replace with your target URL
    event_id = '123456'  # Replace with your unique event ID
    scraper_and_splitter = ScraperAndSplitter(base_url, event_id)
    event_data_object = scraper_and_splitter.scrape_content()  # Returns the EventData object
    print(event_data_object)  # Optionally print or process the event_data_object
