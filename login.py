import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
import database
import app

def login():
    username = entry_usuario.get()
    senha = entry_senha.get()
    if database.autenticar_usuario(username, senha):
        root.destroy()
        app.iniciar_app()
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos.")

# Interface
root = ttk.Window(themename="darkly")
root.title("Login")
root.geometry("300x200")

frame = ttk.Frame(root, padding=20)
frame.pack(expand=True)

ttk.Label(frame, text="Usuário:").pack()
entry_usuario = ttk.Entry(frame)
entry_usuario.pack()

ttk.Label(frame, text="Senha:").pack()
entry_senha = ttk.Entry(frame, show="*")
entry_senha.pack()

ttk.Button(frame, text="Login", command=login).pack(pady=10)

root.mainloop()
