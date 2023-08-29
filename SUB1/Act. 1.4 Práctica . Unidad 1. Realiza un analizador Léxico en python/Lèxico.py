import re
import tkinter as tk
from tkinter import ttk

class Lexer:
    def __init__(self):
        self.reservada_keywords = ['if', 'else', 'while', 'for', 'int', 'float', 'Cadena', 'print', 'programa', 'read', 'terminar', 'imprimir','public','static','void','main']
        self.Simboloss = ['+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=', '(', ')', '{', '}', ';', ',', '"', "'"]
        self.token_patterns = [
            ('Cadena', r'"(?:[^"\\]|\\.)*"'),
            ('VARIABLE', r'\$\w+'),
            ('Numero', r'\d+(\.\d+)?'),
            ('reservada', '|'.join(r'\b' + re.escape(keyword) + r'\b' for keyword in self.reservada_keywords)),
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
        self.windows = tk.Tk()
        self.windows.title("Analizador léxico")

        self.text_label = tk.Label(text="Analizador Lexico", height=2, width=75, font=("Ubuntu Medium", 28), bg="#4169E1")
        self.text_label.pack(pady=5)
        
        self.text_label = tk.Label(text="Compiladores",pady=0 ,height=1, width=38, fg="#ffffff",font=("Ubuntu Medium", 22), bg="#000000")
        self.text_label.pack(pady=1)

        self.text_input = tk.Text(self.windows, height=10, width=65, font=("Verdana", 12))
        self.text_input.pack(pady=5)

        self.button_frame = tk.Frame(self.windows)
        self.button_frame.pack()

        self.analyze_button = tk.Button(self.button_frame, text="Analizar", command=self.analyze_text, bg="#00FFFF", font=("Ubuntu", 14))
        self.analyze_button.grid(row=0, column=0, padx=30, pady=5)

        self.clean_button = tk.Button(self.button_frame, text="Limpiar", command=self.clean_text, bg="#DC143C", font=("Ubuntu", 14))
        self.clean_button.grid(row=0, column=1, padx=30, pady=5)

        self.tree = ttk.Treeview(self.windows, columns=("Linea", "Token", "Valor", "Reservada", "Cadena", "Identificador", "Símbolo"), show="headings")
        self.tree.heading("Linea", text="Linea")
        self.tree.heading("Token", text="Token")
        self.tree.heading("Valor", text="Valor")
        self.tree.heading("Reservada", text="Reservada")
        self.tree.heading("Cadena", text="Cadena")
        self.tree.heading("Identificador", text="Identificador")
        self.tree.heading("Símbolo", text="Símbolo")
        self.tree.pack()
        
        
        self.tree.column("Linea", anchor="center")
        self.tree.column("Token",  anchor="center")
        self.tree.column("Valor",  anchor="center")
        self.tree.column("Reservada",  anchor="center")
        self.tree.column("Cadena",  anchor="center")
        self.tree.column("Identificador",  anchor="center")
        self.tree.column("Símbolo", anchor="center")

        self.count_tree = ttk.Treeview(self.windows, columns=("Elemento", "Cantidad"), show="headings")
        self.count_tree.heading("Elemento", text="Elemento")
        self.count_tree.heading("Cantidad", text="Cantidad")
        self.count_tree.pack(pady=10)
        
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
            'Numero': 0,  # Agregar esta línea
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
                row_data = [line_number, token_type, token_value, "", "", "", ""]
                if token_type == 'reservada':
                    if token_value in lexer.reservada_keywords:
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
                elif token_type == 'Numero':  # Tratar los tokens de tipo Numero
                    row_data[2] = float(token_value)  # Agregar el valor numérico en la columna "Valor" (como float)
                    count_tokens['Numero'] += 1  # Incrementar el contador de Número

                self.tree.insert("", "end", values=row_data)

    # Insertar resultados en la tabla de conteo
        for element, count in count_elements.items():
            self.count_tree.insert("", "end", values=(element, count))

        for token_type, count in count_tokens.items():
            self.count_tree.insert("", "end", values=(token_type, count))

        


        for _, token_value in tokens:
            if token_value in count_elements:
                count_elements[token_value] += 1

        for element, count in count_elements.items():
            self.count_tree.insert("", "end", values=(element, count))


        for token_type, token_value in tokens:
            row_data = [token_type, token_value, "", "", "", ""]
            if token_type == 'reservada':
                if token_value in lexer.reservada_keywords:
                    row_data[2] = "x"
                    count_tokens['reservada'] += 1
            elif token_type == 'Identificador':
                row_data[4] = "x"
                count_tokens['Identificador'] += 1
            elif token_type == 'Simbolos':
                row_data[5] = "x"
                count_tokens['Simbolos'] += 1
            elif token_type == 'Cadena':
                row_data[3] = "x"
                count_tokens['Cadena'] += 1
            elif token_type == 'Numero':  # Agregar esta condición
                    row_data[2] = "x"  # Marcar el contador de Número
                    count_tokens['Numero'] += 1  # Incrementar el contador de Número

            self.tree.insert("", "end", values=row_data)

        for token_type, count in count_elements.items():
            self.count_tree.insert("", "end", values=(element, count))

        for token_type, count in count_tokens.items():
            self.count_tree.insert("", "end", values=(token_type, count))

    def clean_text(self):
        self.text_input.delete("1.0", "end")
        self.tree.delete(*self.tree.get_children())
        self.count_tree.delete(*self.count_tree.get_children())

    def run(self):
        self.windows.mainloop()

app = LexerApp()
app.run()
