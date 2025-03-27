from pydantic import BaseModel

class Student(BaseModel):
    name: str
    class_name: str
    photo_path: str | None = None
    blur_face: bool = True 