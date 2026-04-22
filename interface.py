import tkinter as tk
from tkinter import messagebox, ttk
from fpdf import FPDF
import os
import sys
from datetime import datetime

class ReciboPDF(FPDF):
    def header(self):
        # --- CORREÇÃO DA LOGO ---
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))

        caminho_jpg = os.path.join(application_path, "logo.jpg")
        caminho_png = os.path.join(application_path, "logo.png")

        if os.path.exists(caminho_jpg):
            self.image(caminho_jpg, x=16.5, y=2, w=25)
            self.ln(26)
        elif os.path.exists(caminho_png):
            self.image(caminho_png, x=16.5, y=2, w=25)
            self.ln(26)
        else:
            self.ln(5)

        # --- TEXTO EM NEGRITO ---
        self.set_font('Courier', 'B', 14) 
        self.cell(0, 5, 'MARYSMOKE', ln=True, align='C')
        
        self.set_font('Courier', 'B', 8)
        self.cell(0, 5, 'Tabacos Artesanais', ln=True, align='C')
        self.ln(3)

class SistemaRecibo:
    def __init__(self, root):
        self.root = root
        self.root.title("MarySmoke - Sistema Final")
        self.root.geometry("400x680") # Aumentei um pouco a altura para caber o novo campo
        
        self.itens_pedido = []
        
        # --- Interface ---
        tk.Label(root, text="DADOS DO PEDIDO", font=("Arial", 10, "bold")).pack(pady=5)
        
        frame_datas = tk.Frame(root)
        frame_datas.pack()
        
        tk.Label(frame_datas, text="Data:").pack(side=tk.LEFT)
        self.entry_data_rec = tk.Entry(frame_datas, width=12)
        self.entry_data_rec.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_data_rec.pack(side=tk.LEFT, padx=5)

        tk.Label(frame_datas, text="Tipo:").pack(side=tk.LEFT)
        self.var_modelo = tk.StringVar(value="À VISTA")
        tk.OptionMenu(frame_datas, self.var_modelo, "À VISTA", "CONSIGNADO").pack(side=tk.LEFT)

        # --- NOVO CAMPO: RECEBEDOR ---
        frame_recebedor = tk.Frame(root)
        frame_recebedor.pack(pady=5)
        tk.Label(frame_recebedor, text="Recebedor:").pack(side=tk.LEFT)
        self.entry_recebedor = tk.Entry(frame_recebedor, width=26)
        self.entry_recebedor.pack(side=tk.LEFT, padx=5)

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

        btn_gerar = tk.Button(root, text="IMPRIMIR RECIBO (NEGRITO)", command=self.gerar_pdf, 
                             bg="#222", fg="white", font=("Arial", 11, "bold"), height=2)
        btn_gerar.pack(pady=5, fill="x", padx=20)
        
        tk.Label(root, text="* A imagem deve se chamar 'logo.jpg' ou 'logo.png'", font=("Arial", 8), fg="gray").pack()

    def adicionar_item(self):
        prod = self.entry_prod.get()
        qtd_str = self.entry_qtd.get()
        
        if not prod or not qtd_str:
            messagebox.showwarning("Atenção", "Preencha item e quantidade!")
            return
        
        try:
            qtd = int(qtd_str)
            subtotal = qtd * 50 # Seu valor atualizado
            self.itens_pedido.append({"prod": prod, "qtd": qtd, "subtotal": subtotal})
            self.tree.insert("", "end", values=(prod, qtd, f"{subtotal:.2f}"))
            
            self.entry_prod.delete(0, tk.END)
            self.entry_qtd.delete(0, tk.END)
            self.entry_prod.focus()
            self.atualizar_total_label()
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida")

    def atualizar_total_label(self):
        total = sum(item["subtotal"] for item in self.itens_pedido)
        self.label_total.config(text=f"TOTAL: R$ {total:.2f}")

    def gerar_pdf(self):
        if not self.itens_pedido:
            messagebox.showwarning("Vazio", "Adicione produtos!")
            return

        recebedor = self.entry_recebedor.get().strip().upper()
        if not recebedor:
            recebedor = "NÃO INFORMADO"

        # 58mm x 200mm
        pdf = ReciboPDF(orientation='P', unit='mm', format=(58, 200))
        
        # Margens laterais de 6mm
        pdf.set_margins(left=6, top=5, right=6)
        
        pdf.add_page()
        
        # --- CLIENTE / RECEBEDOR (NEGRITO) ---
        pdf.set_font('Courier', 'B', 9)
        pdf.cell(0, 4, f'DATA: {self.entry_data_rec.get()}', ln=True)
        pdf.cell(0, 4, f'MOD.: {self.var_modelo.get()}', ln=True)
        # O uso do multi_cell previne que nomes grandes cortem
        pdf.multi_cell(0, 4, f'REC.: {recebedor}')
        pdf.ln(2)
        
        pdf.set_font('Courier', 'B', 10)
        pdf.cell(0, 4, '-' * 24, ln=True, align='C')

        # --- CABEÇALHO TABELA (NEGRITO) ---
        pdf.set_font('Courier', 'B', 9)
        pdf.cell(24, 4, 'ITEM', 0)
        pdf.cell(8, 4, 'QTD', 0, align='C')
        pdf.cell(14, 4, 'TOTAL', 0, align='R', ln=True)

        # --- LOOP DE ITENS (NEGRITO) ---
        pdf.set_font('Courier', 'B', 8) 

        total_geral = 0
        for item in self.itens_pedido:
            y_inicial = pdf.get_y()
            
            pdf.multi_cell(24, 4, item["prod"])
            y_final = pdf.get_y()
            
            pdf.set_xy(6 + 24, y_inicial)
            
            pdf.cell(8, 4, str(item["qtd"]), align='C')
            pdf.cell(14, 4, f'{item["subtotal"]:.0f}', align='R', ln=True)
            
            if y_final > pdf.get_y():
                pdf.set_y(y_final)
                
            total_geral += item["subtotal"]

        pdf.ln(3)
        pdf.set_font('Courier', 'B', 10)
        pdf.cell(0, 4, '-' * 24, ln=True, align='C')
        
        # --- TOTAL (NEGRITO) ---
        pdf.ln(2)
        pdf.set_font('Courier', 'B', 12)
        pdf.cell(0, 6, f'TOTAL R$ {total_geral:.2f}', ln=True, align='R')
        
        # --- RODAPÉ (NEGRITO) ---
        pdf.ln(5)
        pdf.set_font('Courier', 'B', 7)
        pdf.multi_cell(0, 3, 'Conferencia no ato da entrega.\nObrigado!', align='C')

        nome_arquivo = "recibo_marysmoke_bold.pdf"
        pdf.output(nome_arquivo)
        os.startfile(nome_arquivo)

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaRecibo(root)
    root.mainloop()