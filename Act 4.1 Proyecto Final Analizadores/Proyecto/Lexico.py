import re
import tkinter as tk
from tkinter import ttk
from subprocess import call

class Lexer:
    def __init__(self):
        self.reservada_keywords = ['if', 'else', 'while', 'for', 'int', 'float', 'import', 'package', 'func', 'fn', 'println!']
        self.Simboloss = ['+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=', '(', ')', '{', '}', ';', ',', '"', "'","!"]

        self.token_patterns = [
            ('Cadena', r'"(?:[^"\\]|\\.)*"'),
            ('VARIABLE', r'\$\w+'),
            ('Numero', r'\d+(\.\d+)?'),
            ('reservada', '|'.join(r'\b' + re.escape(keyword) + r'(?![A-Za-z0-9_])' for keyword in self.reservada_keywords)),
            ('Identificador', r'[A-Za-z_][A-Za-z0-9_]*'),
            ('Simbolos', '|'.join(map(re.escape, self.Simboloss))),
            ('SPACE', r'\s+'),
        ]

        self.token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_patterns)
        self.token_pattern = re.compile(self.token_regex)

    def tokenize(self, text):
        tokens = []
        position = 0
        while position < len(text):
            match = self.token_pattern.match(text, position)
            if match:
                token_type = match.lastgroup
                if token_type != 'SPACE':
                    token_value = match.group(token_type)
                    tokens.append((token_type, token_value))
                position = match.end()
            else:
                position += 1
        return tokens


class LexerApp:
    def __init__(self):
        self.windows = tk.Tk() #Crea una ventana de la clase
        self.windows.title("Lexical Analyzer") #Establece el titulo de la ventana

        #Crea una etiqueta para el titulo de la aplicacion
        self.text_label = tk.Label(text="Lexical Analyzer", height=2, width=40, font=("Ubuntu", 20, 'bold'), fg="#FFF3DA", bg="#FFA500")
        self.text_label.pack(pady=5)

        #Crea un cuadro de texto para la entrada de texto
        self.text_input = tk.Text(self.windows, height=8, width=70, font=("Ubuntu", 12))
        self.text_input.pack(pady=5)

        #Crea un marco para los botones
        self.button_frame = tk.Frame(self.windows)
        self.button_frame.pack()

        #crea un boton para realizar el analisis lexico del texto de entrada
        self.analyze_button = tk.Button(self.button_frame, text="Analyze", command=self.analyze_text, bg="#A8DF8E", font=("Ubuntu", 12))
        self.analyze_button.grid(row=0, column=0, padx=30, pady=10)

        #crea un boton para limpiar el cuadro de texto
        self.clean_button = tk.Button(self.button_frame, text="Clear", command=self.clean_text, bg="cyan", font=("Ubuntu", 12))
        self.clean_button.grid(row=0, column=1, padx=30, pady=10)

        #Crea un boton para salir del programa
        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.exit_app, bg="#FF6969", font=("Ubuntu", 12))
        self.exit_button.grid(row=0, column=2, padx=30, pady=10)
        
        self.menu_button = tk.Button(self.button_frame,text='Syntax Analyzer',command=self.sintactico,bg="grey", font=("Ubuntu", 12))
        self.menu_button.grid(row=0, column=3, padx=30, pady=10)

        self.tree = ttk.Treeview(self.windows, columns=("Linea", "Token", "Funcion", "Reservada", "Cadena", "Identificador", "Símbolo", "Numero"),show="headings")
        self.tree.heading("Linea", text="Line")
        self.tree.heading("Token", text="Token")
        self.tree.heading("Funcion", text="Function")
        self.tree.heading("Reservada", text="Reserved")
        self.tree.heading("Cadena", text="Cadena")
        self.tree.heading("Identificador", text="Identifier")
        self.tree.heading("Símbolo", text="Symbol")
        self.tree.heading("Numero", text="Number")
        self.tree.pack()

         # Configura la alineación y el ancho de las columnas
        columns = ("Linea", "Token", "Funcion", "Reservada", "Cadena", "Identificador", "Símbolo", "Numero")
        column_widths = (70, 100, 95, 100, 70, 90, 70, 80)  # Define los anchos deseados

        for column, width in zip(columns, column_widths):
            self.tree.column(column, anchor="center", width=width)

        self.text_label = tk.Label(text="Count",height=2, width=35, font=("Ubuntu", 20, 'bold'), fg="white",bg="#A52A2A") 
        self.text_label.pack(pady=(15, 0)) 


        self.count_tree = ttk.Treeview(self.windows, columns=("Elemento", "Cantidad"), show="headings")
        self.count_tree.heading("Elemento", text="Element")
        self.count_tree.heading("Cantidad", text="Amount")
        self.count_tree.pack(pady=1)
        
        columns = ("Elemento", "Cantidad")
        column_widths = (300, 300)  # Define los anchos deseados

        for column, width in zip(columns, column_widths):
            self.count_tree.column(column, anchor="center", width=width)
        
    def analyze_text(self):
        lexer = Lexer()
        text = self.text_input.get("1.0", "end")
        lines = text.split('\n')
        tokens_by_line = [lexer.tokenize(line) for line in lines]

        self.tree.delete(*self.tree.get_children())
        self.count_tree.delete(*self.count_tree.get_children())
        
        # Diccionario para contar los tokens
        count_tokens = {
            'Cadena': 0,
            'reservada': 0,
            'Numero': 0,
            'Identificador': 0,
            'Simbolos': 0
        }

    
         # Count elements
        count_elements = {
            ';': 0,
            '(': 0,
            ')': 0,
            '{': 0,
            '}': 0,
        }

        for line_number, line_tokens in enumerate(tokens_by_line, start=1):
            for token_type, token_value in line_tokens:
                # Aquí se procesan los tokens y se envían a la tabla
                row_data = [line_number, token_type, token_value, "", "", "", "", ""]  # Aseguramos que hay 8 elementos
                if token_type == 'Numero':
                    row_data[7] = "x"
                    count_tokens['Numero'] += 1
                elif token_type == 'reservada':
                    row_data[3] = "x"
                    count_tokens['reservada'] += 1
                elif token_type == 'Identificador':
                    row_data[5] = "x"
                    count_tokens['Identificador'] += 1
                elif token_type == 'Simbolos':
                    row_data[6] = "x"
                    count_tokens['Simbolos'] += 1
                    if token_value in count_elements:
                        count_elements[token_value] += 1
                elif token_type == 'Cadena':
                    row_data[4] = "x"
                    count_tokens['Cadena'] += 1

                self.tree.insert("", "end", values=row_data)


        for element, count in count_elements.items():
            self.count_tree.insert("", "end", values=(element, count))

        for token_type, count in count_tokens.items():
            self.count_tree.insert("", "end", values=(token_type, count))

        for token_value in token:
            if token_value in count_elements:
                count_elements[token_value] += 1

        for element, count in count_elements.items():
            self.count_tree.insert("", "end", values=(element, count))


        # Insertar resultados en la tabla de conteo
        for token_type, count in count_tokens.items():
            self.count_tree.insert("", "end", values=(token_type, count))


    def sintactico(self):
        self.windows.destroy()
        call(["python", "Sintactico.py"])


    def clean_text(self):
        self.text_input.delete("1.0", "end")
        self.tree.delete(*self.tree.get_children())
        self.count_tree.delete(*self.count_tree.get_children())

    def exit_app(self): #Define un metodo para salir del programa
        self.windows.destroy()

    def run(self):
        self.windows.mainloop()

app = LexerApp()
app.run()
