import face_recognition
import cv2
import numpy as np
import os
import pandas as pd
from datetime import datetime
from pymongo import MongoClient
from pyzbar.pyzbar import decode
import ctypes
import subprocess 
#from barcode2 import scanner


known_face_encodings = []
known_face_names = []

# Define a function to load a single image, extract the face encoding, and add it to the lists
def add_known_face(image_path, name):
    image = face_recognition.load_image_file(image_path)
    face_encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(face_encoding)
    known_face_names.append(name)

# Replace "known_images_folder" with the folder path where your known images are stored.
known_images_folder = "./images/"

# Loop through all files in the known_images_folder
for file_name in os.listdir(known_images_folder):
    if file_name.endswith(".jpg") or file_name.endswith(".png"):
        image_path = os.path.join(known_images_folder, file_name)
        name = os.path.splitext(file_name)[0]  # Use the file name (without extension) as the name
        add_known_face(image_path, name)

# Create an empty DataFrame to store the face detection data
face_data = pd.DataFrame(columns=["Name", "Timestamp"])

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Initialize MongoDB client and database
#client = MongoClient('mongodb://localhost:27017/')
#server_connection_string = mongodb+srv://harinadh14:N%40dh2306@atlascluster.9fb52n9.mongodb.net/
client = MongoClient("mongodb+srv://harinadh14:N%40dh2306@atlascluster.9fb52n9.mongodb.net/")
db = client['LALITHA_face_recognition_db']
collection = db['face_data']

face_data_list =[]



# capture webcam 
#cap = cv2.VideoCapture(0)

def scanner():
    while video_capture.isOpened():
        success,frame = video_capture.read()
        # flip the image like mirror image 
        frame  = cv2.flip(frame,1)
        # detect the barcode 
        detectedBarcode = decode(frame)
        # if no any barcode detected 
        if not detectedBarcode:
            print("No any Barcode Detected")
        
        # if barcode detected 
        else:
            # codes in barcode 
            for barcode in detectedBarcode:
                # if barcode is not blank 
                if barcode.data != "":
                    cv2.putText(frame,str(barcode.data),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,255),2)
                    x= cv2.putText(frame,str(barcode.data),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,255),2)
                    print(barcode.data)
                    cv2.imwrite("code.png",frame)


        cv2.imshow('scanner' , frame)
        if cv2.waitKey(1) == ord('q'):
            break




while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    
    # Only process every other frame of video to save time
    if process_this_frame:


       # scanner()

        
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]


        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Save the face data to the MongoDB collection
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if name != "Unknown":
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = {"Name": name, "Timestamp": timestamp}
            face_data_list.append(data)
           # subprocess.run("C:\\Users\\Public\\lalitha2\\barcodeRunner.bat" ,  shell=True )
            scanner()
            collection.insert_one(data)
        elif name == "Unknown":
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = {"Name": name, "Timestamp": timestamp}
            collection.insert_one(data)



    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Convert the face data list to a DataFrame
face_data_df = pd.DataFrame(face_data_list)

# Save the face data to an Excel file
excel_filename = "face_detection_data.xlsx"
face_data_df.to_excel(excel_filename, index=False)
print(f"Face detection data exported to {excel_filename}")


# Release the MongoDB client connection
client.close()

# Save the face data to an Excel file
#face_data.to_excel("face_detection_data.xlsx", index=False)

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
 