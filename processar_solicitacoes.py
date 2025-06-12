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

def processar_solicitacoes(usuario_id_logado):
    papel = obter_papel_usuario(usuario_id_logado)

    if papel not in ["bibliotecario", "administrador"]:
        print("Você não tem permissão para processar solicitações.")
        return

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.id, u.nome, l.titulo, s.livro_id, s.usuario_id
        FROM solicitacoes s
        JOIN usuarios u ON s.usuario_id = u.id
        JOIN livros l ON s.livro_id = l.id
        WHERE s.status = 'pendente'
    """)
    solicitacoes = cursor.fetchall()

    if not solicitacoes:
        print("Não há solicitações pendentes no momento.")
        conn.close()
        return

    print("\nSolicitações pendentes:")
    for idx, (solicitacao_id, nome_usuario, titulo_livro, livro_id, usuario_id) in enumerate(solicitacoes, 1):
        print(f"{idx}. {nome_usuario} solicitou o livro '{titulo_livro}' (ID Solicitação: {solicitacao_id})")

    try:
        escolha = int(input("\nDigite o número da solicitação para processar (ou 0 para cancelar): "))
        if escolha == 0:
            print("Operação cancelada.")
            conn.close()
            return
        if not 1 <= escolha <= len(solicitacoes):
            print("Escolha inválida.")
            conn.close()
            return
    except ValueError:
        print("Entrada inválida.")
        conn.close()
        return

    solicitacao_selecionada = solicitacoes[escolha - 1]
    solicitacao_id, _, _, livro_id, usuario_id = solicitacao_selecionada

    # Verifica se o livro ainda existe
    cursor.execute("SELECT id FROM livros WHERE id = ?", (livro_id,))
    if cursor.fetchone() is None:
        print("Livro não encontrado. Solicitação será marcada como recusada.")
        cursor.execute("UPDATE solicitacoes SET status = 'recusada' WHERE id = ?", (solicitacao_id,))
        conn.commit()
        conn.close()
        return

    # Verifica se o usuário ainda existe
    cursor.execute("SELECT id FROM usuarios WHERE id = ?", (usuario_id,))
    if cursor.fetchone() is None:
        print("Usuário não encontrado. Solicitação será marcada como recusada.")
        cursor.execute("UPDATE solicitacoes SET status = 'recusada' WHERE id = ?", (solicitacao_id,))
        conn.commit()
        conn.close()
        return

    # Verifica se o livro já está emprestado
    cursor.execute("""
        SELECT 1 FROM emprestimos
        WHERE livro_id = ? AND devolvido = 0
    """, (livro_id,))
    if cursor.fetchone():
        print("Este livro já está emprestado. Solicitação será marcada como recusada.")
        cursor.execute("UPDATE solicitacoes SET status = 'recusada' WHERE id = ?", (solicitacao_id,))
        conn.commit()
        conn.close()
        return

    decisao = input("Deseja aprovar (A) ou recusar (R) essa solicitação? ").strip().lower()
    if decisao == 'a':
        data_emprestimo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO emprestimos (livro_id, usuario_id, data_emprestimo, devolvido)
            VALUES (?, ?, ?, 0)
        """, (livro_id, usuario_id, data_emprestimo))
        cursor.execute("UPDATE solicitacoes SET status = 'aprovada' WHERE id = ?", (solicitacao_id,))
        conn.commit()
        print("Empréstimo registrado e solicitação aprovada.")
    elif decisao == 'r':
        cursor.execute("UPDATE solicitacoes SET status = 'recusada' WHERE id = ?", (solicitacao_id,))
        conn.commit()
        print("Solicitação recusada.")
    else:
        print("Decisão inválida. Nenhuma ação realizada.")

    conn.close()