# Sistema de Biblioteca com Controle de Acesso RBAC

## Como executar o sistema

1. Certifique-se de que os seguintes arquivos estejam na mesma pasta:
   - main.py
   - biblioteca.db
   - Todos os arquivos Python auxiliares (ex: login.py, cadastro.py, menus, etc)

2. Execute o programa principal:
   python main.py

## Sobre o projeto

Este sistema simula um ambiente real de biblioteca universitária, com controle de acesso baseado em papéis (RBAC).

Papéis implementados:
- Bibliotecário
- Professor
- Aluno
- Visitante

Funcionalidades:
- Cadastro e login com autenticação por senha
- Validação de RA para alunos
- Visualização e solicitação de livros por papel
- Empréstimos e devoluções (manuais e por solicitação)
- Registro de novos livros
- Processamento de solicitações pelo bibliotecário

## Banco de Dados

O sistema utiliza o arquivo `biblioteca.db` como banco de dados SQLite.

---

### Observações Finais

- Usuários, livros e RAs podem ser ajustados diretamente no banco ou através do sistema (onde permitido).
- O sistema está preparado para evitar ações indevidas, mas continua em aprimoramento.
- Recomenda-se executar o programa via terminal para melhor visualização.
- A senha padrão que utilizamos para popular os usuários do banco de dados foi 'alunos' (está em hash dentro do banco)
