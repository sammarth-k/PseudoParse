from tkinter import *
from tokens import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.filedialog import asksaveasfile
import tkinter.font as tkfont
import os

operations = ["+", "-", "*", "/", "//", "**" "%"]

# All function definitions


def saveas(event=None):
    """Saves file"""

    files = [('Text Document', '*.txt')]
    file = asksaveasfile(filetypes=files, defaultextension=files)
    if file != None:
        path = file.name
        file.write(code_text.get("1.0", END))
        root.title("Pseudo Parse : "+str(os.path.basename(path))+" "+str(path))


def savecode(event=None):
    """Saves code to file"""
    if path != '':
        # extracts code from code_text, textbox for current code and splits into list
        code = code_text.get("1.0", END).split("\n")
        # print(code)
        # There is always '' at the ened of the list, so we pop that out
        code.pop(-1)
        final = ''
        temp = 1
        for i in code:
            # to make sure endline character does not go to the last line of the code
            if temp != len(code):
                final = final+i+"\n"
                temp += 1
            else:
                final = final+i

        # print(final)
        f = open(path, 'w')
        f.write(final)
        f.close()
        messagebox.showinfo("Info", "File saved")
    else:
        saveas()


def clearoutput(event=None):
    """Clears output in output screen."""

    runningcode.config(state=NORMAL)
    runningcode.delete("1.0", "end")
    runningcode.config(state=DISABLED)


def newfile(event=None):
    """Open new file."""

    global path
    if path != '' or code_text.get("1.0", END) != '':
        response = messagebox.askyesnocancel(
            "Warning", "Would you like to overwrite? Any unsaved work will be lost")
        if response == 1:
            code_text.delete("1.0", "end")
            root.title("Pseudo Parse")
            path = ''
    else:
        code_text.delete("1.0", "end")
        root.title("Pseudo Parse")
        path = ''


def openfile(event=None):
    """Opens file."""

    cwd = os.getcwd()
    global path
    try:
        file = filedialog.askopenfile(initialdir=cwd, filetypes=[
                                      ('Text Document', '*.txt')])
        code_text.delete("1.0", "end")
        path = file.name
        code_text.insert(END, file.read())
        root.title("Pseudo Parse : "+str(os.path.basename(path))+" "+str(path))
    except:
        return


def isfloat(n):
    """Checks if number is a float."""

    num = str(n)
    if "." in num:
        return True

    return False


def syntax_error():
    """Throws a syntax error in editor."""

    global runningcode

    runningcode.config(state=NORMAL)
    runningcode.tag_config('error', foreground="red")
    runningcode.insert(END, "\nInvalid Syntax on line "+str(index+1) +
                       "\n"+str(index+1)+"| "+str(final[index])+"\n", "error")
    runningcode.config(state=DISABLED)


def runtime_error():
    """Throws a runtime error in editor."""

    global runningcode
    runningcode.config(state=NORMAL)
    runningcode.tag_config('error', foreground="red")
    runningcode.insert(END, "\nRuntime error on line "+str(index+1) +
                       "\n"+str(index+1)+"| "+str(final[index])+"\n", "error")
    runningcode.config(state=DISABLED)


def pseudo_print():  # normal printing
    """Prints strings and numbers without operations."""
    code = i.split(TOKEN_PRINT+" ")
    if "\"" in code[1]:
        code[1] = code[1].replace("\"", "")
    if code[1] in vars:
        code[1] = vars[code[1]]
    if len(read_code) > index+1:
        if read_code[index+1][0:5].lower() == TOKEN_INPUT:
            runningcode.config(state=NORMAL)
            runningcode.insert(END, str(code[1]))
            runningcode.config(state=DISABLED)
        else:
            runningcode.config(state=NORMAL)
            runningcode.insert(END, str(code[1])+"\n")
            runningcode.config(state=DISABLED)
    else:
        runningcode.config(state=NORMAL)
        runningcode.insert(END, str(code[1])+"\n")
        runningcode.config(state=DISABLED)


def pseudo_print2():
    """Printing for variables or printing performed operation."""
    code = i.split(TOKEN_PRINT+" ")
    if "+" in code[1]:
        adding = code[1].split("+")
        # print(adding)
        num1 = adding[0].strip()
        num2 = adding[1].strip()
        # print(num1,num2,"num1num2")
        if num1 in vars:
            num1 = vars[num1]
        if num2 in vars:
            num2 = vars[num2]
        if type(num1) == str and (num1.isdigit() or isfloat(num1)):
            num1 = float(num1)
        elif type(num1) == str:
            num1 = num1.replace("\"", "")
        if type(num2) == str and (num2.isdigit() or isfloat(num2)):
            num2 = float(num2)
        elif type(num2) == str:
            num2 = num2.replace("\"", "")
        runningcode.config(state=NORMAL)
        runningcode.insert(END, str(num1+num2)+"\n")
        runningcode.config(state=DISABLED)

    else:
        for operation in operations:
            if operation in code[1].strip():
                expression = code[1].split(operation)
                num1 = expression[0].strip()
                num2 = expression[1].strip()
                if num1 in vars:
                    num1 = vars[num1]
                if num2 in vars:
                    num2 = vars[num2]
                if type(num1) == str and (num1.isdigit() or isfloat(num1)):
                    num1 = float(num1)
                if type(num2) == str and (num2.isdigit() or isfloat(num2)):
                    num2 = float(num2)
                runningcode.config(state=NORMAL)
                runningcode.insert(END, f"{eval(f'num1 {operation} num2')} \n")
                runningcode.config(state=DISABLED)
                return

    for k in vars:
        if k == code[1].strip():
            runningcode.config(state=NORMAL)
            runningcode.insert(END, str(vars[k])+"\n")
            runningcode.config(state=DISABLED)


