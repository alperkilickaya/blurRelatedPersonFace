import cv2
import face_recognition
import numpy as np
import argparse

def blur_face(image, face_location, blur_factor=75):
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
    
    print(f"Found {len(face_locations)} faces in group image")
    print(f"Target face encoding shape: {target_face_encoding[0].shape}")
    
    # Compare faces and blur matching ones with strict tolerance
    target_encoding = target_face_encoding[0]  # Use the first face found in target image
    matches = []
    
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Calculate face distance (lower is better)
        face_distance = face_recognition.face_distance([target_encoding], face_encoding)[0]
        print(f"Face distance: {face_distance:.3f}")
        
        # Store all potential matches
        if face_distance < 0.7:  # Initial threshold for potential matches
            matches.append((face_distance, (top, right, bottom, left)))
    
    if matches:
        # Sort matches by distance
        matches.sort(key=lambda x: x[0])
        
        # Get the best match
        best_distance, best_match = matches[0]
        print(f"Best match distance: {best_distance:.3f}")
        
        # Check if this is a clear best match
        if len(matches) > 1:
            second_best_distance = matches[1][0]
            print(f"Second best match distance: {second_best_distance:.3f}")
            
            # Only blur if:
            # 1. Best match is below threshold
            # 2. There's a clear difference between best and second best match
            if best_distance < 0.55 and (second_best_distance - best_distance) > 0.1:
                group_image_cv = blur_face(group_image_cv, best_match)
                print(f"Face blurred successfully. Match distance: {best_distance:.3f}")
                # Save the result
                cv2.imwrite(output_path, group_image_cv)
                print(f"Processed image saved to {output_path}")
                return
            else:
                print(f"No clear best match found. Best: {best_distance:.3f}, Second: {second_best_distance:.3f}")
        else:
            # If only one match, use stricter threshold
            if best_distance < 0.5:
                group_image_cv = blur_face(group_image_cv, best_match)
                print(f"Face blurred successfully. Single match distance: {best_distance:.3f}")
                # Save the result
                cv2.imwrite(output_path, group_image_cv)
                print(f"Processed image saved to {output_path}")
                return
            else:
                print(f"No good enough match found. Distance: {best_distance:.3f}")
    else:
        print("No matches found below threshold")
    
    # If we get here, no face was blurred, so just save the original image
    cv2.imwrite(output_path, group_image_cv)
    print(f"Original image saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Blur a specific face in a group photo')
    parser.add_argument('group_image', help='Path to the group photo')
    parser.add_argument('target_image', help='Path to the target face photo')
    parser.add_argument('output_image', help='Path to save the output image')
    
    args = parser.parse_args()
    
    find_and_blur_face(args.group_image, args.target_image, args.output_image)

if __name__ == "__main__":
    main() 