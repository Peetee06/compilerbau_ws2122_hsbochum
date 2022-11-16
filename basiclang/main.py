###########
# simple GUI for a compiler subject "Compilerbau WS21/22"
# Firstly the code should be saved in a document or loaded before using run.
# Func is a placeholder for the Backend.
# The interface is to implement under line 73 Func.run.
###########
import parser_
###########
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
from code_generator import CodeGenerator
from abstract_stack_machine import AbstractStackMachine
from lexer_ import Lexer

###########
# creating a Tk object
###########
compiler = Tk()
compiler.title('Compiler WS21/22')
file_path = ''


###########
# setting a global path for the saved code
###########
def set_file_path(path):
    global file_path
    file_path = path


###########
# possibility to open an existing file
###########
def open_file():
    path = askopenfilename(filetypes=[('All Files', '*')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)


###########
# save file before run
###########
def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('All Files', '*')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0',
                          'end-1c')  # alternative: use END instead 'end-1c', but beware of the new line caused by 'END'
        file.write(code)
        set_file_path(path)


###########
# run the compiler using Func as source (Lexer, Parser etc.)
###########
def run():
    code_output.delete('1.0', END)  # delete the output for the next run
    if file_path == '':  # if the file isn't saved, don't allow to execute run
        save_prompt = Toplevel()
        text = Label(save_prompt, text='Please save your code')
        text.pack()
        return
    f = open(file_path, "r")  # open the file and read the command
    command = f.read()
    # command = f'{file_path}'
    parser_result, error = parser_.run('<stdin>', command)  # Func.run, interface between Frontend and Backend
    if error:  # catch an error if occur
        code_output.insert('1.0', error.as_string())
    lexer = Lexer('<stdin>', command)
    lexer_result, error = lexer.make_tokens()
    syntax_tree_result = parser_result.conv_to_syntax_tree()
    intermediate_code = CodeGenerator(syntax_tree_result).generate_ir()
    asm_result = AbstractStackMachine(intermediate_code).evaluate()
    if error:  # catch an error if occur
        code_output.insert('1.0', error.as_string())
    elif parser_result:
        code_output.insert('1.0', 'ASM Result: ' + str(asm_result) + '\n\n')
        code_output.insert('1.0', 'Intermediate Code Result:\n' + str(intermediate_code) + '\n\n')
        code_output.insert('1.0', 'Parser Result:\n' + str(parser_result) + '\n\n')
        code_output.insert('1.0', 'Lexer Result: \n' + str(lexer_result) + '\n\n')


###########
# Frontend of the TK-object
###########
menu_bar = Menu(compiler)

# categories in the menu bar
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_as)
# file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='Exit', command=exit)
menu_bar.add_cascade(label='File', menu=file_menu)

run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_bar)

compiler.config(menu=menu_bar)

# creating a Text()-object for input
editor = Text()
editor.pack()

# creating a Text()-object for output
code_output = Text(height=20)
code_output.pack()

compiler.mainloop()
