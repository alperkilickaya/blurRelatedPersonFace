from fastapi import APIRouter, File, Form, UploadFile
import json
from ..controllers.student_controller import StudentController
from ..models.student import Student

router = APIRouter()
controller = StudentController()

@router.post("/add-student")
async def add_student(student_data: str = Form(...), photo: UploadFile = File(...)):
    student_dict = json.loads(student_data)
    # photo_path will be set by the controller
    student_dict["photo_path"] = ""
    student = Student(**student_dict)
    return await controller.add_student(student, photo)

@router.get("/get-students")
async def get_students():
    return controller.student_service.load_students()

@router.get("/get-classes")
async def get_classes():
    return controller.get_classes()

@router.post("/process-photo")
async def process_photo(photo: UploadFile = File(...), class_name: str = Form(...)):
    return await controller.process_class_photo(photo, class_name)

@router.post("/reset-data")
async def reset_data():
    return controller.reset_data() 