def pseudo_input():
    code = i.split(TOKEN_INPUT+" ")
    global var
    global final
    var = code[1]
    # (final)
    # vars[var]=input(read_code[index-1][7:len(read_code[index-1])-1])
    if index-1 >= 0 and final[index-1][0:5].lower() == "print":
        vars[var] = simpledialog.askstring(
            title="Input", prompt=read_code[index-1][7:len(read_code[index-1])-1])
    else:
        vars[var] = simpledialog.askstring(title="Input", prompt="")
    runningcode.config(state=NORMAL)
    runningcode.tag_config("input", foreground="#2CE3AA")
    runningcode.insert(END, str(vars[var])+"\n", "input")
    runningcode.config(state=DISABLED)


def pseudo_set_var():
    code = i.split("=")
    # print(code)
    code[0] = code[0].split()
    if code[1].isdigit():
        vars[code[0][-1]] = int(code[1])  # if variable should store digit
    elif isfloat(code[1]):
        vars[code[0][-1]] = float(code[1])  # if it should store float

    # for all operations, for eg; set z=x+y
    elif "+" in code[1]:
        add = code[1].split("+")
        first = add[0].strip()
        second = add[1].strip()
        if first in vars:
            first = vars[first]
        if second in vars:
            second = vars[second]
        if str(first).isdigit() or isfloat(first):
            first = float(first)
        if str(second).isdigit() or isfloat(second):
            second = float(second)
        vars[code[0][-1]] = first+second

    else:
        for operation in operations:
            if operation in code[1]:
                sub = code[1].strip().split(operation)
                first = sub[0].strip()
                second = sub[1].strip()
                if first in vars:
                    first = vars[first]
                if second in vars:
                    second = vars[second]
                first = float(first)
                second = float(second)
                vars[code[0][-1]
                     ] = str(eval(f"first {operation} second")).strip()
                break
        else:
            vars[code[0][-1]] = code[1].replace("\"", "").strip()


def pseudo_increment():
    name = i.split(TOKEN_INCREMENT)[1].strip()
    vars[name] += 1


def eval_condition(code, token):
    """Evaluates condition."""
    compare = code.split(token)
    a = compare[0].strip()
    b = compare[1].strip()
    if a in vars:
        a = vars[a]
    if b in vars:
        b = vars[b]
    # print(a,b)
    # print(token)
    #print(bool(eval(f"float(a) {token} float(b)")))
    return bool(eval(f"float(a) {token} float(b)"))


tokens = [TOKEN_GTE, TOKEN_LTE, TOKEN_NE, TOKEN_E, TOKEN_GT, TOKEN_LT]


def pseudo_if():
    """Function for conditionals."""
    global runcode
    global runcode
    global code
    code = i.split("then")
    # print(code)
    # ==
    for token in tokens:
        if token in i:
            runcode = eval_condition(code[0][2:], token)
            break

# WHILE <x> repeat


def pseudo_while():
    """Function for while loop."""
    code = i.split("repeat")
    condition = code[0][5::]
    repeat_lines = []
    for j in range(index+1, len(read_code)):
        if "	" in read_code[j]:
            repeat_lines.append(read_code[j][1:])
        else:
            break
    for token in tokens:
        if token in condition:
            comp = token
            break
    while bool(eval_condition(condition, comp)):
        if bool(eval_condition(condition, comp)) == False:
            break
        final = repeat_lines
        pseudo_execute(final)


global final


def pseudo_execute(final):
    """Executes commands"""
    global index
    global read_code
    global runcode
    global runningcode
    global code
    global i
    for i in final:
        # try:
        if i != '' and not(i.isspace()):
            if i.strip()[0] == TOKEN_COMMENT:
                continue
            if i[0:2].lower() == TOKEN_IF and i.lower().strip().endswith("then"):
                pseudo_if()
                continue
            elif i[0:2].lower() == TOKEN_IF and not(i.lower().strip().endswith("then")):
                syntax_error()
                return
            if i[0:4] == TOKEN_ELSE:
                runcode = not(runcode)
                continue
            if "	" not in i and i[0:4] != TOKEN_ELSE and i[0:2] != TOKEN_IF:
                runcode = True
            else:
                i = i[1::]
            if runcode:
                if i[0:5].lower() == TOKEN_PRINT:
                    for j in operations:
                        if j in i:
                            pseudo_print2()
                            break
                    else:
                        pseudo_print()
                elif i[0:5].lower() == TOKEN_INPUT:
                    pseudo_input()
                elif i[0:3].lower() == TOKEN_VAR:
                    pseudo_set_var()
                elif i[0:5].lower() == TOKEN_LOOP and i.lower().strip().endswith("repeat"):
                    pseudo_while()
                elif i[0:9].lower() == TOKEN_INCREMENT:
                    pseudo_increment()
                else:
                    syntax_error()
                    return

        index += 1
        # except:
        # runtime_error()


