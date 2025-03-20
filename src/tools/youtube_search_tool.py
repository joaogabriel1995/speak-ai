

from pydantic import BaseModel, constr, conint, Field
from typing import Optional
from langchain.tools import StructuredTool
from googleapiclient.discovery import build
from config.env_load import EnvLoad

class YoutubeSearchToolInput(BaseModel):
    query: str = Field(..., description="The search query to find YouTube videos.")


    def to_dict(self) -> dict:
        """Converts the model to a dictionary."""
        return self.model_dump()


class YoutubeSearchTool:

    def __init__(self):
        env = EnvLoad()
        self.config = env.get_variables()
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"

        # Criar o cliente da API
        self.youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=self.config.get("youtube_api_key"))

        self.tool = StructuredTool(
            name="youtube_search",
            func=self.search_videos,
            description="Ferramenta utilizada para buscar videos no youtube",
            args_schema=YoutubeSearchToolInput,
        )

    def get_tool(self):
        return self.tool

    def search_videos(self,query: str):
        try:
            # Realizar a pesquisa
            search_response = self.youtube.search().list(
                q=query,  # Consulta de pesquisa
                part="id,snippet",  # Dados a serem retornados (ID e informações básicas)
                type="video",  # Filtrar apenas por vídeos
                maxResults=1,  # Número máximo de resultados
                order="relevance",  # Ordenar por relevância
                videoDuration="medium"  # Filtro de duração
            ).execute()
            print("search_response",search_response)
            # Extrair IDs dos vídeos e informações básicas
            video_results = []
            for item in search_response.get("items", []):
                video_id = item["id"]["videoId"]
                title = item["snippet"]["title"]
                description = item["snippet"]["description"]
                video_results.append({
                    "video_id": video_id,
                    "title": title,
                    "description": description
                })
                print(title)

            return video_results

        except Exception as e:
            print(f"Erro ao buscar vídeos: {e}")
        return []
