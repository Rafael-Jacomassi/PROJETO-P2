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

def obter_emprestimos_ativos(usuario_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id, l.titulo, l.autor, e.data_emprestimo
        FROM emprestimos e
        JOIN livros l ON e.livro_id = l.id
        WHERE e.usuario_id = ? AND e.data_devolucao IS NULL
    """, (usuario_id,))
    emprestimos = cursor.fetchall()
    conn.close()
    return emprestimos

def registrar_devolucao():
    usuario_id = int(input("Digite o ID do usuário que está devolvendo o livro: "))

    emprestimos = obter_emprestimos_ativos(usuario_id)
    if not emprestimos:
        print("Nenhum empréstimo ativo encontrado para esse usuário.")
        return

    print("\nEmpréstimos ativos:")
    for idx, (emprestimo_id, titulo, autor, data_emprestimo) in enumerate(emprestimos, 1):
        print(f"{idx}. {titulo} - {autor} (Emprestado em {data_emprestimo})")

    while True:
        try:
            escolha = int(input("Escolha o número do livro que deseja registrar a devolução: "))
            if 1 <= escolha <= len(emprestimos):
                break
            else:
                print("Número inválido, tente novamente.")
        except ValueError:
            print("Por favor, digite um número válido.")

    emprestimo_id = emprestimos[escolha - 1][0]
    data_devolucao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE emprestimos
        SET data_devolucao = ?
        WHERE id = ?
    """, (data_devolucao, emprestimo_id))
    conn.commit()
    conn.close()

    print("Devolução registrada com sucesso!")