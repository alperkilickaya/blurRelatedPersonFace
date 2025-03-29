import os
from typing import Dict, List
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class StudentService:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.profile_photos_dir = os.path.join(data_dir, "profile_photos")
        self.class_photos_dir = os.path.join(data_dir, "class_photos")
        
        # Create necessary directories
        os.makedirs(self.profile_photos_dir, exist_ok=True)
        os.makedirs(self.class_photos_dir, exist_ok=True)
        
        # Initialize Supabase client
        self.supabase: Client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_ANON_KEY")
        )
    
    def load_students(self) -> Dict:
        """Load student data from Supabase."""
        try:
            response = self.supabase.table("students").select("*").execute()
            print("response", response)
            students = {}
            for student in response.data:
                students[student["name"]] = {
                    "class_name": student["class_name"],
                    "photo_path": student["photo_path"],
                    "blur_face": student["blur_face"]
                }
            return students
        except Exception as e:
            print(f"Error loading students from Supabase: {str(e)}")
            return {}
    
    def save_students(self, students: Dict) -> None:
        """Save student data to Supabase."""
        try:
            # Insert the new student directly
            for name, data in students.items():
                self.supabase.table("students").insert({
                    "name": name,
                    "class_name": data["class_name"],
                    "photo_path": data["photo_path"],
                    "blur_face": data["blur_face"]
                }).execute()
        except Exception as e:
            print(f"Error saving students to Supabase: {str(e)}")
    
    def get_class_photo_dir(self, class_name: str) -> str:
        """Creates and returns the photo directory for a class."""
        class_dir = os.path.join(self.class_photos_dir, class_name)
        os.makedirs(class_dir, exist_ok=True)
        return class_dir
    
    def get_classes(self) -> List[str]:
        """Get list of all classes from Supabase."""
        try:
            response = self.supabase.table("students").select("class_name").execute()
            return list(set(student["class_name"] for student in response.data))
        except Exception as e:
            print(f"Error getting classes from Supabase: {str(e)}")
            return []
    
    def reset_data(self) -> None:
        """Reset all data by deleting photos and students from Supabase."""
        try:
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
            
            # Delete all students from Supabase with a WHERE clause
            self.supabase.table("students").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        except Exception as e:
            print(f"Error resetting data: {str(e)}")
    
    def test_connection(self) -> bool:
        """Test Supabase connection."""
        try:
            # Try to insert a test record
            self.supabase.table("students").insert({
                "name": "test_connection",
                "class_name": "test",
                "photo_path": "test.jpg",
                "blur_face": True
            }).execute()
            
            # If successful, delete the test record
            self.supabase.table("students").delete().eq("name", "test_connection").execute()
            
            print("Successfully connected to Supabase!")
            return True
        except Exception as e:
            print(f"Failed to connect to Supabase: {str(e)}")
            return False 