from cadastro_usuarios import cadastrar_usuario, listar_papeis
from cadastrar_ra import cadastrar_ra

def menu_administrador(usuario_id):
    while True:
        try:
            print("\n--- Menu Administrador ---")
            print("1 - Cadastrar RA válido")
            print("2 - Cadastrar usuário manualmente")
            print("3 - Logout")

            escolha = input("Escolha uma opção: ").strip()

            if escolha == "1":
                cadastrar_ra()
            elif escolha == "2":
                cadastrar_usuario()
            elif escolha == "3":
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida. Tente novamente.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    menu_administrador()
