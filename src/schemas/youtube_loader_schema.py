from pydantic import BaseModel, Field
from typing import List


# Definindo os esquemas Pydantic para a transcrição
class TranscriptionSchema(BaseModel):
    text: str = Field(..., description="O texto do trecho da transcrição.")
    start: float = Field(
        ..., description="O tempo de início do trecho em segundos."
    )  # Corrigido para float
    duration: float = Field(..., description="A duração do trecho em segundos.")


class TranscriptionListSchema(BaseModel):
    page_content: List[TranscriptionSchema]
