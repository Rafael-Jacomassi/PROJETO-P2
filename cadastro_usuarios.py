import sqlite3
from hashlib import sha256

def conectar_bd():
    return sqlite3.connect("biblioteca.db")

def listar_papeis():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM papeis")
    papeis = cursor.fetchall()
    conn.close()
    return papeis

def cadastrar_usuario():
    while True:
        conn = conectar_bd()
        cursor = conn.cursor()

        nome = input("Nome completo: ").strip()
        login = input("Login: ").strip()
        email = input("E-mail: ").strip()
        senha = input("Senha: ").strip()
        senha_hash = sha256(senha.encode('utf-8')).hexdigest()

        print("\nPapéis disponíveis:")
        papeis = listar_papeis()
        for papel in papeis:
            print(f"{papel[0]} - {papel[1]}")

        while True:
            try:
                papel_id = int(input("Digite o ID do papel do usuário: "))
                cursor.execute("SELECT 1 FROM papeis WHERE id = ?", (papel_id,))
                if cursor.fetchone():
                    break
                else:
                    print("ID de papel inválido. Tente novamente.")
            except ValueError:
                print("Digite um número válido.")

        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, login, email, senha, papel_id) VALUES (?, ?, ?, ?, ?)",
                (nome, login, email, senha_hash, papel_id)
            )
            conn.commit()
            print("Usuário cadastrado com sucesso!\n")
        except sqlite3.IntegrityError as e:
            print(f"Erro ao cadastrar usuário: {e}")

        conn.close()

        # Pergunta se deseja cadastrar outro usuário
        while True:
            continuar = input("Deseja cadastrar outro usuário? (s/n): ").strip().lower()
            if continuar == 'n':
                print("Encerrando o cadastro de usuários.\n")
                return
            elif continuar == 's':
                break
            else:
                print("Resposta inválida! Por favor, digite 's' para sim ou 'n' para não.")

if __name__ == "__main__":
    cadastrar_usuario()