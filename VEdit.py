import tkinter
import tkinter.filedialog
import PIL.Image
import PIL.ImageTk

from Video import Video


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
            self.editor_setup(source)
        else:
            self.placeholder = tkinter.Label(
                self.window, text='Load a video to start.')
            self.placeholder.pack()

        self.window.mainloop()

    def load(self):
        self.editor_setup(tkinter.filedialog.askopenfilename())

    def editor_setup(self, source):
        # load the video
        self.video = Video(source)

        # destroy the placeholder text since we have the video
        if self.placeholder:
            self.placeholder.destroy()

        # size and create a canvas to put the loaded video
        self.canvas = tkinter.Canvas(
            self.window, width=self.video.width, height=self.video.height)
        self.canvas.pack()

        self.scale = tkinter.Scale(
            self.window, from_=0, to=1, resolutio=-1, orient=tkinter.HORIZONTAL, length=self.video.width)
        self.scale.pack()

        self.update(10)

    def update(self, delay):
        retval, frame = self.video.get_frame(self.scale.get())

        if retval:
            self.photo = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(frame))

            self.canvas.create_image(
                0, 0, image=self.photo, anchor=tkinter.NW)

        self.window.after(delay, self.update, delay)


if __name__ == "__main__":
    Main('VEdit', '1600x900')
