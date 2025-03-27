import cv2
import face_recognition
import numpy as np

class FaceService:
    @staticmethod
    def blur_face(image, face_location, blur_factor=55):
        """Blur the face in the given image at the specified location"""
        top, right, bottom, left = face_location
        face_image = image[top:bottom, left:right]
        face_image = cv2.GaussianBlur(face_image, (blur_factor, blur_factor), 0)
        image[top:bottom, left:right] = face_image
        return image

    @staticmethod
    def find_and_blur_face(group_image_path: str, target_image_path: str, output_path: str) -> bool:
        """Find and blur the face from target_image in group_image"""
        # Load images
        group_image = face_recognition.load_image_file(group_image_path)
        target_image = face_recognition.load_image_file(target_image_path)
        
        # Find face encodings
        target_face_encoding = face_recognition.face_encodings(target_image)
        
        if not target_face_encoding:
            print("No face found in target image!")
            return False
        
        # Find all faces in the group image
        face_locations = face_recognition.face_locations(group_image)
        face_encodings = face_recognition.face_encodings(group_image, face_locations)
        
        # Convert to OpenCV format for blurring
        group_image_cv = cv2.cvtColor(group_image, cv2.COLOR_RGB2BGR)
        
        print(f"Found {len(face_locations)} faces in group image")
        print(f"Target face encoding shape: {target_face_encoding[0].shape}")
        
        # Compare faces and blur matching ones
        target_encoding = target_face_encoding[0]
        matches = []
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            face_distance = face_recognition.face_distance([target_encoding], face_encoding)[0]
            print(f"Face distance: {face_distance:.3f}")
            
            if face_distance < 0.7:
                matches.append((face_distance, (top, right, bottom, left)))
        
        if matches:
            matches.sort(key=lambda x: x[0])
            best_distance, best_match = matches[0]
            
            if len(matches) > 1:
                second_best_distance = matches[1][0]
                if best_distance < 0.55 and (second_best_distance - best_distance) > 0.1:
                    group_image_cv = FaceService.blur_face(group_image_cv, best_match)
                    cv2.imwrite(output_path, group_image_cv)
                    return True
            else:
                if best_distance < 0.5:
                    group_image_cv = FaceService.blur_face(group_image_cv, best_match)
                    cv2.imwrite(output_path, group_image_cv)
                    return True
        
        cv2.imwrite(output_path, group_image_cv)
        return False 