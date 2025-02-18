# Dockerfile
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema necessárias para psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requirements para o container
COPY requirements.txt /app/

# Instala as dependências Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação para o container
COPY . /app/

# Define a variável de ambiente para o Django (ajuste conforme necessário)
ENV DJANGO_SETTINGS_MODULE=settings.development

# Expõe a porta que o Django usará
EXPOSE 8000

# Comando para executar as migrações e iniciar o servidor
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
