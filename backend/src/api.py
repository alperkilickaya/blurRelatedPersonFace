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

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Statik dosyaları servis et
app.mount("/api/photos", StaticFiles(directory="data"), name="photos")

# Veri modelleri
class Student(BaseModel):
    name: str
    class_name: str
    blur_face: bool = True

class ClassPhoto(BaseModel):
    class_name: str
    blur_students: List[str]

# Veri depolama
STUDENTS_FILE = "data/students.json"
PROFILE_PHOTOS_DIR = "data/profile_photos"
CLASS_PHOTOS_DIR = "data/class_photos"
os.makedirs(PROFILE_PHOTOS_DIR, exist_ok=True)
os.makedirs(CLASS_PHOTOS_DIR, exist_ok=True)

def get_class_photo_dir(class_name: str) -> str:
    """Sınıf için fotoğraf klasörünü oluşturur ve yolunu döndürür."""
    class_dir = os.path.join(CLASS_PHOTOS_DIR, class_name)
    os.makedirs(class_dir, exist_ok=True)
    return class_dir

def load_students():
    if os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_students(students):
    with open(STUDENTS_FILE, 'w') as f:
        json.dump(students, f)

# API endpoints
@app.post("/api/students")
async def add_student(student_data: str = Form(...), photo: UploadFile = File(...)):
    # JSON string'i parse et
    student = json.loads(student_data)
    
    # Fotoğrafı kaydet
    photo_path = f"data/profile_photos/{student['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    with open(photo_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)
    
    # Öğrenci bilgilerini kaydet
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
    temp_path = None
    result_path = None
    
    try:
        # Sınıf klasörünü oluştur
        class_dir = get_class_photo_dir(class_name)
        
        # Fotoğrafı geçici olarak kaydet
        temp_path = os.path.join(class_dir, f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
        
        # Sınıftaki öğrencileri bul
        students = load_students()
        class_students = {name: data for name, data in students.items() 
                         if data["class_name"] == class_name and data["blur_face"]}
        
        if not class_students:
            raise HTTPException(status_code=400, detail="No students found for this class")
        
        # Her öğrenci için yüz bulanıklaştırma işlemi
        result_path = os.path.join(class_dir, f"{class_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
        current_path = temp_path
        
        for student_name, student_data in class_students.items():
            try:
                find_and_blur_face(
                    current_path,
                    student_data["photo_path"],
                    result_path
                )
                current_path = result_path
            except Exception as e:
                # Eğer yüz bulanıklaştırma işlemi başarısız olursa, tüm işlemi iptal et
                raise HTTPException(status_code=500, detail=f"Error processing face for student {student_name}: {str(e)}")
        
        # URL'yi düzelt
        relative_path = os.path.relpath(result_path, "data")
        
        # Temp resmi sil
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        
        return {"result_path": relative_path}
        
    except Exception as e:
        # Hata durumunda geçici dosyaları temizle
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        if result_path and os.path.exists(result_path):
            os.remove(result_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/classes")
async def get_classes():
    students = load_students()
    return list(set(data["class_name"] for data in students.values())) 