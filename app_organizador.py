import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from fpdf import FPDF
from PIL import Image, ImageTk
import database
import ttkbootstrap as tb

def iniciar_app():
    database.criar_tabelas()
    app = tb.Window(themename="darkly")
    app.title("Controle de Estoque")
    app.geometry("800x600")

    # Funções
    def carregar_produtos(filtro=""):
        for row in tree.get_children():
            tree.delete(row)
        for produto in database.obter_produtos(filtro):
            tree.insert("", tk.END, values=produto)

    def adicionar():
        nome = entry_nome.get()
        quantidade = entry_quantidade.get()
        preco = entry_preco.get()
        if nome and quantidade and preco:
            database.adicionar_produto(nome, int(quantidade), float(preco))
            carregar_produtos()
            limpar()
        else:
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")

    def atualizar():
        selected = tree.selection()
        if selected:
            item = tree.item(selected)
            id = item['values'][0]
            nome = entry_nome.get()
            quantidade = entry_quantidade.get()
            preco = entry_preco.get()
            database.atualizar_produto(id, nome, int(quantidade), float(preco))
            carregar_produtos()
            limpar()

    def excluir():
        selected = tree.selection()
        if selected:
            item = tree.item(selected)
            id = item['values'][0]
            database.excluir_produto(id)
            carregar_produtos()
            limpar()

    def limpar():
        entry_nome.delete(0, tk.END)
        entry_quantidade.delete(0, tk.END)
        entry_preco.delete(0, tk.END)

    def selecionar_produto(event):
        selected = tree.selection()
        if selected:
            item = tree.item(selected)
            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, item['values'][1])

            entry_quantidade.delete(0, tk.END)
            entry_quantidade.insert(0, item['values'][2])

            entry_preco.delete(0, tk.END)
            entry_preco.insert(0, item['values'][3])

    def gerar_pdf():
        produtos = database.obter_produtos()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Relatório de Estoque", ln=True, align='C')

        for produto in produtos:
            pdf.cell(0, 10, f"{produto[1]} | Qtd: {produto[2]} | Preço: R${produto[3]:.2f}", ln=True)

        caminho = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if caminho:
            pdf.output(caminho)
            messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")

    def filtrar(event):
        filtro = entry_busca.get()
        carregar_produtos(filtro)

    # Interface
    frame_top = tb.Frame(app)
    frame_top.pack(pady=10)

    tb.Label(frame_top, text="Nome:").grid(row=0, column=0)
    entry_nome = tb.Entry(frame_top)
    entry_nome.grid(row=0, column=1)

    tb.Label(frame_top, text="Quantidade:").grid(row=0, column=2)
    entry_quantidade = tb.Entry(frame_top)
    entry_quantidade.grid(row=0, column=3)

    tb.Label(frame_top, text="Preço:").grid(row=0, column=4)
    entry_preco = tb.Entry(frame_top)
    entry_preco.grid(row=0, column=5)

    frame_botoes = tb.Frame(app)
    frame_botoes.pack(pady=10)

    add_icon = tb.PhotoImage(file="icons/add.png")
    edit_icon = tb.PhotoImage(file="icons/edit.png")
    delete_icon = tb.PhotoImage(file="icons/delete.png")
    clear_icon = tb.PhotoImage(file="icons/clear.png")
    pdf_icon = tb.PhotoImage(file="icons/pdf.png")

    tb.Button(frame_botoes, image=add_icon, command=adicionar).grid(row=0, column=0, padx=5)
    tb.Button(frame_botoes, image=edit_icon, command=atualizar).grid(row=0, column=1, padx=5)
    tb.Button(frame_botoes, image=delete_icon, command=excluir).grid(row=0, column=2, padx=5)
    tb.Button(frame_botoes, image=clear_icon, command=limpar).grid(row=0, column=3, padx=5)
    tb.Button(frame_botoes, image=pdf_icon, command=gerar_pdf).grid(row=0, column=4, padx=5)

    frame_busca = tb.Frame(app)
    frame_busca.pack(pady=10)

    entry_busca = tb.Entry(frame_busca)
    entry_busca.pack(side=tk.LEFT, padx=5)
    entry_busca.bind("<KeyRelease>", filtrar)

    tree = ttk.Treeview(app, columns=("ID", "Nome", "Quantidade", "Preço"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Quantidade", text="Quantidade")
    tree.heading("Preço", text="Preço")
    tree.pack(pady=20, fill="both", expand=True)
    tree.bind("<<TreeviewSelect>>", selecionar_produto)

    carregar_produtos()
    app.mainloop()
