import tkinter
import tkinter.filedialog
import PIL.Image
import PIL.ImageTk
import time
import os

import video
import ffmpeg


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
        fileMenu.add_command(label="Export", command=self.export)
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

    def export(self):
        self.markers.sort()

        list_file = open('list.txt', 'w+')

        try:
            source_name = self.source.split('/')[-1]

            for i in range(0, len(self.markers), 2):
                start_time = self.markers[i] * self.video.duration
                end_time = self.markers[i + 1] * self.video.duration

                start_time = time.strftime('%H:%M:%S', time.gmtime(start_time))
                end_time = time.strftime('%H:%M:%S', time.gmtime(end_time))

                output = 'temp-{}-{}'.format(i, source_name)

                ffmpeg.crop(self.source, start_time, end_time, output)
                list_file.write('file \'{}\'\n'.format(output))

            ffmpeg.concat(list_file.name, 'trimmed-{}'.format(source_name))

        except AttributeError:
            list_file.close()
            return

    def editor_setup(self, source):
        self.source = source

        # load the video
        self.video = video.Video(source)

        # destroy the placeholder text since we have the video
        if self.placeholder:
            self.placeholder.destroy()

        # create a canvas to put the loaded video
        self.video_canvas = tkinter.Canvas(
            self.window, width=self.video.width, height=self.video.height)
        self.video_canvas.pack()

        # create a slider to control the preview of the video
        self.scale = tkinter.Scale(
            self.window, from_=0, to=1, resolutio=-1, orient=tkinter.HORIZONTAL, length=self.video.width, sliderlength=10)
        self.scale.pack()

        # create a canvas to show when is marked
        self.marker_canvas_height = 15
        self.marker_canvas = tkinter.Canvas(
            self.window, width=self.video.width, height=self.marker_canvas_height, background='black')
        self.marker_canvas.pack()

        # the actual storage of all markers
        self.markers = []

        # create a button to mark the current time
        self.button = tkinter.Button(
            self.window, text='Mark', command=self.mark)
        self.button.pack()

        self.update(10)

    def update(self, delay):
        retval, frame = self.video.get_frame(self.scale.get())

        if retval:
            self.photo = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(frame))

            self.video_canvas.create_image(
                0, 0, image=self.photo, anchor=tkinter.NW)

        self.window.after(delay, self.update, delay)

    def mark(self):
        width = 5
        mid = self.scale.get() * self.video.width
        x1 = mid - width / 2
        y1 = 0
        x2 = mid + width / 2
        y2 = self.marker_canvas_height

        if x1 < 0:
            x1 = 0
            x2 = width

        if x2 > self.video.width:
            x2 = self.video.width
            x1 = self.video.width - width

        self.marker_canvas.create_rectangle(x1, y1, x2, y2, fill='green')

        self.markers.append(self.scale.get())


if __name__ == '__main__':
    Main('VEdit', '1600x900')
