from tkinter import *
from tkinter import messagebox

main = Tk()
main.geometry("1366x768")
main.title("Big Bazaar")


class bbmain:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Big Bazaar")

        self.label1 = Label(main)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="main.png")
        self.label1.configure(image=self.img)

        self.button1 = Button(main)
        self.button1.place(relx=0.316, rely=0.446, width=146, height=90)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#ffffff")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#ffffff")
        self.button1.configure(borderwidth="0")
        self.img2 = PhotoImage(file="1.png")
        self.button1.configure(image=self.img2)
        self.button1.configure(command=emp)

        self.button2 = Button(main)
        self.button2.place(relx=0.566, rely=0.448, width=146, height=90)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#ffffff")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="#ffffff")
        self.button2.configure(background="#ffffff")
        self.button2.configure(borderwidth="0")
        self.img3 = PhotoImage(file="2.png")
        self.button2.configure(image=self.img3)
        self.button2.configure(command=adm)


def emp():
    from employee import *

    root.protocol("WM_DELETE_WINDOW", exitt)


def adm():
    from admin import *

    root.protocol("WM_DELETE_WINDOW", exitt)


bb = bbmain(main)
main.mainloop()
