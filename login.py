import sqlite3
from hashlib import sha256

def conectar_bd():
    return sqlite3.connect("biblioteca.db")

def login_usuario():
    conn = conectar_bd()
    cursor = conn.cursor()

    login = input("Login: ").strip()
    senha = input("Senha: ").strip()
    senha_hash = sha256(senha.encode('utf-8')).hexdigest()

    cursor.execute("SELECT id, nome, senha, bloqueado FROM usuarios WHERE login = ?", (login,))
    usuario = cursor.fetchone()

    if usuario:
        usuario_id, nome, senha_salva, bloqueado = usuario

        if bloqueado:
            print("Usuário bloqueado. Entre em contato com o administrador.")
            return
        
        tentativas = 0
        while tentativas < 5:
            if senha_hash == senha_salva:
                print(f"\nBem-vindo(a), {nome}!\n")
                break
            else:
                tentativas += 1
                print(f"Senha incorreta. Tentativas restantes: {5 - tentativas}")
                if tentativas < 5:
                    senha = input("Digite a senha novamente: ").strip()
                    senha_hash = sha256(senha.encode('utf-8')).hexdigest()

        if tentativas == 5:
            cursor.execute("UPDATE usuarios SET bloqueado = 1 WHERE id = ?", (usuario_id))
            conn.commit()
            print("Número máximo de tentativas atingido, usuário bloqueado.")
    else:
        print("Usuário não encontrado.")

    conn.close()

if __name__ == "__main__":
    login_usuario()