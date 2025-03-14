from pydantic import BaseModel, Field, conint, constr
from typing import List, Annotated


class LearningJourneyInput(BaseModel):
    level: Annotated[str, constr(max_length=300)] = Field(
        ...,
        description="User's English level ",
        example="User's English level  (  A1, A2, B1, B2, C1, C2).",
    )
    duration: Annotated[
        int, Field(..., description="Duration of the study plan in months", example="3")
    ]
    days_week: Annotated[
        int,
        Field(
            ...,
            description="Number of days per week dedicated to studying.",
            example="5",
        ),
    ]
    hour_day: Annotated[
        int,
        Field(..., description="Number of hours dedicated per day.", example="2 hours"),
    ]

    def to_dict(self) -> dict:
        """Converte o modelo para um dicionário"""
        return self.model_dump()
