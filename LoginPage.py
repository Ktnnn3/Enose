from tkinter import *
from functools import partial
#from tkinter import messagebox
#from tkinter import font
#from tkinter.font import families

style = ('Arial Black',55)
styleTEXT = ('Bahnschrift SemiBold SemiConden',50)
styleBOX = ('Bahnschrift SemiBold SemiConden',45)
	

def nextPage():
    tkWindow.destroy()
    import ModePage
    

#check username n password
def validateLogin(username, password):
    if (username.get()=='cmu' and password.get()=='1234'):
        nextPage()
    else: 
        messagebox.showerror("Can not Login","Incorrect username or password, Please fill it corectly",)

    print("username entered :", username.get())
    print("password entered :", password.get())

    
    

#window
tkWindow = Tk()
tkWindow.attributes("-fullscreen", True)
tkWindow.bind("<Escape>", lambda event: tkWindow.attributes("-fullscreen", False))
tkWindow.configure(background='#3d2c32')

#Enose Login
Label(tkWindow,text=" > > Electrical Nose < <" ,font=style,fg='#f9ad5a',background='#3d2c32').place(relx=0.5, rely=0.43, anchor=CENTER)

#username label and text entry box
usernameLabel = Label(tkWindow, text="Username",font=styleTEXT,fg='#f4a896',background='#3d2c32').place(relx=0.36, rely=0.57, anchor=CENTER)
username = StringVar()
usernameEntry = Entry(tkWindow, textvariable=username,width=12,font=styleBOX,borderwidth=40, relief= FLAT,background='#f4a896',fg='#3d2c32').place(relx=0.63, rely=0.58, anchor=CENTER,height=70) 

#password label and password entry box
passwordLabel = Label(tkWindow,text="Password",font=styleTEXT,fg='#f4a896',background='#3d2c32').place(relx=0.36, rely=0.7, anchor=CENTER)
password = StringVar() 
passwordEntry = Entry(tkWindow, textvariable=password, show='*',width=12,font=styleBOX, borderwidth=40, relief= FLAT,background='#f4a896',fg='#3d2c32').place(relx=0.63, rely=0.7, anchor=CENTER,height=70) 

validateLogin = partial(validateLogin, username, password)

#login button
loginButton = Button(tkWindow, text="Login", command=validateLogin,width=7,font=styleTEXT, relief=GROOVE,fg='#3d2c32',background='#f9ad5a').place(relx=0.5, rely=0.83, anchor=CENTER,height=90)
loginButton = Button(tkWindow, text="Login", command=validateLogin,width=7,font=styleTEXT, relief=GROOVE,fg='#3d2c32',background='#f4a896').place(relx=0.49, rely=0.84, anchor=CENTER,height=90)

tkWindow.mainloop()