import tkinter as tk
from PIL import ImageTk
import sqlite3
from numpy import random
import pyglet

bg_clr = '#3d6466'

pyglet.font.add_file("fonts/Ubuntu-Bold.ttf")
pyglet.font.add_file("fonts/Shanti-Regular.ttf")

def clear_widgets(frame):
	# select all frame widgets and delete them
	for widget in frame.winfo_children():
		widget.destroy()

def fetch_db():
    connection = sqlite3.connect("data/recipes.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sqlite_schema WHERE type='table';")
    all_tables = cursor.fetchall()
    
    #adding randomness
    idx = random.randint(0, len(all_tables)-1)

    #fetch ingredients:
    table_name = all_tables[idx][1]
    cursor.execute("SELECT * FROM " + table_name + ";")
    table_rec = cursor.fetchall()
    
    connection.close()
    return table_name, table_rec

def preprocess(table_name, table_rec):
    title = table_name[:-6]
    title = "".join([char if char.islower() else " " + char for char in title])

    ing = []
    for i in table_rec:
        name = i[1]
        qty = i[2]
        unit = i[3]
        ing.append(qty + " " + unit + " of " + name)
    
    return title, ing

def load_frame1():
    clear_widgets(frame2)
    frame1.tkraise()
    #widgets for frame1
    #for image widget
    frame1.pack_propagate(False)
    logo_img = ImageTk.PhotoImage(file = "assets/RRecipe_logo.png")
    logo_wid = tk.Label(frame1, image = logo_img, bg = bg_clr)
    logo_wid.image = logo_img
    logo_wid.pack()

    #for text widget
    tk.Label(frame1, 
            text = "Ready for the random recipe?", 
            bg = bg_clr, 
            fg = "white", 
            font = ("Shanti", 14)).pack()

    #for button widget
    tk.Button(frame1, 
            text = "SHUFFLE", 
            font = ("Ubuntu", 20), 
            bg = "#28393a", 
            fg="white", 
            cursor = "hand2", 
            activebackground = "#badee2", 
            activeforeground = "black", 
            command = lambda:load_frame2()
            ).pack(pady = 20)


def load_frame2():
    clear_widgets(frame1)
    frame2.tkraise()
    table_name, table_rec = fetch_db()
    title, ing = preprocess(table_name, table_rec)

    logo_img = ImageTk.PhotoImage(file = "assets/RRecipe_logo_bottom.png")
    logo_wid = tk.Label(frame2, image = logo_img, bg = bg_clr)
    logo_wid.image = logo_img
    logo_wid.pack(pady = 20)


    tk.Label(frame2, 
            text = title, 
            bg = bg_clr, 
            fg = "white", 
            font = ("Ubuntu", 20)
            ).pack(pady = 25)

    for i in ing:
            tk.Label(frame2, 
                text = i, 
                bg = "#28393a", 
                fg = "white", 
                font = ("Shanti", 12)
                ).pack(fill = "both")
    
    tk.Button(frame2, 
            text = "BACK", 
            font = ("Ubuntu", 18), 
            bg = "#28393a", 
            fg="white", 
            cursor = "hand2", 
            activebackground = "#badee2", 
            activeforeground = "black", 
            command = lambda:load_frame1()
            ).pack(pady = 20)




# initiallize app
root = tk.Tk()
root.title("Recipe Picker")
root.eval("tk::PlaceWindow . center")

#frames are like pages
frame1 = tk.Frame(root,width=500,height=600,bg=bg_clr)
frame2 = tk.Frame(root,bg=bg_clr)

frame1.grid(row=0,column = 0)
frame2.grid(row=0,column = 0)


#to get the center of the screen:
# x = root.winfo_screenwidth()//2 - places the window at the center of width
# y = int(root.winfo_screenheight()*0.1) - places the window at 10% from the top
# root.geometry('500x600' + str(x) + '+' + str(y))

load_frame1()

# run app
root.mainloop() 