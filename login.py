import sqlite3
import hashlib

def conectar_bd():
    return sqlite3.connect("biblioteca.db")

def hash_senha(senha):
    """Retorna o hash SHA-256 da senha"""
    return hashlib.sha256(senha.encode()).hexdigest()

def obter_usuario_por_login(login_usuario):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id, senha, papel_id, bloqueado, tentativas FROM usuarios WHERE login = ?", (login_usuario,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado  # tupla ou None

def obter_nome_papel(papel_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM papeis WHERE id = ?", (papel_id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def atualizar_tentativas(usuario_id, tentativas):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET tentativas = ? WHERE id = ?", (tentativas, usuario_id))
    conn.commit()
    conn.close()

def bloquear_usuario(usuario_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET bloqueado = 1 WHERE id = ?", (usuario_id,))
    conn.commit()
    conn.close()

def login():
    while True:
        login_usuario = input("Login do usuário: ").strip()
        senha = input("Senha: ").strip()

        usuario = obter_usuario_por_login(login_usuario)

        if not usuario:
            print("Usuário não encontrado.")
            continue  # tenta novamente

        usuario_id, senha_hash_bd, papel_id, bloqueado, tentativas = usuario

        if bloqueado:
            print("Usuário bloqueado devido a muitas tentativas falhas. Contate o administrador.")
            return None

        senha_hash_input = hash_senha(senha)

        if senha_hash_input == senha_hash_bd:
            # Login OK
            # Resetar tentativas
            atualizar_tentativas(usuario_id, 0)
            papel_nome = obter_nome_papel(papel_id)
            print(f"Login realizado com sucesso!")
            return (usuario_id, papel_nome)
        else:
            # Senha incorreta
            tentativas += 1
            atualizar_tentativas(usuario_id, tentativas)
            print(f"Senha incorreta. Tentativa {tentativas} de 5.")

            if tentativas >= 5:
                bloquear_usuario(usuario_id)
                print("Usuário bloqueado por muitas tentativas incorretas.")
                return None
            # continua o loop para nova tentativa

if __name__ == "__main__":
    resultado = login()
    if resultado:
        usuario_id, papel = resultado
        print(f"Bem-vindo(a)!")
