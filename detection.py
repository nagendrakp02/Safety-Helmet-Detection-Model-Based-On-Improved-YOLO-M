import cv2
import torch
import numpy as np
import tkinter as tk
from tkinter import filedialog

path = 'C:/Users/nagen/Desktop/Final_Project/yolov5safetyhelmet-main/Last.pt'

try:
    model = torch.hub.load('ultralytics/yolov5', 'custom', path, force_reload=True)
except Exception as e:
    print("Error loading the model:", e)
    exit(1)


def select_video_file():
    root = tk.Tk()
    root.withdraw()  
    file_path = filedialog.askopenfilename(title="Select a video file", filetypes=[("Video files", "*.mp4")])
    return file_path


def detect_objects_from_file(video_file):
    if not video_file:
        print("No file selected. Exiting...")
        return

    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return

    cv2.namedWindow("Detected Objects", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Detected Objects", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        count += 1
        if count % 3 != 0:
            continue
        frame = cv2.resize(frame, (1020, 600))
        results = model(frame)
        frame = np.squeeze(results.render())
        cv2.imshow("Detected Objects", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def access_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    cv2.namedWindow("Safety Helmet Detection", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Safety Helmet Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        if results.pred:
            safety_helmets = [pred for pred in results.pred[0] if pred[5] == 0]

            if safety_helmets:
                for helmet in safety_helmets:
                    box = helmet[:4].int().tolist()  
                    cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
                alert_message = ""
            else:
                alert_message = "Alert: Safety helmets not detected!"
        else:
            alert_message = "Alert: No predictions available!"

        cv2.putText(frame, alert_message, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Safety Helmet Detection", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_file = select_video_file()
    detect_objects_from_file(video_file)
