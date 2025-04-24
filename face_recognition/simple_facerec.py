import cv2
import face_recognition
import numpy as np
import os

class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.frame_resizing = 0.25  # Resize factor for faster processing

    def load_encoding_images(self, images_path):
        """
        Load face encodings from images in a given directory.
        """
        images_list = os.listdir(images_path)
        for image_name in images_list:
            image_path = os.path.join(images_path, image_name)
            img = cv2.imread(image_path)
            if img is None:
                print(f"Warning: Could not read image {image_path}")
                continue
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_img)
            if encodings:
                self.known_face_encodings.append(encodings[0])
                self.known_face_names.append(os.path.splitext(image_name)[0])

    def detect_known_faces(self, frame):
        """
        Detect faces in the frame and match them with known faces.
        """
        if frame is None:
            print("Error: Received an empty frame!")
            return [], []

        # Check if frame is empty before resizing
        if frame.shape[0] == 0 or frame.shape[1] == 0:
            print("Error: Empty frame received!")
            return [], []

        # Resize the frame for faster face recognition
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)

        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances) if len(face_distances) > 0 else None
            if best_match_index is not None and matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        # Scale face locations back to original frame size
        face_locations = [(int(top / self.frame_resizing), int(right / self.frame_resizing),
                           int(bottom / self.frame_resizing), int(left / self.frame_resizing))
                          for (top, right, bottom, left) in face_locations]

        return face_locations, face_names
