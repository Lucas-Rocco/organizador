import sqlite3

def conectar():
    return sqlite3.connect('estoque.db')

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    # Criar usuário admin padrão
    cursor.execute('INSERT OR IGNORE INTO usuarios (id, username, senha) VALUES (1, "admin", "admin")')
    conn.commit()
    conn.close()

def adicionar_produto(nome, quantidade, preco):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)', (nome, quantidade, preco))
    conn.commit()
    conn.close()

def obter_produtos(filtro=""):
    conn = conectar()
    cursor = conn.cursor()
    if filtro:
        cursor.execute('SELECT * FROM produtos WHERE nome LIKE ?', (f'%{filtro}%',))
    else:
        cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    conn.close()
    return produtos

def atualizar_produto(id, nome, quantidade, preco):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('UPDATE produtos SET nome=?, quantidade=?, preco=? WHERE id=?', (nome, quantidade, preco, id))
    conn.commit()
    conn.close()

def excluir_produto(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM produtos WHERE id=?', (id,))
    conn.commit()
    conn.close()

def autenticar_usuario(username, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE username=? AND senha=?', (username, senha))
    usuario = cursor.fetchone()
    conn.close()
    return usuario
