import sqlite3
from datetime import datetime

def conectar_bd():
    return sqlite3.connect("biblioteca.db")

def obter_papel_usuario(usuario_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nome FROM usuarios u
        JOIN papeis p ON u.papel_id = p.id
        WHERE u.id = ?
    """, (usuario_id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def realizar_emprestimo(usuario_id):
    papel = obter_papel_usuario(usuario_id)
    if papel not in ['bibliotecario', 'administrador']:
        print("Você não tem permissão para realizar empréstimos.")
        return

    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        livro_id = int(input("Digite o ID do livro para empréstimo: "))
    except ValueError:
        print("ID inválido.")
        conn.close()
        return

    #Verifica se o livro já está emprestado (emprestimos sem devolução)
    cursor.execute("""
        SELECT 1 FROM emprestimos
        WHERE livro_id = ? AND devolvido = 0
    """, (livro_id,))
    if cursor.fetchone():
        print("Este livro já está emprestado e não foi devolvido.")
        conn.close()
        return

    try:
        usuario_emprestimo_id = int(input("Digite o ID do usuário que fará o empréstimo: "))
    except ValueError:
        print("ID inválido.")
        conn.close()
        return

    data_emprestimo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO emprestimos (livro_id, usuario_id, data_emprestimo, devolvido)
        VALUES (?, ?, ?, 0)
    """, (livro_id, usuario_emprestimo_id, data_emprestimo))

    conn.commit()
    conn.close()
    print("Empréstimo realizado com sucesso!")