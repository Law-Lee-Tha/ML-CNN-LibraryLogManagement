import cv2
import pymongo
from pymongo import MongoClient
from bson import Binary
import numpy as np

# Connect to MongoDB
client = MongoClient("mongodb+srv://harinadh14:N%40dh2306@atlascluster.9fb52n9.mongodb.net/")
db = client['LALITHA_face_recognition_db']
collection = db['images(FACES)']

# Retrieve images from MongoDB
images = collection.find()
print(images)
for image_data in images:
    img_binary = image_data['data']
    
    # Convert Binary to bytes
    img_bytes = img_binary

    # Convert bytes to numpy array
    nparr = np.frombuffer(img_bytes, np.uint8)

    # Decode numpy array to image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Display the retrieved image
    cv2.imshow("Retrieved Image", img)
    cv2.waitKey(0)

# Close OpenCV windows
cv2.destroyAllWindows()