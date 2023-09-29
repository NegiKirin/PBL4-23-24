import face_recognition
import os
import sys
import cv2
import numpy as np
import time
class face_detector:
    
    def __init__(self):
        self.data_root = '../database'
        self.known_encodings = []
        self.known_names = []
        self.width = 1280
        self.height = 720
        self.cap = None
        self.camera = 0
        self.save_path_folder = None
        
    def load_data(self):
        # Change direct path: './database'
        os.chdir(self.data_root)
        # Find all folder in database
        for folder in os.listdir():
            #Find all file in folder
            for file in os.listdir(folder):
                # Image_path: './database/folder/image'
                image_path = os.path.join(folder, file)
                # Load image
                known_image = face_recognition.load_image_file(image_path)
                # Encoding image
                know_encoding = face_recognition.face_encodings(known_image)[0]
                # Add to known_encodings
                self.known_encodings.append(know_encoding)
                # Add to known_names
                self.known_names.append(folder)
    
    def face_detection(self):
        self.cap = cv2.VideoCapture(self.camera)
        while True:
            ret, frame = self.cap.read()
            if ret == True:
                #Flip frame
                frame = cv2.flip(frame, 1)
                
                # List to saving current name
                face_names = []
                name = "Unknown"
                
                # List to saving face location
                face_locations = []
                
                # List to saving face_encodings
                face_encodings = []
                
                # Resize frame to easy processing
                small_frame = cv2.resize(frame, (0, 0), fx = 0.5, fy = 0.5).astype(np.uint8)
                
                # Convert BGR_frame to RGB_frame
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                # Define location of a face in camera => return list of tuple(top, right, bottom, left)
                face_locations = face_recognition.face_locations(small_frame)
                
                # Encoding current face frame in camera
                face_encodings = face_recognition.face_encodings(small_frame, face_locations)
                
                for face_encoding in face_encodings:
                    # Checking face => return a list of True, False
                    matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
                    
                    # Caculate distance of current_face and known_face => return a list of distance
                    face_distances = face_recognition.face_distance(self.known_encodings, face_encoding)
                    
                    # Take a index of minimum value in list_of_distance
                    best_match_index = np.argmin(face_distances)
                    
                    if matches[best_match_index] == True and face_distances[best_match_index] <= 0.5:
                        name = self.known_names[best_match_index]

                    face_names.append(name)
                    for (top, right, bottom, left), name in zip(face_locations, face_names):
                        # Draw a box around the face and label it
                        cv2.rectangle(frame, (left * 2, top * 2), (right * 2, bottom * 2), (0, 255, 0), 2)
                        
                        # Write name of faces
                        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        
                # Show fps in screen
                fps = self.cap.get(cv2.CAP_PROP_FPS)
                cv2.putText(frame, f"FPS: {str(fps)}", (50, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

                # Show frame on screen
                cv2.imshow("Face Recognition", frame)
                
                if cv2.waitKey(2) == ord('q'):
                    break
        self.cap.release()
        cv2.destroyAllWindows()
                
    # Method set up new folder
    def setup_folder(self, name_folder):
        # Initial path new folder to set up
        folder_path = os.path.join(self.data_root, name_folder)
        print("Set up new folder: {}".format(folder_path))
        # Check a new folder is exist
        if not os.path.exists(folder_path):
            # Create a new folder
            os.makedirs(folder_path)
            # Saving new folder
            self.save_path_folder = folder_path
            print('Create new folder: {}'.format(folder_path))
    
    
    #Method capture a picture
    def capture_image(self, name_folder):
        self.cap = cv2.VideoCapture(self.camera)
        print('Press y to capture a picture: ' )
        while True:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                cv2.imshow('take a picture', frame)
                if cv2.waitKey(2) == ord('y'):
                    cv2.imwrite(os.path.join(self.save_path_folder, f'{name_folder}.jpg'), frame)
                    print(f'Image captured and save as {self.save_path_folder}/{name_folder}.jpg')
                    break
        self.cap.release()
        cv2.destroyAllWindows()
                

def main():
    obj = face_detector()
    obj.load_data()
    obj.face_detection()

main()          
            
            
            

