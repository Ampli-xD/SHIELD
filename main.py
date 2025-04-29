import os
import uuid
import tempfile
from typing import Dict, Optional, List
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from storage import SupabaseHandler
from processor import process_file, analyze_with_llm
from Engine.DataObjects.Event import EventData

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Initialize storage handler
storage = SupabaseHandler(SUPABASE_URL, SUPABASE_KEY)

# Create FastAPI app
app = FastAPI(title="Document Analysis API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory event storage
events: Dict[str, EventData] = {}

# Response models
class UploadResponse(BaseModel):
    event_id: str
    message: str

class AnalysisResponse(BaseModel):
    event_id: str
    status: str
    result: Optional[str] = None

class EventSummary(BaseModel):
    event_id: str
    num_objects: int

@app.get("/")
async def root():
    return {"message": "Document Analysis API"}

@app.post("/upload/", response_model=UploadResponse)
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # Generate event ID
    event_id = str(uuid.uuid4())
    
    # Create event data object
    event = EventData(event_id)
    events[event_id] = event
    
    # Save file to temporary location
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp_file_path = temp.name
            content = await file.read()
            temp.write(content)
        
        # Upload to Supabase storage
        file_path = f"{event_id}/{file.filename}"
        storage.upload_file(temp_file_path, BUCKET_NAME)
        
        # Process in background
        background_tasks.add_task(
            process_and_analyze, 
            event_id, 
            file.filename, 
            temp_file_path
        )
        
        return UploadResponse(
            event_id=event_id,
            message="File uploaded and processing started"
        )
    
    except Exception as e:
        if event_id in events:
            del events[event_id]
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

@app.get("/status/{event_id}", response_model=AnalysisResponse)
async def get_analysis_status(event_id: str):
    if event_id not in events:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event = events[event_id]
    
    # Check if processing is complete (has combined text)
    if event.get_combined_text():
        return AnalysisResponse(
            event_id=event_id,
            status="complete",
            result=event.get_combined_text()
        )
    else:
        return AnalysisResponse(
            event_id=event_id,
            status="processing"
        )

@app.get("/events/", response_model=List[EventSummary])
async def list_events():
    return [
        EventSummary(
            event_id=event_id,
            num_objects=event.get_number_of_data_objects()
        )
        for event_id, event in events.items()
    ]

async def process_and_analyze(event_id: str, filename: str, file_path: str):
    try:
        if event_id not in events:
            return
        
        event = events[event_id]
        
        # Process file based on type
        data_objects = process_file(file_path, filename)
        
        # Add data objects to event
        for data_object in data_objects:
            event.add_data(data_object)
        
        # Analyze with LLM
        result = analyze_with_llm(event)
        
        # Store result
        event.set_combined_text(result)
        
    except Exception as e:
        print(f"Processing error: {str(e)}")
        # In case of error, keep the event but mark it as failed
        if event_id in events:
            events[event_id].set_combined_text(f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)