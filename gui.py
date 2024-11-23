import tkinter as tk
from tkinter import filedialog
import detection
import winsound  

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.background_image = tk.PhotoImage(file="background_image.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)
        
        self.header_label = tk.Label(self, text="Safety Helmet Detection Using YOLOv5", font=("Helvetica", 16))
        self.header_label.pack(pady=10)
        
        self.select_file_button = tk.Button(self, text="Select Video File", command=self.select_video_file, font=("Helvetica", 14))
        self.select_file_button.pack(pady=10)
        
        self.camera_button = tk.Button(self, text="Access Camera", command=self.access_camera, font=("Helvetica", 14))
        self.camera_button.pack(pady=10)
        
        self.footer_label = tk.Label(self, text="Powered by YOLO", font=("Helvetica", 10))
        self.footer_label.pack(pady=10)

    def select_video_file(self):
        file_path = filedialog.askopenfilename(title="Select a video file", filetypes=[("Video files", "*.mp4")])
        if file_path:
            detection.detect_objects_from_file(file_path)

    def access_camera(self):
        detection.access_camera()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")

    app.mainloop()
