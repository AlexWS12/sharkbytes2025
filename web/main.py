from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import tempfile
import sys

# Add gemini module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gemini.gemini_description import analyze_security_image

# Load environment variables
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# Add CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Event model
class Event(BaseModel):
    id: Optional[int] = None
    timestamp: Optional[str] = None
    event_type: str
    description: str
    severity: str
    image_url: Optional[str] = None


class EventCreate(BaseModel):
    event_type: str
    description: str
    severity: str = "info"


class FrameAnalysisResponse(BaseModel):
    event_id: int
    timestamp: str
    analysis: str
    severity: str
    status: str


@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok"}


@app.get("/anomalies")
def get_anomalies(limit: Optional[int] = 50):
    """
    Get anomaly events (alias for /events endpoint).
    Used by the frontend AnomalyLog component.
    """
    return get_events(limit=limit)


class ControlCommand(BaseModel):
    command: str


@app.post("/control")
def camera_control(command: ControlCommand):
    """
    Handle camera control commands from the frontend.

    Commands:
    - toggle_lock: Toggle auto-tracking on/off
    - center: Center the camera servos
    - pan_left, pan_right: Pan camera left or right
    - tilt_up, tilt_down: Tilt camera up or down
    """
    # This is a placeholder - you'll need to integrate with your sentry system
    # For now, just acknowledge the command
    print(f"[CONTROL] Received command: {command.command}")

    # TODO: Send command to the sentry system via socket/queue/shared state
    # For example, you could use Redis, a message queue, or a shared file

    return {"status": "success", "command": command.command}


@app.get("/video_feed")
def video_feed():
    """
    Stream video feed from the camera.
    This is a placeholder - you'll need to implement actual video streaming.

    For MJPEG streaming, you would use StreamingResponse with a generator function.
    """
    # TODO: Implement video streaming from the sentry camera
    # Example using StreamingResponse:
    # from fastapi.responses import StreamingResponse
    # return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

    return {"status": "not_implemented", "message": "Video streaming endpoint - to be implemented"}


@app.get("/events", response_model=List[Event])
def get_events(limit: Optional[int] = 10, event_type: Optional[str] = None):
    """
    Get security events from Supabase.

    Parameters:
    - limit: Maximum number of events to return (default: 10)
    - event_type: Filter by event type (optional)
    """
    try:
        # Build query
        query = supabase.table("events").select("*").order("timestamp", desc=True).limit(limit)

        # Add filter if event_type specified
        if event_type:
            query = query.eq("event_type", event_type)

        # Execute query
        response = query.execute()

        return response.data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching events: {str(e)}")


@app.post("/events", response_model=Event)
def create_event(event: EventCreate):
    """
    Create a new security event.

    This endpoint allows the sentry system to log events to the database.
    """
    try:
        # Add timestamp
        event_data = event.model_dump()
        event_data["timestamp"] = datetime.now().isoformat()

        # Insert into Supabase
        response = supabase.table("events").insert(event_data).execute()

        if response.data:
            return response.data[0]
        else:
            raise HTTPException(status_code=500, detail="Failed to create event")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating event: {str(e)}")


@app.post("/analyze-frame", response_model=FrameAnalysisResponse)
async def analyze_frame(file: UploadFile = File(...)):
    """
    Receive a frame from the sentry system, analyze it with Gemini Vision,
    store the image in Supabase Storage, and store the analysis result in Supabase.

    Parameters:
    - file: Image file (JPEG, PNG, etc.)

    Returns:
    - Analysis result with event ID and description
    """
    temp_path = None
    try:
        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_path = temp_file.name
            content = await file.read()
            temp_file.write(content)

        # Use the existing analyze_security_image function
        result = analyze_security_image(temp_path)

        # Check if analysis was successful
        if result["status"] != "success":
            raise HTTPException(
                status_code=500,
                detail=f"Gemini analysis failed: {result.get('error', 'Unknown error')}"
            )

        analysis_text = result["analysis"]

        # Determine severity based on keywords in the analysis
        severity = "info"
        analysis_lower = analysis_text.lower()

        if any(keyword in analysis_lower for keyword in ["alert", "suspicious", "unusual", "concern"]):
            severity = "warning"
        elif any(keyword in analysis_lower for keyword in ["danger", "threat", "emergency", "critical"]):
            severity = "critical"

        # Upload image to Supabase Storage
        timestamp = datetime.now()
        timestamp_str = timestamp.isoformat()

        # Create a unique filename with timestamp
        file_extension = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
        storage_filename = f"frame_{timestamp.strftime('%Y%m%d_%H%M%S')}_{timestamp.microsecond}{file_extension}"

        # Upload to Supabase Storage bucket using the content we already read
        supabase.storage.from_("security-frames").upload(
            path=storage_filename,
            file=content,
            file_options={"content-type": file.content_type or "image/jpeg"}
        )

        # Get public URL for the uploaded image
        image_url = supabase.storage.from_("security-frames").get_public_url(storage_filename)

        # Store the analysis as an event in Supabase
        event_data = {
            "event_type": "vision_analysis",
            "description": analysis_text,
            "severity": severity,
            "timestamp": timestamp_str,
            "image_url": image_url
        }

        db_response = supabase.table("events").insert(event_data).execute()

        if not db_response.data or len(db_response.data) == 0:
            raise HTTPException(status_code=500, detail="Failed to store analysis in database")

        event_record = db_response.data[0]
        event_id = event_record.get("id", 0)

        return FrameAnalysisResponse(
            event_id=event_id,
            timestamp=timestamp_str,
            analysis=analysis_text,
            severity=severity,
            status="success"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing frame: {str(e)}")

    finally:
        # Clean up temporary file
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)


app.mount("/", StaticFiles(directory="web/static/dist", html=True), name="frontend")