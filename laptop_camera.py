import cv2

# Initialize the camera (0 is typically the default camera)
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Could not open the camera.")
    exit()

print("Press 'c' to capture the image and 'q' to quit.")

while True:
    # Capture the video frame by frame
    ret, frame = camera.read()
    
    if not ret:
        print("Failed to grab frame.")
        break

    # Display the current frame
    cv2.imshow("Camera Feed", frame)

    # Wait for a key press
    key = cv2.waitKey(1)

    # If 'c' is pressed, capture the image
    if key == ord('c'):
        captured_image = frame.copy()
        cv2.imshow("Captured Image", captured_image)
        cv2.imwrite("captured_image.jpg", captured_image)  # Save the image
        print("Image captured and saved as 'captured_image.jpg'.")

    # If 'q' is pressed, quit the program
    if key == ord('q'):
        print("Exiting...")
        break

# Release the camera and close OpenCV windows
camera.release()
cv2.destroyAllWindows()
