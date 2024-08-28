import tkinter as tk
from tkinter import ttk
import _sqlite3


class CashFlowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Fluxo de Caixa Família Santa Catarina")
        self.root.geometry("1024x600")  # Tamanho da janela para desktop

        # Inicialização dos valores totais
        self.total_entries = 0
        self.total_exits = 0

        # Frame principal para dividir as telas de entrada e saída
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        # Frame para Entradas
        self.entry_frame = ttk.LabelFrame(self.main_frame, text="Entradas", padding="0")
        self.entry_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Labels e Campos para Entradas
        ttk.Label(self.entry_frame, text="Data").grid(row=0, column=0)
        self.entry_date = tk.Entry(self.entry_frame)
        self.entry_date.grid(row=0, column=1)

        ttk.Label(self.entry_frame, text="Item").grid(row=1, column=0)
        self.entry_item = tk.Entry(self.entry_frame)
        self.entry_item.grid(row=1, column=1)

        ttk.Label(self.entry_frame, text="Valor Unitário (R$)").grid(row=2, column=0)
        self.entry_unit_value = tk.Entry(self.entry_frame)
        self.entry_unit_value.grid(row=2, column=1)

        ttk.Label(self.entry_frame, text="Valor Total (R$)").grid(row=3, column=0)
        self.entry_total_value = tk.Entry(self.entry_frame)
        self.entry_total_value.grid(row=3, column=1)

        # Botão de adicionar entrada com cor verde
        self.add_entry_button = tk.Button(self.entry_frame, text="Adicionar Entrada", command=self.add_entry, bg="green", fg="white")
        self.add_entry_button.grid(row=4, columnspan=2, pady=10)

        # Frame para Saídas
        self.exit_frame = ttk.LabelFrame(self.main_frame, text="Saídas", padding="10")
        self.exit_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Labels e Campos para Saídas
        ttk.Label(self.exit_frame, text="Data").grid(row=0, column=0)
        self.exit_date = tk.Entry(self.exit_frame)
        self.exit_date.grid(row=0, column=1)

        ttk.Label(self.exit_frame, text="Item").grid(row=1, column=0)
        self.exit_item = tk.Entry(self.exit_frame)
        self.exit_item.grid(row=1, column=1)

        ttk.Label(self.exit_frame, text="Valor Unitário (R$)").grid(row=2, column=0)
        self.exit_unit_value = tk.Entry(self.exit_frame)
        self.exit_unit_value.grid(row=2, column=1)

        ttk.Label(self.exit_frame, text="Valor Total (R$)").grid(row=3, column=0)
        self.exit_total_value = tk.Entry(self.exit_frame)
        self.exit_total_value.grid(row=3, column=1)

        # Botão de adicionar saída com cor vermelha
        self.add_exit_button = tk.Button(self.exit_frame, text="Adicionar Saída", command=self.add_exit, bg="red", fg="white")
        self.add_exit_button.grid(row=4, columnspan=2, pady=10)

        # Frame para exibir Entradas e Saídas em colunas separadas
        self.result_frame = ttk.Frame(root)
        self.result_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Text Widgets para exibir Entradas e Saídas
        self.entry_text = tk.Text(self.result_frame, height=15, width=40)
        self.entry_text.pack(side="left", fill="both", expand=True, padx=5)

        self.exit_text = tk.Text(self.result_frame, height=15, width=40)
        self.exit_text.pack(side="right", fill="both", expand=True, padx=5)

        # Label para Exibir Saldo com texto maior e negrito
        self.difference_label = ttk.Label(root, text="Saldo: R$ 0,00", font=("Helvetica", 16, "bold"))
        self.difference_label.pack(pady=10)

    def add_entry(self):
        date = self.entry_date.get()
        item = self.entry_item.get()
        unit_value = self.entry_unit_value.get()
        total_value = self.entry_total_value.get()

        try:
            total_value = float(total_value.replace('R$', '').replace(',', '.'))
        except ValueError:
            self.entry_text.insert(tk.END, "Erro: Valor total inválido\n")
            return

        self.total_entries += total_value

        entry_text = f"Entrada: {date} - {item} - R$ {unit_value} - R$ {total_value}\n"
        self.entry_text.insert(tk.END, entry_text, 'entry')
        self.update_difference()
        self.clear_entry_fields()

    def add_exit(self):
        date = self.exit_date.get()
        item = self.exit_item.get()
        unit_value = self.exit_unit_value.get()
        total_value = self.exit_total_value.get()

        try:
            total_value = float(total_value.replace('R$', '').replace(',', '.'))
        except ValueError:
            self.exit_text.insert(tk.END, "Erro: Valor total inválido\n")
            return

        self.total_exits += total_value

        exit_text = f"Saída: {date} - {item} - R$ {unit_value} - R$ {total_value}\n"
        self.exit_text.insert(tk.END, exit_text, 'exit')
        self.update_difference()
        self.clear_exit_fields()

    def clear_entry_fields(self):
        self.entry_date.delete(0, tk.END)
        self.entry_item.delete(0, tk.END)
        self.entry_unit_value.delete(0, tk.END)
        self.entry_total_value.delete(0, tk.END)

    def clear_exit_fields(self):
        self.exit_date.delete(0, tk.END)
        self.exit_item.delete(0, tk.END)
        self.exit_unit_value.delete(0, tk.END)
        self.exit_total_value.delete(0, tk.END)

    def update_difference(self):
        difference = self.total_entries - self.total_exits
        self.difference_label.config(text=f"Diferença: R$ {difference:,.2f}")

        # Limpa a formatação existente
        self.entry_text.tag_configure('entry', foreground='green', font=("Helvetica", 14))
        self.exit_text.tag_configure('exit', foreground='red', font=("Helvetica", 14))

if __name__ == "__main__":
    root = tk.Tk()
    app = CashFlowApp(root)
    root.mainloop()

##Conectando ao Banco de Dados

conn = _sqlite3.connect('cashflow.db')
cursor = conn.cursor()
