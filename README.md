# django-workshop

## Sobre

Este projeto é um esboço da implementação de gerenciamento de projetos utilizado no ambiente empresarial da Asa Branca Distribuidora. Tem operações iniciais de Criação, Leitura e Deleção de projetos. Este projeto foi desenvolvido durante o workshop de Django feito internamente.

## Configuração do ambiente

- Instalação do Python (Versão 3.8.4) - [Python 3.8.4](https://www.python.org/downloads/release/python-384/)
- Instalar virtualenv - `pip install virtualenv`
- Criar ambiente virtual para dependências - `virtualenv venv` 
  - `venv` é o nome dado ao ambiente virtual, que fica a seu critério
- Ativação do ambiente virtual - `.\venv\Scripts\activate`
- Instalar as dependências do arquivo [requirements](./requirements.txt) - `pip install -r "requirements.txt"`, localizado na pasta raiz do projeto
- OBS: este projeto foi feito utilizando uma versão de desenvolvedor do Banco de dados SQL Server, e necessita de uma instância instalada localmente ou uma url para uma instâmcia em nuvem para baixar, instalar e rodar este projeto sem alterá-lo

## Comandos para inicialização do projeto

```bash

# Cria migrations sem aplicá-las
$ python manage.py makemigrations

# Executa migrations
$ python manage.py migrate

# Coleta arquivos estáticos
$ python manage.py collectstatic

# Cria super usuário
$ python manage.py createsuperuser

# Inicializar o servidor
$ python manage.py runserver

```

## Rotas

```bash

# Listagem de todos os projetos cadastrados
$ /projects

# Importação de projetos a partir de um arquivo csv
$ /projects

# Criação de projeto
$ /projects/project

# Listar ou deletar um projeto
$ /projects/project/1
  No exemplo acima, o número 1 é o id do projeto a ser listado ou deletado

```