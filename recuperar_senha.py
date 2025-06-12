import sqlite3
import random
import smtplib
from email.mime.text import MIMEText
from hashlib import sha256

def conectar_bd():
    return sqlite3.connect("biblioteca.db")

def recuperar_senha():
    conn = conectar_bd()
    cursor = conn.cursor()

    login = input("Digite seu login: ").strip()
    cursor.execute("SELECT email, bloqueado FROM usuarios WHERE login = ?", (login,))
    resultado = cursor.fetchone()

    if not resultado:
        print("Usuário não encontrado.")
        conn.close()
        return

    email, bloqueado = resultado
    if bloqueado == 1:
        print("Usuário bloqueado. Recuperação não permitida.")
        conn.close()
        return

    #Gera o código e salva no banco de dadps
    codigo_recuperacao = str(random.randint(100000, 999999))
    cursor.execute("UPDATE usuarios SET codigo_recuperacao = ? WHERE login = ?", (codigo_recuperacao, login))
    conn.commit()

    #Dados do remetente e senha de app do gmail
    email_remetente = "queirozrafaja@gmail.com"
    senha_app = "twcc iber kndv danc"

    #Monta a mensagem
    mensagem = MIMEText(f"Seu código de recuperação é: {codigo_recuperacao}")
    mensagem["Subject"] = "Recuperação de senha - Biblioteca"
    mensagem["From"] = email_remetente
    mensagem["To"] = email

    #Envia o email
    try:
        servidor = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        servidor.login(email_remetente, senha_app)
        servidor.sendmail(email_remetente, email, mensagem.as_string())
        servidor.quit()
        print("Código de recuperação enviado para seu e-mail!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        conn.close()
        return

    #Verifica o código
    tentativas = 0
    while tentativas < 5:
        codigo_digitado = input("Digite o código de recuperação recebido no e-mail: ").strip()
        if codigo_digitado == codigo_recuperacao:
            nova_senha = input("Digite sua nova senha: ").strip()
            nova_senha_hash = sha256(nova_senha.encode('utf-8')).hexdigest()
            cursor.execute("UPDATE usuarios SET senha = ?, codigo_recuperacao = NULL WHERE login = ?", (nova_senha_hash, login))
            conn.commit()
            print("Senha redefinida com sucesso!")
            break
        else:
            print("Código incorreto, tente novamente.")
            tentativas += 1

    if tentativas == 5:
        print("Número máximo de tentativas atingido. Recuperação cancelada.")
    
    conn.close()

if __name__ == "__main__":
    recuperar_senha()