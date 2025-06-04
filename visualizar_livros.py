import sqlite3

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

def visualizar_livros(usuario_id):
    papel = obter_papel_usuario(usuario_id)
    if papel is None:
        print("Erro: Papel do usuário não encontrado. Contate o administrador.")
        return

    conn = conectar_bd()
    cursor = conn.cursor()

    if papel in ["bibliotecario", "administrador", "professor"]:
        # Esses papéis veem todos os livros
        cursor.execute("SELECT titulo, autor, ano, acesso_restrito FROM livros")
    else:
        # Outros papéis veem só livros não restritos
        cursor.execute("SELECT titulo, autor, ano, acesso_restrito FROM livros WHERE acesso_restrito = 0")

    livros = cursor.fetchall()
    conn.close()

    if not livros:
        print("Nenhum livro disponível para o seu papel.")
        return

    print(f"\nLivros disponíveis:\n")
    for livro in livros:
        titulo, autor, ano, acesso_restrito = livro
        restrito_texto = " (Restrito)" if acesso_restrito else ""
        print(f"- {titulo} - {autor} - {ano}{restrito_texto}")