def coderun(event=None):
    """Runs pseudocode."""
    global index
    global read_code
    global runcode
    global runningcode
    global code
    global final
    runningcode.config(state=NORMAL)
    runningcode.insert(
        END, "\n"+"----------------------------------------"+"\n")
    runningcode.config(state=DISABLED)

    read_code = code_text.get("1.0", END).split(
        "\n")  # extract code from textbox
    read_code.pop(-1)  # remove extra '' element at end of list

    global vars  # stores all the variables in the form of a dictionary
    vars = {}

    # Executing code
    index = 0
    runcode = True
    if read_code == ['']:
        return
    final = read_code
    pseudo_execute(read_code)


root = Tk()

root.wm_iconbitmap('icon.ico')
root.title("PseudoParse")

path = ''  # stores path of file being worked on

# -----------Front End------------------- 

# Adding logo image
img = Image.open("icon.ico")
img = img.resize((40, 40), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)
panel = Label(root, image=img, bg="#2c2c2c")
panel.image = img
panel.grid(row=0, column=1, sticky="W", columnspan=2)

# Title
title = Label(root, text="PseudoParse", font=(
    'Roboto', 12, "bold"), fg="#2CE3AA", bg="#2c2c2c")
title.grid(row=0, column=1, columnspan=2)

# Code text box
border_color = Frame(root, background="#2CE3AA")
code_text = Text(border_color, width=40, height=20,
                 bg="#393939", fg="thistle1")
code_text.tag_config('bold', font=('Roboto', 10, 'bold'))
code_text.grid(row=0, column=0, padx=2, pady=2)
border_color.grid(row=1, column=1, padx=35, pady=10)
# Set Font
font = tkfont.Font(font=code_text['font'])

# Set Tab size
tab_size = font.measure('    ')
code_text.config(tabs=tab_size)

# Output text box
border_color2 = Frame(root, background="#2CE3AA")
runningcode = Text(border_color2, width=40, height=20,
                   bg="#393939", fg="thistle1")
runningcode.tag_config('bold', font=('Roboto', 10, 'bold'))
runningcode.grid(row=0, column=0, padx=2, pady=2)
border_color2.grid(row=1, column=2, pady=10)
runningcode.config(state=DISABLED)

# MENU
menubar = Menu(root)

# File section
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New          Ctrl+N", command=newfile)
filemenu.add_command(label="Open        Ctrl+O", command=openfile)
filemenu.add_command(label="Save          Ctrl+S", command=savecode)
filemenu.add_command(label="Save as...  Ctrl+Shift+S", command=saveas)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# Shell section
shellmenu = Menu(menubar, tearoff=0)
shellmenu.add_command(label="Run Code       F1", command=coderun)
shellmenu.add_command(label="Clear output  F3", command=clearoutput)
menubar.add_cascade(label="Shell", menu=shellmenu)

# About section
aboutmenu = Menu(menubar, tearoff=0)
aboutmenu.add_command(label="License")
aboutmenu.add_separator()
aboutmenu.add_command(label="Credits")
aboutmenu.add_command(label="Github")
menubar.add_cascade(label="About", menu=aboutmenu)

root.config(menu=menubar)

# Clear ouput button with logo
img_cross = Image.open("cross.png")
img_cross = img_cross.resize((15, 15), Image.ANTIALIAS)
img_cross = ImageTk.PhotoImage(img_cross)
button_clearoutput = Button(
    root, image=img_cross, bg="#2c2c2c", fg='#2CE3AA', border=0, command=clearoutput)
button_clearoutput.grid(row=0, column=3, sticky="W", padx=15)

# Run code button with logo
img_play = Image.open("play.png")
img_play = img_play.resize((15, 15), Image.ANTIALIAS)
img_play = ImageTk.PhotoImage(img_play)
button_runcode = Button(root, image=img_play, bg="#2c2c2c",
                        fg='#2CE3AA', command=coderun, border=0)
button_runcode.grid(row=0, column=2, sticky=E)

# Binding keyboard shortcuts
root.bind('<Control-n>', newfile)
root.bind('<Control-o>', openfile)
root.bind('<Control-s>', savecode)
root.bind('<Control-Shift-s>', saveas)
root.bind('<F1>', coderun)
root.bind('<F3>', clearoutput)

# Copyright section
copyright_text = Label(root, text="©2021,Arjun Singh Sodhi and Sammarth Kumar, All rights reserved",
                       bg="#2c2c2c", fg="#2CE3AA", font=('Roboto', 8))
copyright_text.grid(row=2, column=1, columnspan=2)

root.configure(bg="#2c2c2c")
root.mainloop()
