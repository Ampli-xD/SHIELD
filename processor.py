import os
import mimetypes
import requests
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Import data objects
from Engine.DataObjects.Base import BaseData
from Engine.DataObjects.Event import EventData
from Engine.DataObjects.TextDataObject import TextData
from Engine.DataObjects.ImageDataObject import ImageData
from Engine.DataObjects.AudioDataObject import AudioData
from Engine.DataObjects.VideoDataObject import VideoData

# Import processors
from Engine.Processors.TextProcessing import ContextCombiner
from Engine.Processors.ImageProcessing import ImageProcessor
from Engine.Processors.AudioProcessing import AudioProcessor
from Engine.Processors.VideoProcessing import VideoProcessor

# Load environment variables
load_dotenv()
LLM_API_KEY = os.getenv("LLM_API_KEY")

class ProcessorMonitor:
    """Simple monitor class for processors to log progress"""
    def publish(self, objective, module):
        print(f"[{module}] {objective}")

# Initialize monitor
monitor = ProcessorMonitor()

def process_file(file_path: str, filename: str) -> List[BaseData]:
    """
    Process a file and create appropriate data objects based on file type
    
    Args:
        file_path: Path to the temporary file
        filename: Original filename
        
    Returns:
        List of data objects created from the file
    """
    # Generate a unique event ID for this processing session
    event_id = str(Path(filename).stem) + "_" + os.path.basename(file_path)[-8:]
    
    # Get file extension and MIME type
    file_ext = Path(filename).suffix.lower()
    mime_type, _ = mimetypes.guess_type(filename)
    file_path_obj = Path(file_path)
    
    data_objects = []
    
    try:
        # Text files
        if mime_type and mime_type.startswith('text/'):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text_content = f.read()
            
            text_data = TextData(file_path_obj, event_id)
            text_data.set_context(text_content)
            data_objects.append(text_data)
        
        # PDF files - treat as text for now
        elif file_ext == '.pdf':
            # Create a text data object since we don't have PDF-specific data object
            text_data = TextData(file_path_obj, event_id)
            # We'll use a placeholder context
            text_data.set_context(f"PDF file: {filename}")
            data_objects.append(text_data)
        
        # Images
        elif mime_type and mime_type.startswith('image/'):
            image_data = ImageData(file_path_obj, event_id)
            data_objects.append(image_data)
        
        # Audio
        elif mime_type and mime_type.startswith('audio/'):
            audio_data = AudioData(file_path_obj, event_id)
            data_objects.append(audio_data)
        
        # Video
        elif mime_type and mime_type.startswith('video/'):
            video_data = VideoData(file_path_obj, event_id)
            data_objects.append(video_data)
        
        # Other file types
        else:
            # Create a generic text data object with file info
            text_data = TextData(file_path_obj, event_id)
            text_data.set_context(f"Unsupported file format: {file_ext}")
            data_objects.append(text_data)
    
    except Exception as e:
        # Handle processing errors by creating a text data object with the error
        text_data = TextData(file_path_obj, event_id)
        text_data.set_context(f"Error processing file {filename}: {str(e)}")
        data_objects.append(text_data)
    
    return data_objects

def analyze_with_llm(event: EventData) -> str:
    """
    Analyze data objects in the event using LLM
    
    Args:
        event: The event with data objects to analyze
        
    Returns:
        Analysis result as a string
    """
    data_objects = event.get_all_data()
    
    if not data_objects:
        return "No data to analyze"
    
    try:
        # Process each data object based on its type
        for data_object in data_objects:
            if isinstance(data_object, TextData):
                # Text is already processed during file upload
                pass
                
            elif isinstance(data_object, ImageData):
                # Process image using ImageProcessor
                image_processor = ImageProcessor(api_key=LLM_API_KEY)
                image_processor.fetch_image_analysis(data_object)
                
            elif isinstance(data_object, AudioData):
                # Process audio using AudioProcessor
                audio_processor = AudioProcessor(api_key=LLM_API_KEY)
                audio_processor.fetch_audio_transcription(data_object)
                
            elif isinstance(data_object, VideoData):
                # Process video using VideoProcessor
                video_processor = VideoProcessor(api_key=LLM_API_KEY)
                video_processor.fetch_video_analysis(data_object)
        
        # Combine contexts from all data objects
        context_combiner = ContextCombiner()
        context_combiner.combine_contexts(event)
        
        # Return the combined context
        return event.get_combined_text()
        
    except Exception as e:
        error_message = f"LLM analysis failed: {str(e)}"
        print(error_message)
        return error_message