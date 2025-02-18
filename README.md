## Visão Geral

Este projeto é o back-end da prova de recrutamento da Athenas. Ele foi desenvolvido utilizando **Django** e **Django REST Framework** e tem como objetivo gerenciar a entidade **Pessoa**.  
O sistema implementa as operações de **CRUD** (incluir, pesquisar, alterar e excluir) e, como ponto extra, calcula o peso ideal de uma pessoa com base na fórmula:

- Para homens: (72,7 * altura) - 58
- Para mulheres: (62,1 * altura) - 44,7

## Estrutura do Projeto

A estrutura principal do projeto é a seguinte:

```
athenas_project/
├── athenas/               # Configurações principais do Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py           # Configuração de URLs do projeto
│   ├── wsgi.py
│   └── settings/         # Configurações divididas por ambiente
│       ├── __init__.py
│       ├── base.py       # Configurações comuns a todos os ambientes
│       ├── development.py# Configurações para desenvolvimento
│       └── production.py # Configurações para produção
├── pessoa/                # App responsável pela entidade Pessoa
│   ├── admin.py
│   ├── apps.py
│   ├── models.py         # Modelo Pessoa e lógica de negócio (inclui cálculo do peso ideal)
│   ├── serializers.py    # Serializadores para conversão entre objetos e JSON
│   ├── tasks.py          # Camada de acesso ao banco de dados (CRUD)
│   ├── services.py       # Camada de serviço que orquestra a lógica de negócio
│   ├── tests.py          # Testes unitários e de integração para a app
│   └── views.py          # API Views para operações CRUD e cálculo do peso ideal
├── Dockerfile             # Instruções para construir a imagem Docker do Django
├── docker-compose.yml     # Orquestração dos containers: web (Django) e db (PostgreSQL)
├── manage.py              # Script de gerenciamento do Django
├── requirements.txt       # Dependências Python do projeto
└── README.md              # Documentação deste projeto
```

## Instalação e Configuração

### Pré-requisitos

- **Python 3.12** (ou versão compatível)
- **PostgreSQL** (ou utilizar o SQLite para desenvolvimento)
- **Docker** e **Docker Compose** (opcional, mas recomendado para consistência dos ambientes)
- **Virtualenv** (recomendado para isolar dependências)

### Configuração Local (Sem Docker)

1. **Clone o Repositório:**

   ```bash
   git clone <URL_DO_SEU_REPOSITORIO>
   cd athenas_project
   ```

2. **Crie e Ative o Ambiente Virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate    # No Windows: venv\Scripts\activate
   ```

3. **Instale as Dependências:**

   Certifique-se de que o arquivo `requirements.txt` esteja presente e contenha, por exemplo:

   ```
   Django==5.1.6
   djangorestframework==3.14.0
   django-cors-headers==3.13.0
   python-decouple==3.8
   psycopg2-binary==2.9.6
   ```

   Execute:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configuração de Variáveis de Ambiente:**

   Crie um arquivo `.env` na raiz (ou defina as variáveis de ambiente no seu sistema). Exemplo para desenvolvimento:

   ```ini
   SECRET_KEY=super-secreta-chave-dev
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost

   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=athenas-dev
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. **Defina o Ambiente de Desenvolvimento:**

   Execute:

   ```bash
   export DJANGO_SETTINGS_MODULE=settings.development
   ```

6. **Realize as Migrações e Inicie o Servidor:**

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

   A aplicação ficará disponível em [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Configuração com Docker

1. **Dockerfile:**

   Verifique que seu Dockerfile (na raiz do projeto) está configurado para instalar as dependências e expor a porta 8000. Exemplo:

   ```dockerfile
   FROM python:3.12-slim
   WORKDIR /app
   RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
   COPY requirements.txt /app/
   RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
   COPY . /app/
   ENV DJANGO_SETTINGS_MODULE=settings.development
   EXPOSE 8000
   CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
   ```

2. **docker-compose.yml:**

   Utilize o arquivo `docker-compose.yml` para orquestrar os containers do Django (web) e do PostgreSQL (db):

   ```yaml
   version: '3.8'

   services:
     web:
       build: .
       container_name: athenas_web
       command: sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
       volumes:
         - .:/app
       ports:
         - "8000:8000"
       environment:
         - DJANGO_SETTINGS_MODULE=settings.development
         - SECRET_KEY=super-secreta-chave-dev
         - DEBUG=True
         - ALLOWED_HOSTS=127.0.0.1,localhost
         - DB_ENGINE=django.db.backends.postgresql
         - DB_NAME=athenas-dev
         - DB_USER=postgres
         - DB_PASSWORD=postgres
         - DB_HOST=db
         - DB_PORT=5432
       depends_on:
         - db

     db:
       image: postgres:14
       container_name: athenas_db
       restart: always
       environment:
         POSTGRES_DB: athenas-dev
         POSTGRES_USER: postgres
         POSTGRES_PASSWORD: postgres
       volumes:
         - postgres_data:/var/lib/postgresql/data

   volumes:
     postgres_data:
   ```

3. **Construir e Iniciar:**

   Na raiz do projeto, execute:

   ```bash
   docker-compose up --build
   ```

   A aplicação ficará disponível em [http://localhost:8000](http://localhost:8000).

## Testes

### Testes do Django

- **Localmente:**

  ```bash
  python manage.py test
  ```

- **Dentro do Docker:**

  ```bash
  docker-compose exec web python manage.py test
  ```

### Testes do Angular (se aplicável)

Caso o front-end esteja configurado e dockerizado, você pode rodar os testes com:

```bash
ng test
```

Esse comando iniciará o test runner (por exemplo, Karma) e exibirá os resultados.

## Documentação do Código

### Back-end

- **Views:**  
  As views foram desenvolvidas utilizando APIViews do Django REST Framework e delegam a lógica de negócio para os serviços. Cada view possui docstrings explicando suas funções.

- **Serializers:**  
  Os serializers convertem os dados dos modelos em JSON e realizam validações. Eles garantem que os dados recebidos estão no formato esperado.

- **Services e Tasks:**  
  A camada de Service orquestra as chamadas para a camada Task, que contém a implementação efetiva das operações CRUD. Essa separação facilita a manutenção e os testes unitários.

- **Testes:**  
  Foram implementados testes unitários para as views, serviços e tarefas, garantindo que as operações do sistema funcionem conforme esperado.

## Decisões Técnicas

- **Separação de Camadas:**  
  O uso de Views, Serializers, Services e Tasks permite isolar a lógica de negócio e simplificar a manutenção e testes.

- **Docker e Variáveis de Ambiente:**  
  A aplicação utiliza Docker para garantir consistência entre ambientes. As configurações sensíveis e específicas de cada ambiente são gerenciadas por variáveis de ambiente, facilitando a implantação e melhorando a segurança.

- **Banco de Dados:**  
  Para o ambiente de desenvolvimento, é utilizado o banco PostgreSQL com o nome `athenas-dev`, enquanto em produção espera-se utilizar `athenas-prod` (configurado via variáveis de ambiente).

- **Testes:**  
  Foram escritos testes para assegurar a qualidade e integridade do código.

## Instruções Rápidas

- **Rodar o Projeto Localmente:**

  ```bash
  export DJANGO_SETTINGS_MODULE=settings.development
  python manage.py runserver
  ```

- **Rodar o Projeto com Docker:**

  ```bash
  docker-compose up --build
  ```

- **Executar Testes:**

  - **Django (Local):**

    ```bash
    python manage.py test
    ```

  - **Django (Docker):**

    ```bash
    docker-compose exec web python manage.py test
    ```
# athenas-backend
