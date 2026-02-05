import tkinter as tk
from tkinter import messagebox, ttk
from fpdf import FPDF
import os
from datetime import datetime

class ReciboPDF(FPDF):
    def header(self):
        # 1. LOGOTIPO (Adicionado)
        # Verifica se existe um arquivo 'logo.jpg' na pasta
        if os.path.exists("logo.png"):
            # x=center (aprox), w=largura em mm (25mm fica bom em 58mm)
            # Centralizando matematicamente: (58 - 25) / 2 = 16.5
            self.image("logo.png", x=16.5, y=2, w=25)
            self.ln(26) # Pula linha suficiente para a imagem não ficar em cima do texto
        else:
            self.ln(5) # Se não tiver logo, só dá um espaço

        self.set_font('Courier', 'B', 14)
        self.cell(0, 5, 'MARYSMOKE', ln=True, align='C')
        
        self.set_font('Courier', 'I', 8)
        self.cell(0, 5, 'Tabacos Artesanais', ln=True, align='C')
        self.ln(3)

class SistemaRecibo:
    def __init__(self, root):
        self.root = root
        self.root.title("MarySmoke - Sistema v2.0")
        self.root.geometry("400x650")
        
        self.itens_pedido = []
        
        # Cabeçalho da Interface
        tk.Label(root, text="DADOS DO PEDIDO", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Datas e Modelo
        frame_datas = tk.Frame(root)
        frame_datas.pack()
        
        tk.Label(frame_datas, text="Data:").pack(side=tk.LEFT)
        self.entry_data_rec = tk.Entry(frame_datas, width=12)
        self.entry_data_rec.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_data_rec.pack(side=tk.LEFT, padx=5)

        tk.Label(frame_datas, text="Tipo:").pack(side=tk.LEFT)
        self.var_modelo = tk.StringVar(value="À VISTA")
        tk.OptionMenu(frame_datas, self.var_modelo, "À VISTA", "CONSIGNADO").pack(side=tk.LEFT)

        self.sep = ttk.Separator(root, orient='horizontal')
        self.sep.pack(fill='x', pady=10)

        # Adicionar Produtos
        tk.Label(root, text="INCLUIR PRODUTOS", font=("Arial", 10, "bold")).pack()
        
        frame_add = tk.Frame(root)
        frame_add.pack(pady=5)
        
        tk.Label(frame_add, text="Item:").grid(row=0, column=0)
        self.entry_prod = tk.Entry(frame_add, width=20)
        self.entry_prod.grid(row=0, column=1)

        tk.Label(frame_add, text="Qtd:").grid(row=1, column=0)
        self.entry_qtd = tk.Entry(frame_add, width=20)
        self.entry_qtd.grid(row=1, column=1)
        
        btn_add = tk.Button(root, text="Adicionar (+)", command=self.adicionar_item, bg="#3498db", fg="white")
        btn_add.pack(pady=5)

        # Lista Visual
        columns = ("Prod", "Qtd", "Subtotal")
        self.tree = ttk.Treeview(root, columns=columns, show='headings', height=8)
        self.tree.heading("Prod", text="Produto")
        self.tree.heading("Qtd", text="Qtd")
        self.tree.heading("Subtotal", text="R$")
        
        self.tree.column("Prod", width=180)
        self.tree.column("Qtd", width=50, anchor="center")
        self.tree.column("Subtotal", width=80, anchor="center")
        self.tree.pack(pady=5, padx=10)

        # Total
        self.label_total = tk.Label(root, text="TOTAL: R$ 0,00", font=("Arial", 14, "bold"), fg="#27ae60")
        self.label_total.pack(pady=10)

        # Botão Gerar
        btn_gerar = tk.Button(root, text="IMPRIMIR RECIBO (PDF)", command=self.gerar_pdf, 
                             bg="#2c3e50", fg="white", font=("Arial", 11, "bold"), height=2)
        btn_gerar.pack(pady=5, fill="x", padx=20)
        
        tk.Label(root, text="* Salve 'logo.jpg' na mesma pasta para aparecer a imagem", font=("Arial", 8), fg="gray").pack()

    def adicionar_item(self):
        prod = self.entry_prod.get()
        qtd_str = self.entry_qtd.get()
        
        if not prod or not qtd_str:
            messagebox.showwarning("Atenção", "Preencha item e quantidade!")
            return
        
        try:
            qtd = int(qtd_str)
            subtotal = qtd * 50 # R$ 50 fixo para teste
            self.itens_pedido.append({"prod": prod, "qtd": qtd, "subtotal": subtotal})
            self.tree.insert("", "end", values=(prod, qtd, f"{subtotal:.2f}"))
            
            self.entry_prod.delete(0, tk.END)
            self.entry_qtd.delete(0, tk.END)
            self.entry_prod.focus()
            self.atualizar_total_label()
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida (use números inteiros)")

    def atualizar_total_label(self):
        total = sum(item["subtotal"] for item in self.itens_pedido)
        self.label_total.config(text=f"TOTAL: R$ {total:.2f}")

    def gerar_pdf(self):
        if not self.itens_pedido:
            messagebox.showwarning("Vazio", "Adicione produtos antes de gerar!")
            return

        # --- CONFIGURAÇÃO DA PÁGINA ---
        # Largura 58mm
        pdf = ReciboPDF(orientation='P', unit='mm', format=(58, 200))
        
        # --- MARGENS AUMENTADAS PARA 6mm --- (Evita corte lateral)
        pdf.set_margins(left=6, top=5, right=6)
        
        pdf.add_page()
        
        # Detalhes do Cliente
        pdf.set_font('Courier', '', 9)
        pdf.cell(0, 4, f'DATA: {self.entry_data_rec.get()}', ln=True)
        pdf.cell(0, 4, f'MOD.: {self.var_modelo.get()}', ln=True)
        pdf.ln(2)
        
        pdf.set_font('Courier', 'B', 10)
        pdf.cell(0, 4, '-' * 24, ln=True, align='C') # Reduzi traços para caber na margem maior

        # Cabeçalho da Tabela
        pdf.set_font('Courier', 'B', 9)
        pdf.cell(24, 4, 'ITEM', 0)
        pdf.cell(8, 4, 'QTD', 0, align='C')
        pdf.cell(14, 4, 'TOTAL', 0, align='R', ln=True)
        pdf.set_font('Courier', '', 8)

        # Loop de Itens
        total_geral = 0
        for item in self.itens_pedido:
            # Salva posição Y atual
            y_inicial = pdf.get_y()
            
            # Coluna 1: Produto (Multi-line) com largura reduzida (24mm)
            pdf.multi_cell(24, 4, item["prod"])
            y_final = pdf.get_y()
            
            # Volta para o topo da linha para imprimir Qtd e Valor
            pdf.set_xy(6 + 24, y_inicial) # 6 da margem esquerda + 24 da largura da coluna
            
            # Coluna 2: Qtd
            pdf.cell(8, 4, str(item["qtd"]), align='C')
            
            # Coluna 3: Subtotal
            pdf.cell(14, 4, f'{item["subtotal"]:.0f}', align='R', ln=True)
            
            # Se o nome do produto ocupou mais de uma linha, ajusta o cursor
            if y_final > pdf.get_y():
                pdf.set_y(y_final)
                
            total_geral += item["subtotal"]

        pdf.ln(3)
        pdf.set_font('Courier', 'B', 10)
        pdf.cell(0, 4, '-' * 24, ln=True, align='C')
        
        # --- VALOR TOTAL ---
        # Aumentei o tamanho da fonte levemente e removi a borda direita forçada
        pdf.ln(2)
        pdf.set_font('Courier', 'B', 12)
        # align='R' empurra para a margem direita (agora 6mm, mais segura)
        pdf.cell(0, 6, f'TOTAL R$ {total_geral:.2f}', ln=True, align='R')
        
        pdf.ln(5)
        pdf.set_font('Courier', 'I', 7)
        pdf.multi_cell(0, 3, 'Conferencia no ato da entrega.\nObrigado!', align='C')

        nome_arquivo = "recibo_marysmoke_logo.pdf"
        pdf.output(nome_arquivo)
        os.startfile(nome_arquivo)

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaRecibo(root)
    root.mainloop()