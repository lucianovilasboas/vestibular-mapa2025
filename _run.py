import schedule
import subprocess
import time
from log import logger

# Função para executar os scripts
def executar():
    print("Executando automacao.py...")
    logger.info("Executando automacao.py...")
    subprocess.run(["python", "automacao.py"], shell=True)
    logger.info("Execução finalizada.")

    print("Executando processa.py...")
    logger.info("Executando processa.py...")
    subprocess.run(["python", "processa.py"], shell=True)
    logger.info("Execução finalizada.")

    print("Executando gitrun.py...")
    logger.info("Executando gitrun.py...")
    subprocess.run(["python", "gitrun.py", "-m", "Data update using git"], shell=True)
    logger.info("Execução finalizada.")


if __name__ == "__main__":
    logger.info("Iniciando execução...")
    executar()
    logger.info("Execução finalizada.")
