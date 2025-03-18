from config.rpc_client import RpcClient
from config.rabbitmq import RabbitMQ
import json

from langchain_community.document_loaders import YoutubeLoader
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled

from langchain_core.documents import Document
from pydantic import BaseModel, constr, conint, Field
from typing import List, Optional
from langchain.tools import StructuredTool


class YoutubeLoaderToolInput(BaseModel):
    youtube_url: str = Field(..., description="Youtube url for tramnscript")
    language: Optional[List[str]] = Field(description="change language for transcript")


class YoutubeLoaderTool:

    def __init__(self):
        self.tool = StructuredTool(
            name="youtube_transcription",
            func=self.load,
            description="Ferramenta para extrair legenda de videos do youtube",
            args_schema=YoutubeLoaderToolInput,
        )

    async def load(self, youtube_url: str, language: list[str] = ["en"]):
        try:
            channel = await RabbitMQ().get_channel()
            rpc_client = RpcClient(channel)
            await rpc_client.setup()
            payload = {"language": "en", "youtube_url": youtube_url}
            response = await rpc_client.call(
                "process_transcription_api", payload, 600000
            )

            responseJson = json.loads(response)
            metadata = {"source": responseJson.get("url")}
            return [
                Document(page_content=str(responseJson.get("text")), metadata=metadata)
            ]
        except Exception as e:
            print("Erro na chamada RPC:", e)

    def get_tool(self):
        return self.tool
