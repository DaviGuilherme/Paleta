# Use uma imagem base do Python
FROM python

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instale as dependências
RUN pip install -r requirements.txt

# Copie todos os arquivos do diretório atual para o contêiner
COPY . .

# Comando para executar o aplicativo quando o contêiner for iniciado
CMD ["python", "server.py"]
