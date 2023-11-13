#Importando Librerias
import re
import tkinter as tk
from subprocess import call
from tkinter import messagebox
from ply import lex, yacc

#Definir los tokens
tokens = (
    'FOR',
    'INT',
    'ID',
    'NUM',
    'STRING',
    'PLUS',
    'SEMICOLON',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'DOT',
    'EQUALS',
    'LEQ',
    'FN',
    'PRINTLN',
    'CADENA',
    'ADMIRATION',
     
)
t_PLUS = r'\+'
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_DOT = r'\.'
t_EQUALS = r'='
t_LEQ = r'<=' 
t_ADMIRATION = r'!'



def t_STRING(t):
    r'\"[^\"]*\"'
    t.value = t.value[1:-1]
    return t



def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    if t.value == 'for':
        t.type = 'FOR'
    elif t.value == 'int':
        t.type = 'INT'
    elif t.value == 'fn':
        t.type = "FN"
    elif t.value == 'println':
        t.type = 'PRINTLN'
    return t
# Regla para identificar números
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar espacios en blanco y saltos de línea
t_ignore = ' \t\n'

def t_error(t):
    error_message(f"Token desconocido '{t.value[0]}'", t.lineno)
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()

# Definición de la gramática para el análisis sintáctico
def p_hola_loop(p):
    '''hola_loop : FN ID LPAREN RPAREN LBRACE PRINTLN ADMIRATION LPAREN  STRING RPAREN SEMICOLON RBRACE'''
    # FOR LPAREN INT ID EQUALS NUM SEMICOLON ID LEQ NUM SEMICOLON ID PLUS PLUS RPAREN LBRACE ID DOT ID DOT ID LPAREN ID PLUS NUM RPAREN  SEMICOLON RBRACE'''
    pass

# Manejo de errores de sintaxis
def p_error(p):
    if p:
        error_message(f"Syntax error in '{p.value}'", p.lineno)
    else:
        error_message("Syntax error: unexpected end of code", len(code_text.get("1.0", "end-1c").split('\n')))

# Construcción del parser
parser = yacc.yacc()

# Función para el análisis léxico
def lex_analyzer(code):
    lexer.input(code)
    tokens = []
    while True:
        token = lexer.token()
        if not token:
            break
        tokens.append((token.lineno, token.type, token.value))
    return tokens

# Función para el análisis sintáctico
def parse_code(code):
    parser.parse(code, lexer=lexer)

def error_message(message, line_number):
    messagebox.showerror("Syntax Error", f"{message}\nOn the line {line_number}")

# Función para procesar el código ingresado
def process_code():
    code = code_text.get("1.0", "end-1c")
    tokens = lex_analyzer(code)
    result_text.delete("1.0", "end")
    for token in tokens:
        line_number, token_type, token_value = token
        result_text.insert("end", f"Línea ->: {token_type} -> {token_value}\n")
    parse_code(code)

def clear_text():
    code_text.delete("1.0", "end")
    result_text.delete("1.0", "end")

def exit_app():
    window.destroy()

def lexico():
    window.destroy()
    call(["python", "Lexico.py"])

# Creación de la ventana de la interfaz gráfica
window = tk.Tk()
window.title("Lexical Analyzer")
window.geometry("700x480")
window.configure(bg="#DCDCDC")

# Etiqueta y campo de texto para ingresar el código
code_label = tk.Label(window, text="Enter code:", fg="white", bg="#87CEEB", font=("Ubuntu", 14))
code_label.pack(pady=(15, 0))

code_text = tk.Text(window, height=10, width=50)
code_text.pack()

process_frame = tk.Frame(window)
process_frame.pack()

# Botón para procesar el código
process_button = tk.Button(process_frame, text="Process", command=process_code, fg="black", bg="#98FB98", font=("Ubuntu", 12))
process_button.pack(side="left", padx=(5, 5))

# Botón para limpiar el código
clear_button = tk.Button(process_frame, text="Clear", command=clear_text, fg="black", bg="#FFB6C1", font=("Ubuntu", 12))
clear_button.pack(side="left", padx=(5, 5))

# Botón para salir de la aplicación
exit_button = tk.Button(process_frame, text="Exit", command=exit_app, fg="black", bg="#FFA500", font=("Ubuntu", 12))
exit_button.pack(side="left", padx=(5, 5))

menu_button = tk.Button(process_frame,text='Lexical Analyzer',command=lexico,bg="grey", font=("Ubuntu", 12))
menu_button.pack(side="left", padx=(5, 5))

result_label = tk.Label(window, text="Tokens:", fg="black", bg="#FFFF99", font=("Ubuntu", 14))
result_label.pack(pady=(15, 0))

result_text = tk.Text(window, height=10, width=50)
result_text.pack()

# Ejecución de la interfaz gráfica
window.mainloop()