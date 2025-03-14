from typing import Annotated
from pydantic import BaseModel, Field, conint, constr
from langchain.tools import StructuredTool
from langchain_community.tools import YouTubeSearchTool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from tools.youtube_transcript_tool import YoutubeLoaderTool
import os
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

        self.llm = ChatOpenAI(
            model="gpt-4o",
            api_key=api_key,
            temperature=0,  # Para respostas mais determinísticas
        )

        # Inicializa a ferramenta do YouTube
        self.youtube_tool = YouTubeSearchTool()
        # Cria a ferramenta de listening
        self.listening_tool = StructuredTool(
            name="listening_tool",
            func=self.listening,
            description="Ferramenta para criar planos de estudo de listening baseados em recursos gerais, exceto vídeos e podcasts.",
            args_schema=ListeningInput,
        )

        # Vincula ferramentas ao LLM
        self.tools = [self.listening_tool, self.youtube_tool]
        self.llm_with_tool = self.llm.bind_tools(self.tools)

    async def execute(self, task: str, resource: str, duration: int, level: str):
        """
        Executa a tarefa de listening.
        O LLM decide qual ferramenta usar com base no recurso (YouTube para vídeos, listening_tool para outros casos).
        """
        prompt = self.generate_prompt(task, resource, duration)

        messages = [HumanMessage(content=prompt)]

        response = self.llm_with_tool.invoke(messages)
        messages.append(response)

        if response.tool_calls:
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                # Executar a ferramenta correspondente
                if tool_name == "listening_tool":
                    result = self.listening_tool.invoke(tool_args)
                elif (
                    tool_name == "youtube_search"
                ):  # Nome correto da ferramenta do YouTube
                    result = self.youtube_tool.invoke(
                        task
                    )  # Usa a tarefa como consulta
                    youtube = YoutubeLoaderTool()
                    array_data = ast.literal_eval(result)

                    transcription = await youtube.get_tool().invoke(
                        {"youtube_url": array_data[0], "language": ["en"]}
                    )
                    prompt = listening_exercise_prompt()
                    print(
                        prompt.format(
                            **{
                                "task": task,
                                "duration": duration,
                                "level": level,
                                "transcription": transcription,
                            }
                        )
                    )
                    chain = listening_exercise_prompt() | self.llm
                    response = chain.invoke(
                        {
                            "task": task,
                            "duration": duration,
                            "level": level,
                            "transcription": transcription,
                        }
                    )
                    print("response", response)
                else:
                    continue

                print(f"✅ Resultado da ferramenta `{tool_name}`: {result}")
                return result  # Retorna o resultado da primeira ferramenta chamada (pode ser ajustado)

        else:
            return (
                response.content
            )  # Retorna a resposta direta do LLM se não houver chamadas de ferramentas

    def generate_prompt(self, task: str, resource: str, duration: int) -> str:
        """
        Gera um prompt adequado para a LLM com base nos parâmetros fornecidos.
        """
        prompt = (
            f"Crie um plano de estudo para listening com duração de {duration} minutos.\n"
            f"Tarefa: {task}\n"
            f"Recurso: {resource}\n"
            f"Instruções:\n"
            f"- Se o recurso for 'YouTube' ou contiver 'podcast' (exemplo: 'ESL Pod podcast'), use a ferramenta 'YouTubeSearchTool' para buscar vídeos ou podcasts relevantes.\n"
            f"- Para todos os outros recursos, use a ferramenta 'listening_tool' para criar um plano de estudo.\n"
            f"Retorne apenas a chamada da ferramenta apropriada com os argumentos corretos, sem explicações adicionais."
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
