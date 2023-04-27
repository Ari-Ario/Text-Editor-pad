"""A simple Text-editor and pad beside it"""

from tkinter import *
from tkinter import messagebox, ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.colorchooser import askcolor
from PIL import ImageGrab, ImageTk, Image


#function to adjust the background-color of the text-box
def color_adjustment_bg():
    color = askcolor()[1]
    text_box["bg"] = color

#function to adjust the text color of the text-box
def color_adjustment():
    color = askcolor()[1]
    text_box["fg"] = color

#function to adjust the blue color of text in menu-bar
def blue_func():
    color = askcolor(color="blue")[1]
    text_box["fg"] = color

#function to adjust the red color of text in menu-bar
def red_func():
    color = askcolor(color="red")[1]
    text_box["fg"] = color

#function to adjust the yellow color of text in menu-bar
def yellow_func():
    color = askcolor(color="yellow")[1]
    text_box["fg"] = color

#function to adjust the cyan color of text in menu-bar
def cyan_func():
    color = askcolor(color="cyan")[1]
    text_box["fg"] = color

#function to adjust the magenta color of text in menu-bar
def magenta_func():
    color = askcolor(color="magenta")[1]
    text_box["fg"] = color

#function to adjust the black color of text in menu-bar
def black_func():
    color = askcolor(color="black")[1]
    text_box["fg"] = color

#function to adjust the white color of text in menu-bar
def white_func():
    color = askcolor(color="white")[1]
    text_box["fg"] = color

#function to clean all the text
def clean_text_box():
    text_box.delete("1.0", END)

#function to open a file and copy the text into the text-box
def open_file():
    path = askopenfilename(defaultextension="*.*",filetypes=[("All Files", "*.*"), ("Text File", ".txt"), ("PDF File", ".pdf")])
    if not path:
        return error_box()
    with open(path, mode="r", encoding="utf-8") as file:
        text = file.readlines()
        text_box.insert(END, text) 
    win.title(f"Simple Text Editor - {path}")

#function to save the file 
def saveas_file():
    path = asksaveasfilename(defaultextension="*.txt", filetypes=[("Text File", ".txt"),("PDF File", ".pdf"), ("All Files", "*.*")])
    if not path:
        return error_box()
    with open(path, "w") as file:
        text = text_box.get("1.0", END)
        file.write(text)
    win.title(f"Simple Text Editor -{path}")

#function to show a pop-up window, in case you havenot opened or saved the file correctly
def error_box():
    messagebox.showerror("Upps", "something went wrong, Maybe not opened or saved correctly!")

#a pop-up window to show the basic info about open-source code
def message_box():
    messagebox.showinfo("About this app", "This Application is developed by\
                        Ismail Mostafanejad in 2022 - aim of portfolio. It is an open source code/ writtten in Python!")

#function to erase the text-box (Page)
def clear_page():
    text_box.delete("1.0", END)

#function to find the searched keyword
def find(input_entry):
    input_box = text_box.get("1.0", END).split("\n")
    dict = {}
    for i, line in enumerate(input_box):
        count = line.count(input_entry)
        idx = 0
        for j in range(count):
            idx = line.find(input_entry, idx, len(line))
            if i+1 not in dict: 
                dict[i+1] = []
                dict[i+1].append(idx)
            else:
                dict[i+1].append(idx)
            idx +=len(input_entry)
    return dict

#function to search the keyword. it is needs above function: find
def search():
    input_entry = entry_search.get()
    dict= find(input_entry)
    for key, val in dict.items():
        for v in val:
            idx_start, idx_end = f"{key}.{v}", f"{key}.{v + len(input_entry)}"
            text_box.tag_config("start", foreground="red")
            text_box.tag_add("start", idx_start, idx_end)

#complicated method to replace all. Simple method is below. it needs find function.
def replaceall():
    input_entry_search = entry_search.get()
    input_entry_replace = entry_replace.get()
    length = len(input_entry_search) - len(input_entry_replace)
    dict = find(input_entry_search)
    for key, val in dict.items():
        diff = 0
        for v in val:
            idx_start, idx_end = f"{key}.{v+diff}", f"{key}.{v + len(input_entry_search)+diff}"
            text_box.delete(idx_start, idx_end)
            text_box.insert(idx_start , input_entry_replace)
            diff -= length

#simple function of replace. the complicated function is above! this replaces first found word 
def replace():
    input_search = entry_search.get()
    input_replace= entry_replace.get()
    text = text_box.get("1.0", END).split("\n")
    i = 0
    for line in text:
        if input_search not in line:
            i+=1
        else:
            idx_start, idx_end = "", ""
            idx_start = line.find(input_search)
            idx_end = idx_start + len(input_search)
            idx_start, idx_end = f"{i+1}.{idx_start}", f"{i+1}.{idx_end}"
            text_box.delete(str(idx_start), str(idx_end))
            text_box.insert(idx_start, input_replace)
            i+=1
            break

