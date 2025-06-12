from visualizar_livros import visualizar_livros
from solicitar_emprestimo import solicitar_emprestimo
from visualizar_solicitacoes_usuario import visualizar_solicitacoes_usuario

def menu_professor(usuario_id):
    while True:
        print("\n--- Menu do Professor ---")
        print("1. Visualizar livros disponíveis")
        print("2. Solicitar empréstimo")
        print("3. Ver minhas solicitações")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            visualizar_livros(usuario_id)
        elif opcao == "2":
            solicitar_emprestimo(usuario_id)
        elif opcao == "3":
            visualizar_solicitacoes_usuario(usuario_id)
        elif opcao == "0":
            print("Saindo do menu do professor...")
            break
        else:
            print("Opção inválida. Tente novamente.")