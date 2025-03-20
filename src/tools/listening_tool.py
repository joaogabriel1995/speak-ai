from typing import Annotated
from pydantic import BaseModel, Field, conint, constr
from langchain.tools import StructuredTool

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from tools.youtube_transcript_tool import YoutubeLoaderTool
import os
import json
from langchain_community.document_loaders import GoogleApiYoutubeLoader, GoogleApiClient
from langchain.output_parsers import PydanticOutputParser
from .youtube_search_tool import YoutubeSearchTool, YoutubeSearchToolInput


from schemas.listening_tool_schema import ListeningToolOutput
from prompts.listening_lesson_prompt import listening_exercise_prompt
from dotenv import load_dotenv
import ast

# Carregar variáveis de ambiente
load_dotenv(dotenv_path=".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Schema para os parâmetros da task de listening
class ListeningInput(BaseModel):
    task: Annotated[str, constr(max_length=50)] = Field(
        ..., description="A specific, actionable task to be performed."
    )
    resource: str = Field(
        ...,
        description="The specific resource or tool to be used (e.g., 'ESL Pod podcast', 'YouTube').",
    )
    duration: Annotated[int, conint(ge=1)] = Field(
        ..., description="The estimated time for the task in minutes (min: 1)."
    )


class ListeningChain:
    def __init__(self, api_key):
        """
        Inicializa a cadeia de listening com um modelo de linguagem (LLM) e ferramentas para buscar vídeos e podcasts.
        """

        self.llm = ChatOpenAI(model="gpt-4o",api_key=api_key,temperature=0,  
        )
        self.youtube_tool = YoutubeSearchTool().get_tool()
        self.tools = [self.youtube_tool]
        self.llm_with_tool = self.llm.bind_tools(self.tools)
        self.output_parser = PydanticOutputParser(pydantic_object=ListeningToolOutput)
        self.format_instructions = self.output_parser.get_format_instructions()

    async def execute(self, task: str, resource: str, duration: int, level: str):
        prompt = self.generate_prompt(task, resource, duration, level)
        messages = [HumanMessage(content=prompt)]
        response = self.llm_with_tool.invoke(messages)
        messages.append(response)

        if response.tool_calls:
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                if tool_name == "youtube_search":
                    print("tool_args", tool_args["query"])
                    print(type(tool_args))
                    tool_input = YoutubeSearchToolInput(**tool_args)
                    result = self.youtube_tool.invoke({"query": tool_input.query})
                    print("RESULTADO:", result)
                    if result:  # Verifica se há resultados
                        youtube = YoutubeLoaderTool()
                        transcription = await youtube.get_tool().invoke(
                            {"youtube_url": result[0]['video_id'], "language": ["en"]}
                        )
                        prompt = listening_exercise_prompt()
                        chain = prompt | self.llm
                        response = chain.invoke(
                            {
                                "task": task,
                                "duration": duration,
                                "level": level,
                                "transcription": transcription,
                            }
                        )
                        output_json = self.output_parser.parse(response.content)
                        return output_json
                    else:
                        print("Nenhum vídeo encontrado para a consulta.")
                        return {"error": "Nenhum vídeo encontrado para a consulta fornecida."}
                else:
                    continue
        else:
            return response.content
    def generate_prompt(self, task: str, resource: str, duration: int, level: str) -> str:
        """
        Gera um prompt otimizado para a LLM, garantindo que a busca de vídeos seja altamente relevante para o assunto da aula.
        """
        prompt = (
            f"Crie um plano de estudo para aprimorar a habilidade de listening com duração de {duration} minutos.\n"
            f"Tarefa: {task}\n"
            f"Recurso: {resource}\n"
            f"\n"
            f"Instruções:\n"
            f"- Se o recurso for 'YouTube' ou contiver 'podcast' (exemplo: 'ESL Pod podcast'), use a ferramenta 'YouTubeSearchTool' para buscar vídeos ou podcasts altamente relevantes para a **tarefa** e **nível do aluno**.\n"
            f"- A pesquisa deve conter palavras-chave da **tarefa** para garantir que os vídeos sejam sobre o assunto exato que está sendo estudado.\n"
            f"- Priorize vídeos educativos, explicativos e que ofereçam exercícios práticos sobre o tema.\n"
            f"- Se possível, busque vídeos recentes para garantir que o conteúdo esteja atualizado.\n"
            f"\n"
            f"Formato da resposta:\n"
            f"Retorne **apenas** a chamada da ferramenta apropriada com os argumentos otimizados para pesquisa, sem explicações adicionais."
        )
        return prompt


    def listening(self, task: str, resource: str, duration: int) -> str:
        """
        Executa a tarefa de listening para recursos gerais (não vídeos ou podcasts).
        """
        # Aqui você pode implementar uma lógica mais complexa para gerar um plano de estudo
        return f"Plano de estudo para {task} usando {resource} por {duration} minutos. (Implementação genérica)"

    def get_tools(self) -> list:
        """
        Retorna a lista de ferramentas disponíveis.
        """
        return self.tools
