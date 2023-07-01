import cv2
import os

# Define the path to the directory containing the downloaded images
dataset_dir = 'facedataset'

# Create a directory to save the preprocessed images
preprocessed_dir = 'preprocessed_dataset'
if not os.path.exists(preprocessed_dir):
    os.makedirs(preprocessed_dir)

# Initialize the face detection model (e.g., Haar Cascade or deep learning-based face detector)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Preprocess each image in the dataset directory
for filename in os.listdir(dataset_dir):
    if filename.endswith('.jpg'):
        image_path = os.path.join(dataset_dir, filename)

        # Load the image
        image = cv2.imread(image_path)

        # Convert the image to grayscale for face detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Perform face detection
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Process each detected face
        for (x, y, w, h) in faces:
            # Extract the face region
            face = image[y:y+h, x:x+w]

            # Resize the face to a desired size (e.g., 256x256)
            resized_face = cv2.resize(face, (256, 256))

            # Save the preprocessed face in the preprocessed directory
            save_path = os.path.join(preprocessed_dir, f"{filename}_{x}_{y}.jpg")
            cv2.imwrite(save_path, resized_face)

print("Image preprocessing complete!")
