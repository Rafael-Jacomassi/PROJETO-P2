import sqlite3

def criar_banco():
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()

    #Tabela dos papéis
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS papeis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    );
    """)
    
    #Tabela de usuários
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        login TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        bloqueado INTEGER DEFAULT 0,
        codigo_recuperacao TEXT,
        papel_id INTEGER,
        FOREIGN KEY(papel_id) REFERENCES papeis(id)
    );
    """)

    #Tabela de livros
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    ano INTEGER,
    acesso_restrito INTEGER DEFAULT 0
    );
    """)

    #Tabela de logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        acao TEXT NOT NULL,
        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        );
        """)
    
    #Inserir os papéis se ainda não existirem
    papeis_padrao = ["administrador", "bibliotecario", "professor", "aluno", "visitante"]
    for papel in papeis_padrao:
        cursor.execute("INSERT or IGNORE INTO papeis (nome) VALUES (?)", (papel,))

    conn.commit()
    conn.close()
    print("Banco de dados criados e papéis inseridos com sucesso!")

if __name__ == "__main__":
    criar_banco()