#function of save as button and then exit the text-editor
def save_and_exit():
    saveas_file()
    win.destroy()

#function for undo in menu-Edite
def undo():
    text_box.edit_undo()

#function for redo in menu-Edite
def redo():
    text_box.edit_redo()

#function for most common converters, which will be added later
def converters():
    pass

#a new window for archive
def open_new_win():
    new_win= Tk()
    new_win.title("Archive")
    text_b = Text(new_win)
    text_b.grid(row=0, column=0)
    butt= Button(new_win, text="Close Window", command=new_win.destroy)
    butt.grid(row=1, column=0, sticky=EW)
    f= open("archive.txt", "r")
    list=[]
    lines= f.readlines()
    for line in lines:
        word = line.rstrip()
        if word not in list:
            list.append(word)
    text_b.insert("1.0", "A list of archieve: "+str(list))
    f.close()
        

#code of the main window
root = Tk()
root.title("Text Editor")
win= LabelFrame(root)
win.pack(side=LEFT, fill=BOTH, expand=True)
win.rowconfigure([0,1,2,3,4,5,6,7,8,9], weight=1, minsize=1)
win.columnconfigure([0,1,2], weight=1, minsize=5)

menubar = Menu(win)
root.config(menu=menubar)

file = Menu(menubar, activebackground="cyan", tearoff=0)
menubar.add_cascade(menu=file, label="FILE")
file.add_command(label="New File", command=clean_text_box)
file.add_command(label="Import File", command=open_file)
file.add_command(label="Save As", command=saveas_file)
file.add_separator()
file.add_command(label="Exit", command=win.destroy)

editing = Menu(menubar, activebackground="light blue", tearoff=0)
menubar.add_cascade(menu=editing, label="EDIT")
editing.add_command(label="Undo", command=undo)
editing.add_command(label="Redo", command=redo)
#editing.add_command(label="Edit", command=None)
editing.add_command(label="Clear page", command=clear_page)

tools = Menu(menubar)
tools.add_cascade(menu=tools,label="TOOLS")
tools.add_command(label="Pen", command=None)
tools.add_command(label="Brush", command=None)
tools.add_separator()
tools.add_command(label="Erase", command=None)

#the functions for fontsize-adjustment are defined inside the menu to avoid extra place
size = Menu(menubar, tearoff=0)
menubar.add_cascade(menu=size, label="SIZE")
size.add_command(label="0.5x", command=lambda: text_box.config(font=("Helvetica",10)))
size.add_command(label="1x", command=lambda: text_box.configure(font=("Helvetica", 11)))
size.add_command(label="2x", command=lambda: text_box.config(font=("Helvetica", 12)))
size.add_command(label="3x", command=lambda: text_box.config(font=("Helvetica", 13)))

color = Menu(menubar, tearoff=0)
menubar.add_cascade(menu=color, label="COLOR")
color.add_command(label="Blue", command= blue_func)
color.add_command(label="Red", command=red_func)
color.add_command(label="Yellow", command=yellow_func)
color.add_command(label="Cyan", command=cyan_func)
color.add_command(label="Magenta", command=magenta_func)
color.add_separator()
color.add_command(label="Color Bar", command=color_adjustment)

color_background = Menu(menubar, tearoff=0)
menubar.add_cascade(label="BG-COLOR", menu=color_background)
color_background.add_command(label="Color Chooser", command=color_adjustment_bg)
#help-menu plus messagebox

text_box = Text(win, width=100, height=40, bg="white", undo=True, maxundo=-1)
text_box.grid(row=0, column=1, rowspan=10, sticky="nsew")

scroll_bar = Scrollbar(win, orient="vertical")
scroll_bar.grid(row=0, column=2, rowspan=10, sticky=NS)
text_box.config(yscrollcommand = scroll_bar.set)
scroll_bar.config(command=text_box.yview)

#column of the all buttons and boxes at the left side

entry_search= Entry(win, width=20)
entry_search.grid(row=1, column=0, rowspan=1, sticky="w")
button_search= Button(win, text="Search ", relief=GROOVE, command=search)
button_search.grid(row=1, column=0, rowspan=1, sticky="e")

entry_replace = Entry(win, width=20)
entry_replace.grid(row= 2, column=0, rowspan=1, sticky="w")
button_replace= Button(win, text="Replace", command=replace)
button_replace.grid(row=2, column=0, sticky=E)
button_replaceall= Button(win, text="Rep. All ", relief=GROOVE, command=replaceall)
button_replaceall.grid(row=3, column=0, rowspan=1, sticky=NE)

sep1= ttk.Separator(win, orient="horizontal")
sep1.grid(row=3, column=0, rowspan=1, columnspan=1, sticky=EW)

button_archive= Button(win, text="Show Archive", command=open_new_win)
button_archive.grid(row=5, column=0, sticky=EW)

