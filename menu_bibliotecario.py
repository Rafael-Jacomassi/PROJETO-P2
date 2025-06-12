from realizar_emprestimo import realizar_emprestimo
from processar_solicitacoes import processar_solicitacoes
from visualizar_livros import visualizar_livros
from visualizar_emprestimos_ativos import visualizar_emprestimos_ativos_filtrados
from visualizar_devolucoes import visualizar_devolucoes_filtradas
from devolucao import registrar_devolucao
from cadastrar_livro import cadastrar_livro

def menu_bibliotecario(usuario_id):
    while True:
        print("\n--- Menu do Bibliotecário ---")
        print("1. Visualizar livros disponíveis")
        print("2. Visualizar empréstimos")
        print("3. Visualizar devoluções")
        print("4. Realizar empréstimo manual")
        print("5. Processar solicitações de empréstimo")
        print("6. Registrar devolução")
        print("7 - Cadastrar novos livros")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            visualizar_livros(usuario_id)
        elif opcao == "2":
            visualizar_emprestimos_ativos_filtrados()
        elif opcao == "3":
            visualizar_devolucoes_filtradas()
        elif opcao == "4":
            realizar_emprestimo(usuario_id)
        elif opcao == "5":
            processar_solicitacoes(usuario_id)
        elif opcao == "6":
            registrar_devolucao(usuario_id)
        elif opcao == "7":
            cadastrar_livro(usuario_id)
        elif opcao == "0":
            print("Saindo do menu do bibliotecário...")
            break
        else:
            print("Opção inválida. Tente novamente.")