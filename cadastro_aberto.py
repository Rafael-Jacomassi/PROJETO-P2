import sqlite3
from hashlib import sha256

def conectar_bd():
    return sqlite3.connect("biblioteca.db")

def cadastrar_usuario_aberto():
    conn = conectar_bd()
    cursor = conn.cursor()

    print("=== Cadastro Aberto de Usuário ===")
    nome = input("Nome completo: ").strip()
    login = input("Login desejado: ").strip()
    email = input("E-mail: ").strip()
    senha = input("Senha: ").strip()
    senha_hash = sha256(senha.encode('utf-8')).hexdigest()

    # Verifica duplicidade de login ou email
    cursor.execute("SELECT 1 FROM usuarios WHERE login = ? OR email = ?", (login, email))
    if cursor.fetchone():
        print("Erro: Este login ou e-mail já está em uso.")
        conn.close()
        return

    print("\nPapéis disponíveis para cadastro:")
    print("1 - Aluno")
    print("2 - Visitante")

    while True:
        try:
            escolha = int(input("Escolha o papel (1 ou 2): "))
            if escolha in [1, 2]:
                break
            else:
                print("Escolha inválida. Apenas 1 (Aluno) ou 2 (Visitante).")
        except ValueError:
            print("Digite um número válido.")

    # Mapear escolha para id correto do papel no banco
    papel_id_map = {
        1: 4,  # Aluno
        2: 5   # Visitante
    }
    papel_id = papel_id_map[escolha]

    ra = None
    if papel_id == 4:  # Aluno
        ra = input("Digite seu RA: ").strip()

        # Verifica se o RA está autorizado
        cursor.execute("SELECT 1 FROM ras_validos WHERE ra = ?", (ra,))
        if not cursor.fetchone():
            print("Erro: Este RA não está autorizado para cadastro.")
            conn.close()
            return

        # Verifica se o RA já foi utilizado
        cursor.execute("SELECT 1 FROM usuarios WHERE ra = ?", (ra,))
        if cursor.fetchone():
            print("Erro: Este RA já está cadastrado.")
            conn.close()
            return

    try:
        cursor.execute("""
            INSERT INTO usuarios (nome, login, email, senha, papel_id, ra)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, login, email, senha_hash, papel_id, ra))
        conn.commit()
        print("\nCadastro realizado com sucesso!")
    except sqlite3.IntegrityError as e:
        print(f"Erro ao cadastrar usuário: {e}")

    conn.close()

if __name__ == "__main__":
    cadastrar_usuario_aberto()