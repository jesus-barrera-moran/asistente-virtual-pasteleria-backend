# Usa una imagen base de Python 3.12
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Exponer el puerto donde corre la aplicación
EXPOSE 8000

# Comando para iniciar la aplicación usando Uvicorn
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]

# FROM python:3.11-slim

# RUN pip install poetry==1.6.1

# RUN poetry config virtualenvs.create false

# WORKDIR /code

# COPY ./pyproject.toml ./README.md ./poetry.lock* ./

# COPY ./package[s] ./packages

# RUN poetry install  --no-interaction --no-ansi --no-root

# COPY ./app ./app

# RUN poetry install --no-interaction --no-ansi

# EXPOSE 8080

# CMD exec uvicorn app.server:app --host 0.0.0.0 --port 8080
