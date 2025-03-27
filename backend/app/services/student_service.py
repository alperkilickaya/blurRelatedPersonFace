import os
import json
from typing import Dict, List
from ..models.student import Student

class StudentService:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.students_file = os.path.join(data_dir, "students.json")
        self.profile_photos_dir = os.path.join(data_dir, "profile_photos")
        self.class_photos_dir = os.path.join(data_dir, "class_photos")
        
        # Create necessary directories
        os.makedirs(self.profile_photos_dir, exist_ok=True)
        os.makedirs(self.class_photos_dir, exist_ok=True)
    
    def load_students(self) -> Dict:
        """Load student data from JSON file."""
        if os.path.exists(self.students_file):
            with open(self.students_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_students(self, students: Dict) -> None:
        """Save student data to JSON file."""
        with open(self.students_file, 'w') as f:
            json.dump(students, f)
    
    def get_class_photo_dir(self, class_name: str) -> str:
        """Creates and returns the photo directory for a class."""
        class_dir = os.path.join(self.class_photos_dir, class_name)
        os.makedirs(class_dir, exist_ok=True)
        return class_dir
    
    def get_classes(self) -> List[str]:
        """Get list of all classes."""
        students = self.load_students()
        return list(set(data["class_name"] for data in students.values()))
    
    def reset_data(self) -> None:
        """Reset all data by deleting photos and students.json"""
        # Delete profile photos
        for file in os.listdir(self.profile_photos_dir):
            file_path = os.path.join(self.profile_photos_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        # Delete class photos
        for class_dir in os.listdir(self.class_photos_dir):
            class_path = os.path.join(self.class_photos_dir, class_dir)
            if os.path.isdir(class_path):
                for file in os.listdir(class_path):
                    file_path = os.path.join(class_path, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                os.rmdir(class_path)
        
        # Delete students.json
        if os.path.exists(self.students_file):
            os.remove(self.students_file) 