import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
from ex2_copy import *
from subprocess import Popen

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT) + 150

        self.canvas = tk.Canvas(window, width=self.width, height=self.height)
        self.canvas.pack()

        self.btn_start_camera = tk.Button(window, text="Start Camera", width=20, command=self.start_camera, bg='red', fg='white', borderwidth=1, relief='ridge')
        self.btn_start_camera.place(relx=0.1, rely=0.8,anchor=tk.CENTER)

        self.btn_stop_camera = tk.Button(window, text="Stop Camera", width=20, command=self.stop_camera, bg='green', fg='white', borderwidth=1, relief='ridge')
        self.btn_stop_camera.place(relx=0.1, rely=0.84,anchor=tk.CENTER)

        self.btn_upload_video = tk.Button(window, text="Upload Video", width=20, command=self.upload_video, bg='pink', fg='white', borderwidth=1, relief='ridge')
        self.btn_upload_video.place(relx=0.1, rely=0.89,anchor=tk.CENTER)

        self.btn_start_game = tk.Button(window, text="open game", width=20, command=self.start_game, bg='blue', fg='white', borderwidth=1, relief='ridge')
        self.btn_start_game.place(relx=0.1, rely=0.93,anchor=tk.CENTER)

        self.btn_exit = tk.Button(window, text="Exit", width=20, command=self.exit, borderwidth=1, relief='ridge')
        self.btn_exit.place(relx=0.1, rely=0.98,anchor=tk.CENTER)

        self.delay = 10
        self.update()
        self.window.mainloop()
    def draw_inference(self, text, font_size, text_color):
        self.canvas.delete('all')
        x1 = self.width - 480
        y1 = self.height - 130
        x2  = self.width - 5
        y2 = self.height - 5
        font = ("Arial", font_size)
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
        x_center = (x1 + x2) / 2
        y_center = (y1 + y2) / 2
        self.canvas.create_text(x_center, y_center, text=text, font=font, fill=text_color)

    def start_game(self):
        path_game = "D:\proffile\steamapps\common\Asphalt 9 Legends\\Asphalt9_Steam_x64_rtl.exe"

        Popen([path_game])

    def start_camera(self):
        self.vid = cv2.VideoCapture(self.video_source)

    def stop_camera(self):
        if self.vid.isOpened():
            self.vid.release()

    def upload_video(self):
        self.stop_camera()
        file_path = filedialog.askopenfilename()
        if file_path:
            self.vid = cv2.VideoCapture(file_path)

    def exit(self):
        self.stop_camera()
        self.window.quit()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = HandGestureController(ret, frame, self.vid)
            frame, text = frame.process_video()
            self.draw_inference(text, 40, "red")
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(self.delay, self.update)

# Tạo một cửa sổ
App(tk.Tk(), "Tkinter OpenCV GUI")