import tkinter as tk
from tkinter import ttk
import subprocess
import os

class VideoCaptureApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Video Capture App")

        # Parameters
        self.width = tk.StringVar(value="1456")
        self.height = tk.StringVar(value="1088")
        self.denoise = tk.StringVar(value="cdn_off")
        self.shutter = tk.StringVar(value="30")
        self.framerate = tk.StringVar(value="55")
        self.duration_sec = tk.StringVar(value="10")  # Default duration in seconds
        self.filename = tk.StringVar(value="video")
        self.extension = tk.StringVar(value=".mp4")
        self.save_directory = tk.StringVar(value=os.path.expanduser("~/Desktop"))

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Frame for parameter inputs
        parameter_frame = ttk.LabelFrame(self.master, text="Parameters")
        parameter_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        ttk.Label(parameter_frame, text="Width:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(parameter_frame, textvariable=self.width).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(parameter_frame, text="Height:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(parameter_frame, textvariable=self.height).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(parameter_frame, text="Denoise:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(parameter_frame, textvariable=self.denoise).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(parameter_frame, text="Shutter (µs):").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(parameter_frame, textvariable=self.shutter).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(parameter_frame, text="Framerate:").grid(row=4, column=0, padx=5, pady=5)
        ttk.Entry(parameter_frame, textvariable=self.framerate).grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(parameter_frame, text="Duration (sec):").grid(row=5, column=0, padx=5, pady=5)
        ttk.Entry(parameter_frame, textvariable=self.duration_sec).grid(row=5, column=1, padx=5, pady=5)

        # Frame for file saving inputs
        save_frame = ttk.LabelFrame(self.master, text="Save File")
        save_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        ttk.Label(save_frame, text="Filename:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(save_frame, textvariable=self.filename).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(save_frame, text="Extension:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(save_frame, textvariable=self.extension).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(save_frame, text="Save Directory:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(save_frame, textvariable=self.save_directory).grid(row=2, column=1, padx=5, pady=5)

        # Button to start capture
        ttk.Button(self.master, text="Start Capture", command=self.start_capture).grid(row=2, column=0, padx=10, pady=10)

    def start_capture(self):
        # Convert duration from seconds to milliseconds
        duration_ms = int(self.duration_sec.get()) * 1000

        # Construct the command based on user input
        filename = f"{self.filename.get()}{self.extension.get()}"
        save_path = os.path.join(os.path.expanduser(self.save_directory.get()), filename)

        command = [
            "libcamera-vid",
            "--width", self.width.get(),
            "--height", self.height.get(),
            "--denoise", self.denoise.get(),
            "--shutter", self.shutter.get(),
            "--framerate", self.framerate.get(),
            "-t", str(duration_ms),  # Converted duration in milliseconds
            "-o", save_path
        ]

        # Run the command
        subprocess.run(command)


def main():
    root = tk.Tk()
    app = VideoCaptureApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
