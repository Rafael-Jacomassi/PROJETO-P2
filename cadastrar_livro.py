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

def cadastrar_livro(usuario_id):
    papel = obter_papel_usuario(usuario_id)

    if papel is None:
        print("Erro: Papel do usuário não encontrado. Contate o administrador.")
        return

    if papel not in ["bibliotecario", "administrador"]:
        print("Você não tem permissão para cadastrar livros.")
        return

    while True:
        titulo = input("Título do livro: ").strip()
        autor = input("Autor do livro: ").strip()

        try:
            ano = int(input("Ano de publicação: "))
        except ValueError:
            print("Ano inválido. Cadastro cancelado.")
            continue

        while True:
            restrito = input("Este livro é de acesso restrito? (s/n): ").strip().lower()
            if restrito in ("s", "n"):
                break
            else:
                print("Resposta inválida! Por favor, digite 's' para sim ou 'n' para não.")

        acesso_restrito = 1 if restrito == "s" else 0

        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO livros (titulo, autor, ano, acesso_restrito) VALUES (?, ?, ?, ?)",
                           (titulo, autor, ano, acesso_restrito))
            conn.commit()
            print("Livro cadastrado com sucesso!\n")
        except sqlite3.IntegrityError:
            print("Erro: Livro já cadastrado ou dados inválidos.")
        finally:
            conn.close()

        while True:
            continuar = input("Deseja cadastrar outro livro? (s/n): ").strip().lower()
            if continuar == "n":
                print("Encerrando o cadastro de livros.\n")
                return
            elif continuar == "s":
                break
            else:
                print("Resposta inválida! Por favor, digite 's' para sim ou 'n' para não.")