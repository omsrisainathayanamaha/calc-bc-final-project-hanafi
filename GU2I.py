from tkinter import *
root = Tk()
 
root.title('my box gui')
root.geometry("1920x1080")

label1 = Label(root, text = 'hi').pack()
label2 = Label(root, text = 'hello').pack()

root.mainloop()