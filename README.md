# Rede Lobos - Tools-API (Rede Lobos - Desafio Backend)

## API Documentation (Swagger):
https://app.swaggerhub.com/apis/willianmulia/rede-lobos-api/0.1.0

## Descrição:
Esta aplicação é um simples repositório para gerenciar ferramentas com seus respectivos nomes, links, descrições e tags.

## Linguagem e Banco de Dados:
A aplicação foi desenvolvida utilizando a linguagem Python e o banco de dados MySql.

## Servidor local:
 Utiliza servidor uvicorn - porta 3000.

## Passos para execução do projeto:
### Instalar pacotes:
pip install requirements.txt
### Iniciar o servidor de banco de dados:
Abrir MySQL Workbench e acessar (ou criar) o servidor desejado.
Após, preencher as credenciais de acesso ao servidor no arquivo "***credentials.py***"
### Executar "***main.py***":
Arquivo "main.py" cria e alimenta (se necessário) o *schema* "***db_tools***" e suas respectivas tabelas ["***tools***", "***user***"] (caso já não existem) com informações *default*.
Também inicia o servidor uvicorn (porta 3000). 

## Utilização da API:
### Requisições do tipo "POST":
São permitidas apenas com o login de usuário (JWT Authentication). Deve-se criar um usuário através da rota "***/user/signup***" ou logar atraves do rota "***/user/login***" (caso já tenha sido criado o usuário). Por fim, a API retorna um token de acesso.
### Requisições do tipo "GET":
São permitidas independente do login de usuário.
