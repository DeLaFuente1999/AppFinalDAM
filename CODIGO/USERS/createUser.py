import tkinter

root = tkinter.Tk()
root.title("EMZ")
root.geometry("1000x500")

frame_title = tkinter.Frame(root)

frame_title.grid(row=0, column=0, padx=(50,0))
title = tkinter.Label(frame_title, text="Añadir Usuarios", font=("Arial", 24))
title.grid(pady=(27, 10)) 

frame_textBox = tkinter.Frame(root)
frame_textBox.grid(row=1, column=0, padx=(50,0))
entry1 = tkinter.Entry(frame_textBox)
entry1.grid(pady=(27, 10))


root.mainloop()