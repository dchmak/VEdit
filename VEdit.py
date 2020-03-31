import tkinter
import tkinter.filedialog
import cv2
import PIL.Image
import PIL.ImageTk

RESOLUTION = '1600x900'


class Main:
    def __init__(self, title, resolution, source=None):
        # create the window
        self.window = tkinter.Tk()
        self.window.title(title)
        self.window.geometry(resolution)

        # create a menu bar
        menubar = tkinter.Menu(self.window)
        self.window.config(menu=menubar)

        # create and add the File cascade to the menu bar
        fileMenu = tkinter.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Load", command=self.load)
        menubar.add_cascade(label="File", menu=fileMenu)

        if source:
            self.display_video(source)
        else:
            self.placeholder = tkinter.Label(
                self.window, text='Load a video to start.')
            self.placeholder.pack()

        self.window.mainloop()

    def load(self):
        self.display_video(tkinter.filedialog.askopenfilename())

    def display_video(self, source):
        # load the video
        self.video = Video(source)

        # destroy the placeholder text since we have the video
        if self.placeholder:
            self.placeholder.destroy()

        # size and create a canvas to put the loaded video
        self.canvas = tkinter.Canvas(
            self.window, width=self.video.width, height=self.video.height)
        self.canvas.pack()

        self.update(10)

    def update(self, delay):
        retval, frame = self.video.get_frame()

        if retval:
            self.photo = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(frame))

            self.canvas.create_image(
                0, 0, image=self.photo, anchor=tkinter.NW)

        self.window.after(delay, self.update, delay)


class Video:
    def __init__(self, source):
        # open the video source
        self.video = cv2.VideoCapture(source)
        if not self.video.isOpened():
            raise ValueError("Unable to open video source", source)

        # get video source width and height
        self.width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        if self.video.isOpened():
            self.video.release()

    def get_frame(self):
        if self.video.isOpened():
            ret, frame = self.video.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        return (ret, None)


if __name__ == "__main__":
    Main('VEdit', RESOLUTION)
