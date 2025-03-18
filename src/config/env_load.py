from dotenv import load_dotenv
import os


class EnvLoad:
    def __init__(self, env_file: str = "../.env"):
        """
        Inicializa a classe e carrega as variáveis do arquivo .env em um dicionário.
        """
        load_dotenv(env_file)
        self.variables = {"open_api_key": os.getenv("OPENAI_API_KEY"), "youtube_api_key": os.getenv("YOUTUBE_API_KEY")}

    def get_variables(self):
        """
        Retorna todas as variáveis carregadas.
        """
        return self.variables
