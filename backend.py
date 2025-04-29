# get the file
# check media type 
# create a dataobject of it
# send the dataobject to the respective processor
# process the dataobject
# call the LLm scoring
# return the results

import json
import os
import time
import uuid

from Engine.DataObjects import Event
from Engine.Launcher.FileSegregator import FileSegregator
from Engine.LLMHandler.MultiSetLLMScoring import LLMScoring
from Engine.Processors import AudioProcessing, ImageProcessing, VideoProcessing
from Engine.Storage.SupabaseHandler import SupabaseHandler

event_id = int(str(uuid.uuid4().int)[:8])
event = Event.EventData(event_id=event_id)

# Example usage of SupabaseHandler
supabase_url = "your_supabase_url"
supabase_key = "your_supabase_key"
bucket_name = "your_bucket_name"
file_path = "path_to_your_file"

try:
    # Initialize the SupabaseHandler
    storage_handler = SupabaseHandler(supabase_url, supabase_key)
    
    # Upload a file
    file_url = storage_handler.upload_file(file_path, bucket_name)
    print(f"File uploaded successfully. Public URL: {file_url}")
    
    # Additional operations:
    # Get file URL
    # url = storage_handler.get_file_url("example.jpg", bucket_name)
    
    # Download file
    # storage_handler.download_file("example.jpg", bucket_name, "downloaded_example.jpg")
    
    # Delete file
    # storage_handler.delete_file("example.jpg", bucket_name)
    
except Exception as e:
    print(f"Error: {e}")

