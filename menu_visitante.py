from visualizar_livros import visualizar_livros

def menu_visitante(usuario_id):
    while True:
        print("\n--- Menu do Visitante ---")
        print("1. Visualizar livros disponíveis")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            visualizar_livros(usuario_id)
        elif opcao == "0":
            print("Saindo do menu do visitante...")
            break
        else:
            print("Opção inválida. Tente novamente.")