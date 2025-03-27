import os
import shutil
from datetime import datetime
from fastapi import HTTPException, UploadFile
from ..services.student_service import StudentService
from ..services.face_service import FaceService
from ..models.student import Student

class StudentController:
    def __init__(self):
        self.student_service = StudentService()
        self.face_service = FaceService()
    
    async def add_student(self, student: Student, photo: UploadFile) -> dict:
        """Add a new student with profile photo"""
        try:
            # Save photo
            photo_path = os.path.join(
                "data/profile_photos",
                f"{student.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            )
            with open(photo_path, "wb") as buffer:
                shutil.copyfileobj(photo.file, buffer)
            
            # Save student information
            students = self.student_service.load_students()
            students[student.name] = {
                "class_name": student.class_name,
                "photo_path": photo_path,
                "blur_face": student.blur_face
            }
            self.student_service.save_students(students)
            
            return {"message": "Student added successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def process_class_photo(self, photo: UploadFile, class_name: str) -> dict:
        """Process class photo and blur faces"""
        result_path = None
        
        try:
            # Create class directory
            class_dir = self.student_service.get_class_photo_dir(class_name)
            
            # Load students for this class
            students = self.student_service.load_students()
            class_students = {
                name: data for name, data in students.items() 
                if data["class_name"] == class_name
            }
            
            print(f"Processing photo for class: {class_name}")
            print(f"Found {len(class_students)} students in class")
            
            # Process photo for each student
            any_face_blurred = False
            
            # Save the original photo first
            result_path = os.path.join(
                class_dir,
                f"{class_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            )
            with open(result_path, "wb") as buffer:
                shutil.copyfileobj(photo.file, buffer)
            
            for student_name, student_data in class_students.items():
                if student_data["blur_face"]:
                    print(f"Processing blur for student: {student_name}")
                    print(f"Student photo path: {student_data['photo_path']}")
                    try:
                        if self.face_service.find_and_blur_face(
                            result_path,
                            student_data["photo_path"],
                            result_path
                        ):
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
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_classes(self) -> list:
        """Get list of all classes"""
        return self.student_service.get_classes()
    
    def reset_data(self) -> dict:
        """Reset all data"""
        try:
            self.student_service.reset_data()
            return {"message": "All data reset successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) 