# Generamos una imagen de Python. En este caso la última.
FROM python:latest

# Configuración del directorio de ejecución.
WORKDIR /app

# Copia del archivo requirements.txt para la imagen creada.
COPY requirements.txt .

# Dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia de los archivos .py necesarios para la ejecución del entorno.
COPY gen2.py .

# Comando de inicio del contenedor
CMD ["python", "gen2.py"]



