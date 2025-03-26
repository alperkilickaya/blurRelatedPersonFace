import cv2
import face_recognition
import numpy as np
import argparse

def blur_face(image, face_location, blur_factor=55):
    """
    Blur the face in the given image at the specified location
    """
    top, right, bottom, left = face_location
    face_image = image[top:bottom, left:right]
    
    # Apply Gaussian blur
    face_image = cv2.GaussianBlur(face_image, (blur_factor, blur_factor), 0)
    
    # Put the blurred face back into the original image
    image[top:bottom, left:right] = face_image
    return image

def find_and_blur_face(group_image_path, target_image_path, output_path):
    """
    Find and blur the face from target_image in group_image
    """
    # Load images
    group_image = face_recognition.load_image_file(group_image_path)
    target_image = face_recognition.load_image_file(target_image_path)
    
    # Find face encodings
    target_face_encoding = face_recognition.face_encodings(target_image)
    
    if not target_face_encoding:
        print("No face found in target image!")
        return
    
    # Find all faces in the group image
    face_locations = face_recognition.face_locations(group_image)
    face_encodings = face_recognition.face_encodings(group_image, face_locations)
    
    # Convert to OpenCV format for blurring
    group_image_cv = cv2.cvtColor(group_image, cv2.COLOR_RGB2BGR)
    
    # Compare faces and blur matching ones with strict tolerance
    target_encoding = target_face_encoding[0]  # Use the first face found in target image
    best_match = None
    best_match_distance = float('inf')
    
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Calculate face distance (lower is better)
        face_distance = face_recognition.face_distance([target_encoding], face_encoding)[0]
        
        # Update best match if this face is closer to target
        if face_distance < best_match_distance:
            best_match_distance = face_distance
            best_match = (top, right, bottom, left)
    
    # Only blur if we found a good match (distance threshold)
    if best_match and best_match_distance < 0.5:  # Adjust this threshold as needed
        group_image_cv = blur_face(group_image_cv, best_match)
        print(f"Face blurred successfully. Match distance: {best_match_distance:.3f}")
    else:
        print(f"No good match found. Best match distance: {best_match_distance:.3f}")
    
    # Save the result
    cv2.imwrite(output_path, group_image_cv)
    print(f"Processed image saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Blur a specific face in a group photo')
    parser.add_argument('group_image', help='Path to the group photo')
    parser.add_argument('target_image', help='Path to the target face photo')
    parser.add_argument('output_image', help='Path to save the output image')
    
    args = parser.parse_args()
    
    find_and_blur_face(args.group_image, args.target_image, args.output_image)

if __name__ == "__main__":
    main() 