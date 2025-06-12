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

def listar_livros(usuario_id):
    papel = obter_papel_usuario(usuario_id)

    conn = conectar_bd()
    cursor = conn.cursor()

    if papel in ['bibliotecario', 'professor']:
        cursor.execute("SELECT id, titulo, autor FROM livros")
    else:
        cursor.execute("SELECT id, titulo, autor FROM livros WHERE acesso_restrito = 0")

    livros = cursor.fetchall()
    conn.close()
    return livros

def solicitar_emprestimo(usuario_id):
    papel = obter_papel_usuario(usuario_id)
    if papel not in ['aluno', 'professor']:
        print("Seu usuário não tem permissão para solicitar empréstimos ou não está cadastrado.")
        return
    
    livros = listar_livros(usuario_id)
    if not livros:
        print("Nenhum livro disponível para solicitação.")
        return
    
    print("\nLivros disponíveis para solicitação.")
    for idx, (livro_id, titulo, autor) in enumerate(livros, 1):
        print(f"{idx}. {titulo} - {autor}")

    while True:
        try:
            escolha = int(input("Digite o número do livro que deseja solicitar: "))
            if 1 <= escolha <= len(livros):
                break
            else:
                print("Escolha inválida.")
        except ValueError:
            print("Digite um número válido.")

    livro_id = livros[escolha - 1][0]
    data_solicitacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO solicitacoes (usuario_id, livro_id, data_solicitacao) VALUES (?, ?, ?)", (usuario_id, livro_id, data_solicitacao))

    conn.commit()
    conn.close()

    print("Solicitação registrada com sucesso! Aguardando avaliação do bibliotecário.")

if __name__ == "__main__":
    usuario_id = int(input("Digite seu ID de usuário: "))
    solicitar_emprestimo(usuario_id)