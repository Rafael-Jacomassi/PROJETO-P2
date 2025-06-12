import sqlite3

def conectar_bd():
    return sqlite3.connect("biblioteca.db")

def visualizar_solicitacoes_usuario(usuario_id):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.id, l.titulo, l.autor, s.status, s.data_solicitacao
        FROM solicitacoes s
        JOIN livros l ON s.livro_id = l.id
        WHERE s.usuario_id = ?
        ORDER BY s.data_solicitacao DESC
    """, (usuario_id,))
    
    solicitacoes = cursor.fetchall()
    conn.close()

    if not solicitacoes:
        print("Você não fez nenhuma solicitação de empréstimo.")
        return

    print("\nSuas Solicitações de Empréstimo:\n")
    for id_, titulo, autor, status, data in solicitacoes:
        print(f"ID: {id_} | Livro: {titulo} - {autor} | Status: {status.upper()} | Data: {data}")

if __name__ == "__main__":
    usuario_id = int(input("Digite seu ID de usuário: "))
    visualizar_solicitacoes_usuario(usuario_id)