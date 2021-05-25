from tkinter import *

# import ResultPage


f = ("Arial Black", 55)
styleBox = ("Bahnschrift SemiBold SemiConden", 50)
choose = 0
test = 0

def chooseOption(ch):
    global test
    test = ch
    print('choose = ', test)
    nextPage()


def nextPage():
    tkWindow.destroy()
    import ResultPage
    

# window
tkWindow = Tk()
tkWindow.attributes("-fullscreen", True)
tkWindow.bind("<Escape>", lambda event: tkWindow.attributes(
    "-fullscreen", False))
tkWindow.configure(background='#3d2c32')

# Label Enose
Label(tkWindow, text='> > Electric Nose Mode < < ', font=f, background='#3d2c32',
      fg='#f9ad5a').place(relx=0.5, rely=0.15, anchor=CENTER)

# Buttin Mode
choose = Button(tkWindow, text='Detect Racid Order', bg="White", command=lambda: chooseOption(
    1), font=styleBox, relief=FLAT, background='#f9ad5a', fg='#333D51', width=20).place(relx=0.40, rely=0.35, anchor=CENTER)
choose = Button(tkWindow, text='Detect Racid Order', bg="White", command=lambda: chooseOption(
    1), font=styleBox, relief=FLAT, background='#f4a896', fg='#3d2c32', width=20).place(relx=0.38, rely=0.33, anchor=CENTER)

choose = Button(tkWindow, text='Detect Fungi Order', bg="White", command=lambda: chooseOption(
    2), font=styleBox, relief=FLAT, background='#f9ad5a', fg='#333D51',width=20).place(relx=0.60, rely=0.58, anchor=CENTER)
choose = Button(tkWindow, text='Detect Fungi Order', bg="White", command=lambda: chooseOption(
    2), font=styleBox, relief=FLAT, background='#f4a896', fg='#3d2c32',width=20).place(relx=0.58, rely=0.56, anchor=CENTER)



choose = Button(tkWindow, text='Detect Insect Order', bg="White", command=lambda: chooseOption(
    3), font=styleBox, relief=FLAT, background='#f9ad5a', fg='#333D51',width=20).place(relx=0.40, rely=0.81, anchor=CENTER)
choose = Button(tkWindow, text='Detect Insect Order', bg="White", command=lambda: chooseOption(
    3), font=styleBox, relief=FLAT, background='#f4a896', fg='#3d2c32',width=20).place(relx=0.38, rely=0.79, anchor=CENTER)

# exec(open('ModePage.py').read())


tkWindow.mainloop()
