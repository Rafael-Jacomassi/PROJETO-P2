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

        # Verifica se login ou email já existem
        cursor.execute("SELECT 1 FROM usuarios WHERE login = ? OR email = ?", (login, email))
        if cursor.fetchone():
            print("Erro: Já existe um usuário com esse login ou e-mail.\n")
            conn.close()
            if not tentar_novamente():
                return
            else:
                continue

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

        ra = None
        # Se o papel for aluno (id 4), solicitar RA e validar
        if papel_id == 4:
            ra = input("Digite o RA do aluno: ").strip()

            # Verifica se o RA está autorizado
            cursor.execute("SELECT 1 FROM ras_validos WHERE ra = ?", (ra,))
            if not cursor.fetchone():
                print("Erro: Este RA não está autorizado para cadastro.")
                conn.close()
                if not tentar_novamente():
                    return
                else:
                    continue

            # Verifica se o RA já foi utilizado
            cursor.execute("SELECT 1 FROM usuarios WHERE ra = ?", (ra,))
            if cursor.fetchone():
                print("Erro: Este RA já está cadastrado.")
                conn.close()
                if not tentar_novamente():
                    return
                else:
                    continue

        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, login, email, senha, papel_id, ra) VALUES (?, ?, ?, ?, ?, ?)",
                (nome, login, email, senha_hash, papel_id, ra)
            )
            conn.commit()
            print("Usuário cadastrado com sucesso!\n")
        except sqlite3.IntegrityError as e:
            print(f"Erro ao cadastrar usuário: {e}")
            conn.close()
            if not tentar_novamente():
                return
            else:
                continue

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

def tentar_novamente():
    while True:
        resp = input("Deseja tentar novamente? (s/n): ").strip().lower()
        if resp == 's':
            return True
        elif resp == 'n':
            print("Retornando ao menu principal.\n")
            return False
        else:
            print("Resposta inválida! Digite 's' para sim ou 'n' para não.")

if __name__ == "__main__":
    cadastrar_usuario()