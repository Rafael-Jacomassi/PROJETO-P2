import sqlite3

def conectar_bd():
    return sqlite3.connect("biblioteca.db")

def visualizar_emprestimos_ativos_filtrados():
    conn = conectar_bd()
    cursor = conn.cursor()

    print("\nDeseja aplicar algum filtro?")
    print("1. Ver todos os empréstimos ativos")
    print("2. Filtrar por nome do usuário")
    print("3. Filtrar por título do livro")
    print("4. Filtrar por intervalo de datas de empréstimo")
    print("0. Cancelar")

    escolha = input("Escolha uma opção: ")

    if escolha == "0":
        conn.close()
        return

    query_base = """
        SELECT e.id, u.nome, l.titulo, l.autor, e.data_emprestimo
        FROM emprestimos e
        JOIN usuarios u ON e.usuario_id = u.id
        JOIN livros l ON e.livro_id = l.id
        WHERE e.data_devolucao IS NULL
    """
    filtros = []
    parametros = []

    if escolha == "2":
        nome_usuario = input("Digite o nome do usuário (ou parte): ").strip()
        filtros.append("u.nome LIKE ?")
        parametros.append(f"%{nome_usuario}%")
    elif escolha == "3":
        titulo_livro = input("Digite o título do livro (ou parte): ").strip()
        filtros.append("l.titulo LIKE ?")
        parametros.append(f"%{titulo_livro}%")
    elif escolha == "4":
        data_inicio = input("Digite a data inicial (AAAA-MM-DD): ").strip()
        data_fim = input("Digite a data final (AAAA-MM-DD): ").strip()
        filtros.append("DATE(e.data_emprestimo) BETWEEN ? AND ?")
        parametros.extend([data_inicio, data_fim])

    if filtros:
        query_base += " AND " + " AND ".join(filtros)

    query_base += " ORDER BY e.data_emprestimo DESC"

    cursor.execute(query_base, tuple(parametros))
    resultados = cursor.fetchall()
    conn.close()

    if not resultados:
        print("Nenhum empréstimo ativo encontrado com os filtros aplicados.")
        return

    print("\nEmpréstimos Ativos:")
    print("-" * 70)
    for emp_id, nome_usuario, titulo, autor, data_emprestimo in resultados:
        print(f"ID: {emp_id} | Usuário: {nome_usuario} | Livro: {titulo} - {autor}")
        print(f"  → Emprestado em: {data_emprestimo}")
    print("-" * 70)