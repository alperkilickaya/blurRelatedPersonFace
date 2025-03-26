from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil
from datetime import datetime
from .face_blur import find_and_blur_face
import json

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/api/photos", StaticFiles(directory="data"), name="photos")

# Data models
class Student(BaseModel):
    name: str
    class_name: str
    blur_face: bool = True

class ClassPhoto(BaseModel):
    class_name: str
    blur_students: List[str]

# Data storage
STUDENTS_FILE = "data/students.json"
PROFILE_PHOTOS_DIR = "data/profile_photos"
CLASS_PHOTOS_DIR = "data/class_photos"
os.makedirs(PROFILE_PHOTOS_DIR, exist_ok=True)
os.makedirs(CLASS_PHOTOS_DIR, exist_ok=True)

def get_class_photo_dir(class_name: str) -> str:
    """Creates and returns the photo directory for a class."""
    class_dir = os.path.join(CLASS_PHOTOS_DIR, class_name)
    os.makedirs(class_dir, exist_ok=True)
    return class_dir

def load_students():
    """Load student data from JSON file."""
    if os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_students(students):
    """Save student data to JSON file."""
    with open(STUDENTS_FILE, 'w') as f:
        json.dump(students, f)

# API endpoints
@app.post("/api/students")
async def add_student(student_data: str = Form(...), photo: UploadFile = File(...)):
    # Parse JSON string
    student = json.loads(student_data)
    
    # Save photo
    photo_path = f"data/profile_photos/{student['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    with open(photo_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)
    
    # Save student information
    students = load_students()
    students[student['name']] = {
        "class_name": student['class_name'],
        "photo_path": photo_path,
        "blur_face": student['blur_face']
    }
    save_students(students)
    
    return {"message": "Student added successfully"}

@app.get("/api/students")
async def get_students():
    return load_students()

@app.post("/api/photos")
async def process_photo(photo: UploadFile = File(...), class_name: str = Form(...)):
    result_path = None
    
    try:
        # Create class directory
        class_dir = get_class_photo_dir(class_name)
        
        # Load students for this class
        students = load_students()
        class_students = {name: data for name, data in students.items() if data["class_name"] == class_name}
        
        print(f"Processing photo for class: {class_name}")
        print(f"Found {len(class_students)} students in class")
        
        # Process photo for each student
        any_face_blurred = False
        
        # Save the original photo first
        result_path = os.path.join(class_dir, f"{class_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
        with open(result_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
        
        for student_name, student_data in class_students.items():
            if student_data["blur_face"]:
                print(f"Processing blur for student: {student_name}")
                print(f"Student photo path: {student_data['photo_path']}")
                try:
                    find_and_blur_face(result_path, student_data["photo_path"], result_path)
                    any_face_blurred = True
                except Exception as e:
                    print(f"Error processing face for student {student_name}: {str(e)}")
                    raise HTTPException(
                        status_code=400,
                        detail=f"Could not find a matching face for student {student_name}. Please try again with a clearer photo."
                    )
            else:
                print(f"Skipping blur for student: {student_name} (blur_face=False)")
        
        if not any_face_blurred:
            raise HTTPException(
                status_code=400,
                detail="No faces were blurred in the photo. Please try again with a clearer photo."
            )
        
        return {"result_path": result_path.replace("data/", "")}
        
    except Exception as e:
        # Clean up result file in case of error
        if result_path and os.path.exists(result_path):
            os.remove(result_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/classes")
async def get_classes():
    students = load_students()
    return list(set(data["class_name"] for data in students.values()))

@app.post("/api/reset")
async def reset_all():
    """Reset all data: delete all photos and students.json"""
    try:
        # Delete all files in profile_photos directory
        for file in os.listdir(PROFILE_PHOTOS_DIR):
            file_path = os.path.join(PROFILE_PHOTOS_DIR, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        # Delete all files in class_photos directory
        for class_dir in os.listdir(CLASS_PHOTOS_DIR):
            class_path = os.path.join(CLASS_PHOTOS_DIR, class_dir)
            if os.path.isdir(class_path):
                for file in os.listdir(class_path):
                    file_path = os.path.join(class_path, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                os.rmdir(class_path)
        
        # Delete students.json if exists
        if os.path.exists(STUDENTS_FILE):
            os.remove(STUDENTS_FILE)
        
        return {"message": "All data reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 