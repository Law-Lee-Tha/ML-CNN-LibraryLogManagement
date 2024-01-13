import cv2
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
from pymongo import MongoClient
from bson import Binary


client = MongoClient("mongodb+srv://harinadh14:N%40dh2306@atlascluster.9fb52n9.mongodb.net/")
db = client['LALITHA_face_recognition_db']
collection = db['images(FACES)']


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Check if the video capture is open
if not video_capture.isOpened():
    messagebox.showerror("Error", "Webcam not found or could not be opened.")
    exit()

# Create a directory to save captured images (if it doesn't exist)
#save_dir = "./images/"
#C:\Users\Public\lalitha2\images
save_dir = "C:/Users/Public/lalitha2/images"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

def capture_image():
    global video_capture
    
    # Capture a single frame from the video
    ret, frame = video_capture.read()
    
    if ret:
        # Save the image to the specified directory with a unique name
        image_name = simpledialog.askstring("Image Name", "Enter the image name (without extension):")
        if image_name:
            image_path = os.path.join(save_dir, f"{image_name}.jpg")
            cv2.imwrite(image_path, frame)
            messagebox.showinfo("Image Saved", f"Image saved as: {image_path}")
            
            # Convert the image to binary
            with open(image_path, "rb") as image_file:
                image_binary = image_file.read()
            
            # Insert the image into MongoDB
            image_data = {'name': image_name, 'data': Binary(image_binary)}
            collection.insert_one(image_data)
            messagebox.showinfo("Image Uploaded", f"Image uploaded to MongoDB with name: {image_name}")


def quit_program():
    global video_capture, client
    
    # Release the video capture and close all windows
    video_capture.release()
    client.close()
    root.destroy()

root = tk.Tk()
root.title("Face Recognition App")

canvas = tk.Canvas(root, width=640, height=480)
canvas.pack()

def show_frame():
    global video_capture
    ret, frame = video_capture.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        canvas.photo = photo
        root.after(10, show_frame)

btn_capture = tk.Button(root, text="Capture Image", command=capture_image)
btn_capture.pack(side=tk.LEFT, padx=10, pady=10)

btn_quit = tk.Button(root, text="Quit", command=quit_program)
btn_quit.pack(side=tk.RIGHT, padx=10, pady=10)

show_frame()
root.mainloop()