sep2= ttk.Separator(win, orient="horizontal")
sep2.grid(row=7, column=0, columnspan=1, rowspan=1, sticky=EW)

button_info = Button(win, text="About         ", relief=RAISED, command=message_box)
button_info.grid(row=8, column=0, sticky="ne")
button_saveexit = Button(win, text="Save & Exit", relief=RAISED, command=save_and_exit)
button_saveexit.grid(row=8, column=0, sticky="se")
button_exit=Button(win, text="Exit            ", relief=RAISED, command=win.destroy)
button_exit.grid(row=9, column=0, rowspan=3, columnspan=1, sticky="se")

#function of popup with right-click on text_box
def do_popup(self, event):
    try:
        menu_popup.tk_popup(event.x_root, event.y_root, 0)
    finally:
        menu_popup.grab_release()

#function to copy selected text
def copy():
    global data
    if text_box.selection_get():
        data= text_box.selection_get()
    #e.bind("<Control-c>")

#function to cut selected text
def cut():
    global data
    if text_box.selection_get():
        data= text_box.selection_get()
        text_box.delete("sel.first", "sel.last")
    #text_box.bind("<Control+x>")

#function to paste selected text
def paste():
    global data
    text_box.insert(END, data)

#function to archive selected text for later use. This is connected with show-archive butten
def archive():
    if text_box.selection_get():
        word= text_box.selection_get()
        word= str(word)
        filename= "archive.txt"
        if filename:
            with open(filename, "a") as f:
                f.write("\n")
                f.write(word)
        else:
            with open(filename, "w"):
                f.write(word)

#popup-menu on the textbox
menu_popup = Menu(win, tearoff=0)
menu_popup.add_command(label="copy", command= lambda: copy())
menu_popup.add_command(label="paste", command=lambda: paste())
menu_popup.add_command(label="cut", command= lambda: cut())
menu_popup.add_command(label="Archive", command=lambda: archive())

text_box.bind("<Button-3>", do_popup)

"""Canvas code beside the Text_box"""
brush_width = 5
brush_color = "black"
old_x = None
old_y = None

#function to change pen-color
def brushcolor():
    global brush_color
    color = askcolor()[1]
    brush_color = color

#function to change background-color of the pad
def background_color():
    color = askcolor()[1]
    c["bg"] = color

#function to change the size of the pen
def brush_size_change(width):
    global brush_width
    brush_width= width

#function to paint on the pad
def paint(e):
    global old_x, old_y
    if old_x and old_y:
        c.create_line(old_x, old_y, e.x, e.y, width= brush_width, fill=brush_color, capstyle="round")
    old_x = e.x
    old_y = e.y

#function, which resets the pad as soon as you finish a line
def reset(e):
    global old_x, old_y
    e.x = None
    e.y = None
    old_x, old_y = None, None

#function to erase the pad
def clear_canvas():
    c.delete(ALL)

def creat_img():
    p = c.postscript(file="test.eps", colormode="color", x=0, y=0, height=256, width=200)
    img = Image.open("test.eps")
    #img.save("sth"+".png" , "PNG")

#all labels, buttons and scales on the pad
frame_canvas= LabelFrame(root, text= "Write or paint on the pad")
frame_canvas.pack(side=RIGHT, fill=BOTH, expand=True)
#label_canvas = Label(win, text="Write or paint on the pad", font="Currier")
#label_canvas.grid(row=0, column=3, sticky=N)
c = Canvas(frame_canvas, bg="light cyan", height=600)
c.pack(side=TOP ,expand=True, fill=BOTH)

frame_all_butts= LabelFrame(frame_canvas)
frame_all_butts.pack(side=BOTTOM, expand=True, fill=BOTH)
label_import_img= Button(frame_all_butts, text="Save Photo", relief=RAISED, command=creat_img())
label_import_img.grid(row=0, column=0, sticky=W)
label_control = Label(frame_all_butts, width=15, text="Pen Width \N{RIGHTWARDS ARROW}")
label_control.grid(row=0, column=0)
scale_control = ttk.Scale(frame_all_butts, from_=5, to=100,  command= brush_size_change)
scale_control.set(brush_width)
scale_control.grid(row=0, column=0, sticky=E)

button_brush_color= Button(frame_all_butts, text="Brush Color ", command=brushcolor)
button_brush_color.grid(row= 1, column=0, sticky=W)
button_bg_color= Button(frame_all_butts, text="BG Color   ", relief=SUNKEN, command=background_color)
button_bg_color.grid(row=1, column=0)
button_canvas_clear = Button(frame_all_butts, text="Clear Pad    ", relief=FLAT, command=clear_canvas)
button_canvas_clear.grid(row=1,column=0,sticky=E)

c.bind("<B1-Motion>", paint)
c.bind("<ButtonRelease-1>", reset)


win.mainloop()