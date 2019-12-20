from tkinter import *
from tkinter import colorchooser, filedialog
import PIL
from PIL import ImageGrab


class main:
    def __init__(self, master):
        self.master = master
        self.x=0
        self.y=0
        self.color_fg = 'black'
        self.color_bg = 'white'
        self.rect=None
        self.old_x = None
        self.old_y = None
        self.drawchange=0
        self.drawWidgets()
        self.canvas = Canvas(self.master, width=800, height=600, bg=self.color_bg)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B3-Motion>", self.on_move_press)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def paint(self, event):
        if self.drawchange==0:
            if self.old_x and self.old_y:
                self.canvas.create_line(self.old_x, self.old_y, event.x, event.y, width=5,
                               fill=self.color_fg,capstyle=ROUND, smooth=True)
            self.old_x = event.x
            self.old_y = event.y

        if self.drawchange==2:
            if self.old_x and self.old_y:
                self.canvas.create_line(self.old_x, self.old_y, event.x, event.y, width=5,
                               fill='white',capstyle=ROUND, smooth=True)
            self.old_x = event.x
            self.old_y = event.y

    def on_button_press(self, event):
        if self.drawchange == 1:
            self.old_x = event.x
            self.old_y = event.y
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, fill=self.color_fg)

    def on_move_press(self, event):
        if self.drawchange==1:
            curX, curY = (event.x, event.y)
            self.canvas.coords(self.rect, self.old_x, self.old_y, curX, curY)

    def changetopenciel(self):
        self.drawchange=0

    def changetosquare(self):
        self.drawchange=1

    def changetoeraser(self):
        self.drawchange=2

    def reset(self,event):
        if self.drawchange==0:
            self.old_x = None
            self.old_y = None

    def save(self):
        file = filedialog.asksaveasfilename(filetypes=[('Portable Network Graphics',
                                                        '*.png')])
        if file:
            x = self.master.winfo_rootx() + self.canvas.winfo_x()
            y = self.master.winfo_rooty() + self.canvas.winfo_y()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            PIL.ImageGrab.grab().crop((x, y, x1, y1)).save(file + '.png')

    def clear(self):
        self.canvas.delete(ALL)

    def change_fg(self):
        self.color_fg = colorchooser.askcolor(color=self.color_fg)[1]

    def drawWidgets(self):
        self.controls = Frame(self.master, padx=5, pady=5)
        button = Button(self.controls,text="Pencil",fg="black",command=self.changetopenciel)
        button2 = Button(self.controls,text="Square", fg="black", command=self.changetosquare)
        buttoneraser= Button(self.controls,text="Eraser",fg="black",command=self.changetoeraser)
        buttoncolour = Button(self.controls,text="Color", fg="black", command=self.change_fg)
        button.pack()
        button2.pack()
        buttoneraser.pack()
        buttoncolour.pack()
        self.controls.pack(side=LEFT)

        menu = Menu(self.master)
        self.master.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='Clear',command=self.clear)
        filemenu.add_command(label='Save as', command=self.save)
        filemenu.add_command(label='Exit',command=quit)


if __name__ == '__main__':
    root = Tk()
    main(root)
    root.title('ProtoPhotoEdit')
    root.mainloop()