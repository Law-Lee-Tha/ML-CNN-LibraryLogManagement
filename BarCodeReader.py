import cv2
from pyzbar.pyzbar import decode

# Function to process barcodes in an image
def process_barcodes(image):
    barcodes = decode(image)
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        print(f"Barcode Type: {barcode_type}, Barcode Data: {barcode_data}")

# Read an image and process barcodes
image_path = 'C:\\Users\\Public\\lalitha2\\barcode-2.jpg'  # Replace with the path to your image
image = cv2.imread(image_path)
process_barcodes(image)

# Read from a video feed and process barcodes
video_capture = cv2.VideoCapture(0)  # Use 0 for default webcam
while True:
    ret, frame = video_capture.read()
    process_barcodes(frame)
    
    cv2.imshow('Barcode Scanner', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
