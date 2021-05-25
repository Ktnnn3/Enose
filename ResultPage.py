import tkinter
from ModePage import test
from tkinter import *

tkWindow = Tk()  
tkWindow.attributes("-fullscreen", True)
tkWindow.bind("<Escape>", lambda event: tkWindow.attributes("-fullscreen", False))
print ('choosePage3 = ',test)



#Label Detect Rancid Order
if (test == 1):
    global order 
    order = 'Rancid'
    LabelOrder=Label(tkWindow,text='Detect Rancid Order')
    LabelOrder.place(relx=0.5, rely=0.1, anchor=CENTER)
elif(test==2):
    order = 'Fungi'
    LabelOrder=Label(tkWindow,text='Detect Fungi Order')
    LabelOrder.place(relx=0.5, rely=0.1, anchor=CENTER)
elif(test==3):
    order = 'Insect'
    LabelOrder=Label(tkWindow,text='Detect Insect Order')
    LabelOrder.place(relx=0.5, rely=0.1, anchor=CENTER)
    

# LabelOrder=Label(tkWindow,text='Detect Rancid Order')
# LabelOrder.place(relx=0.5, rely=0.1, anchor=CENTER)

#Label Status
LabelStatus=Label(tkWindow,text='Status of Electrical Nose')
LabelStatus.place(relx=0.5, rely=0.12, anchor=CENTER)



tkWindow.mainloop()