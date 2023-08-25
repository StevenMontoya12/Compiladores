import tkinter as tk
import re
from tkinter import ttk

class Lexer:
    def __init__(self):
        self.Reservada = ['for', 'do', 'while', 'if', 'else', 'public', 'static', 'void', 'int','main']
        self.Operador = ['=', '+', '-', '*', '/']
        self.Delimitador = ['(', ')', '{', '}', ';']
        self.tokens_regex = {
            'Reservada': '|'.join(r'\b' + re.escape(keyword) + r'\b' for keyword in self.Reservada),
            'Operador': '|'.join(map(re.escape, self.Operador)),
            'Delimitador': '|'.join(map(re.escape, self.Delimitador)),
            'Número': r'\d+(\.\d+)?',
            'Identificador': r'[A-Za-z_]+'
        }
        self.token_patterns = re.compile('|'.join(f'(?P<{t}>{self.tokens_regex[t]})' for t in self.tokens_regex))
        
    def tokenize(self, text):
        tokens = []
        lines = text.split('\n')  # Split the input text into lines
        NúmeroLinea = 1  # Inicializar el número de línea en 1
        for line in lines:
            line_has_tokens = False  # Flag to check if the line has any tokens
            for match in self.token_patterns.finditer(line):
                line_has_tokens = True
                for token_type, token_value in match.groupdict().items():
                    if token_type == 'Identificador' and token_value and len(token_value) > 1:
                        tokens.append((NúmeroLinea, 'Error Lexico', token_value))
                    elif token_type == 'Identificador' and token_value and len(token_value) == 1:
                        tokens.append((NúmeroLinea, 'Identificador', token_value))
                    elif token_value:
                        tokens.append((NúmeroLinea, token_type, token_value))
            if line_has_tokens:
                NúmeroLinea += 1
        return tokens


    def analyze(self, text):
        tokens = self.tokenize(text)
        result = "Token\t\tLexema\t\tLinea\n"
        for line_number, token_type, token_value in tokens:
            result += f"{token_type}\t\t{token_value}\t\t{line_number}\n"
        return result



class LexerApp:
    def __init__(self):
        self.windows = tk.Tk()
        self.windows.title("Analizador léxico")

        self.text_label = tk.Label(text="Analizador Lexico", height=2, width=30, font=("Ubuntu Medium", 28), bg="#4169E1")
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

        self.count_tree = ttk.Treeview(self.windows, columns=("Elemento", "Cantidad"), show="headings")
        self.count_tree.heading("Elemento", text="Elemento")
        self.count_tree.heading("Cantidad", text="Cantidad")
        self.count_tree.pack(pady=5)
        
        self.count_tree.column("Elemento",anchor='center')
        self.count_tree.column("Cantidad", anchor='center')
        
        
        self.tree = ttk.Treeview(self.windows, columns=("Token", "Lexema", "Línea"), show="headings")
        self.tree.heading("Token", text="Token")
        self.tree.heading("Lexema", text="Lexema")
        self.tree.heading("Línea", text="Línea")
        self.tree.pack(pady=5)
        
        self.tree.column("Token", anchor="center")
        self.tree.column("Lexema", anchor="center")
        self.tree.column("Línea", anchor="center")
        



    def analyze_text(self):
        lexer = Lexer()
        text = self.text_input.get("1.0", "end")
        result = lexer.tokenize(text)
        
        # Limpia las entradas existentes en el Treeview
        self.tree.delete(*self.tree.get_children())
        self.count_tree.delete(*self.count_tree.get_children())
        # Diccionario para contabilizar los elementos
        element_counts = {'Reservada': 0, 'Operador': 0, 'Delimitador': 0, 'Número': 0, 'Identificador': 0, '(': 0, ')': 0, '{': 0, '}': 0, ';': 0}
        
        
         # Inserta los resultados en los Treeviews y actualiza el diccionario de contadores
        for line_number, token_type, token_value in result:
            self.tree.insert("", "end", values=(token_type, token_value, line_number))
            if token_type in element_counts:
                element_counts[token_type] += 1
                
        
        # Contar delimitadores
        delimiters = ['(', ')', '{', '}', ';']
        for token_type in delimiters:
            if token_type in element_counts:
                element_counts[token_type] = text.count(token_type)
              
              
        # Etiquetas más descriptivas para delimitadores
        delimiter_labels = {
            '(': 'Parentesis de entrada "("',
            ')': 'Parentesis de salida ")"',
            '{': 'Llave de entrada "{"',
            '}': 'Llave de salida "}"',
            ';': 'Punto y coma ";"'
        }
        
        
        # Inserta las cantidades en la tabla de contadores con etiquetas descriptivas
        for delimiter, count in element_counts.items():
            if delimiter in delimiter_labels:
                self.count_tree.insert("", "end", values=(delimiter_labels[delimiter], count))

                
          # Contar paréntesis y llaves
        for token_type in ['(', ')', '{', '}']:
            element_counts[token_type] = text.count(token_type)
        

         # Inserta las cantidades en la tabla de contadores
        for element, count in element_counts.items():
            self.count_tree.insert("", "end", values=(element, count))


    def clean_text(self): #Define un metodo para limpiar el cuadro de texto y la etiqueta de resultados
        self.text_input.delete("1.0", "end") #Borra el contenido del cuadro del texto
        self.result_label.config(text="") #Limpia el contenido de la etiqueta de resultados

    def exit_app(self): #Define un metodo para salir del programa
        self.windows.destroy()

    def run(self): #Define un metodo para ejecutar la aplicacion de la interfaz grafica
        self.windows.mainloop() #inicia el bucle de la interfaz grafica

app = LexerApp() #Crea una instancia de la clase Lexer app
app.run()   #Ejecuta la aplicacion de la interfaz grafica llamando al metodo "Run"
