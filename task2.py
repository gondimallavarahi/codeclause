import tkinter as tk
from tkinter import filedialog
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from tkinter import *
from PIL import Image, ImageTk
import os

def save_file():
    file = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if file is not None:
        text = str(editor.get(1.0, tk.END))
        file.write(text)
        file.close()
def open_file():
    editor.delete(1.0, tk.END)
    file = filedialog.askopenfile(mode='r')
    file_extension = os.path.splitext(file.name)[1]
    if file_extension == ".txt":
        if file is not None:
            content = file.read()
            con = list(content)
            con = "".join(con[:-1])
            editor.insert(tk.END, con)
            file.close()
    else:
        mb.showwarning("Not Supported", f"You have selected the wrong file format({file_extension[1:]})\n select txt file")
def exit_application():
   root.destroy()


def copy_text():
   editor.event_generate("<<Copy>>")


def cut_text():
   editor.event_generate("<<Cut>>")


def paste_text():
   editor.event_generate("<<Paste>>")


def select_all():
   editor.tag_add(tk.SEL, "1.0", tk.END)


def delete_last_char():
    try:
        # Get the indices of the selection range
        start, end = editor.tag_ranges(tk.SEL)
    except:
        # Handle the case where no text is selected
        content = editor.get(1.0, tk.END)

        new_content = content[:len(content)-2]

        editor.delete(1.0, tk.END)
        editor.insert(tk.END, new_content)
    else:
        editor.delete(tk.SEL_FIRST, tk.SEL_LAST)
    
def delete_all():
    try:
        # Get the indices of the selection range
        start, end = editor.tag_ranges(tk.SEL)
    except:
        editor.delete(1.0, tk.END)
    else:
        editor.delete(tk.SEL_FIRST, tk.SEL_LAST)

def about_notepad():
   mb.showinfo("About Notepad", "This is just another Notepad, but this is better than all others")


def about_commands():
   commands = """
Under the File Menu:
- 'New' clears the entire Text Area
- 'Open' clears text and opens another file
- 'Save As' saves your file in the same / another extension

Under the Edit Menu:
- 'Copy' copies the selected text to your clipboard
- 'Cut' cuts the selected text and removes it from the text area
- 'Paste' pastes the copied/cut text
- 'Select All' selects the entire text
- 'Delete' deletes the last character 
"""

   mb.showinfo("All commands", commands)

root = tk.Tk()
root.title("Text Editor")

# Create a text editor widget
editor = tk.Text(root)
editor.pack()

# Create a menu bar
menu_bar = tk.Menu(root)

# Create a file menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_separator()
file_menu.add_command(label="Close", command=exit_application)


# Adding the Edit Menu and its components
edit_menu = tk.Menu(menu_bar, tearoff=False, activebackground='DodgerBlue')

edit_menu.add_command(label='Copy', command=copy_text)
edit_menu.add_command(label='Cut', command=cut_text)
edit_menu.add_command(label='Paste', command=paste_text)
edit_menu.add_separator()
edit_menu.add_command(label='Select All', command=select_all)
edit_menu.add_command(label='Delete', command=delete_last_char)
edit_menu.add_command(label="Delete All", command=delete_all)

menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Adding the Help Menu and its components
help_menu = tk.Menu(menu_bar, tearoff=False, activebackground='DodgerBlue')

help_menu.add_command(label='About Notepad', command=about_notepad)
help_menu.add_command(label='About Commands', command=about_commands)

menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)

# Add the menu bar to the root window
root.config(menu=menu_bar)

root.mainloop()