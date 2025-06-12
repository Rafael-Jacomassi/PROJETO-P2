import sqlite3

def conectar_bd():
    return sqlite3.connect("biblioteca.db")

def cadastrar_ra():
    print("=== Cadastro de RAs Válidos ===")
    
    while True:
        ra = input("Digite o RA a ser cadastrado (ou 'sair' para encerrar): ").strip()
        if ra.lower() == 'sair':
            print("Encerrando cadastro de RAs.\n")
            break

        if not ra:
            print("RA não pode ser vazio.")
            continue

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM ras_validos WHERE ra = ?", (ra,))
        if cursor.fetchone():
            print("Este RA já está cadastrado como válido.\n")
        else:
            try:
                cursor.execute("INSERT INTO ras_validos (ra) VALUES (?)", (ra,))
                conn.commit()
                print("RA cadastrado com sucesso!\n")
            except sqlite3.IntegrityError:
                print("Erro ao cadastrar o RA. Verifique se ele já existe ou se há erro de digitação.")
        
        conn.close()

if __name__ == "__main__":
    cadastrar_ra()