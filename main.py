import sqlite3
from menu_bibliotecario import menu_bibliotecario
from menu_professor import menu_professor
from menu_aluno import menu_aluno
from menu_visitante import menu_visitante
from menu_administrador import menu_administrador
from login import login

from cadastro_aberto import cadastrar_usuario_aberto
from recuperar_senha import recuperar_senha

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

def iniciar_sistema(usuario_id):
    papel = obter_papel_usuario(usuario_id)

    if papel == "administrador":
        menu_administrador(usuario_id)
    elif papel == "bibliotecario":
        menu_bibliotecario(usuario_id)
    elif papel == "professor":
        menu_professor(usuario_id)
    elif papel == "aluno":
        menu_aluno(usuario_id)
    elif papel == "visitante":
        menu_visitante(usuario_id)
    else:
        print("Papel de usuário não reconhecido. Contate o administrador.")

def menu_principal():
    while True:
        print("\n--- Sistema da Biblioteca ---")
        print("1. Login")
        print("2. Esqueci minha senha")
        print("3. Cadastro")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            login_resultado = login()
            if login_resultado:
                usuario_id, _ = login_resultado
                iniciar_sistema(usuario_id)
            else:
                print("Falha no login ou usuário bloqueado.")
        elif opcao == "2":
            recuperar_senha()
        elif opcao == "3":
            cadastrar_usuario_aberto()
        elif opcao == "0":
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

def main():
    menu_principal()

if __name__ == "__main__":
    main()