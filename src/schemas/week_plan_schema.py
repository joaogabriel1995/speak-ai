from pydantic import BaseModel, Field, conint, constr
from typing import List, Annotated


class WeekPlan(BaseModel):
    objective: Annotated[str, constr(max_length=300)] = Field(
        ...,
        description="Objective of the week (max 300 words).",
        example="Produce 5 complete sentences in simple present with 90% accuracy.",
    )
    activity: Annotated[str, constr(max_length=300)] = Field(
        ...,
        description="A practical activity (max 300 words).",
        example="Listen to 'ESL Pod – Daily Life', write 5 sentences, record a 1-minute audio.",
    )
    theory: Annotated[str, constr(max_length=300)] = Field(
        ...,
        description="A concise explanation of key English grammar topics (max 50 words).",
        example="Simple present: habits/facts. Structure: subject + verb (+s for he/she/it). Ex: 'I eat.'",
    )
    week: Annotated[int, conint(ge=1, le=4)] = Field(
        ..., description="Week number (1 to 4).", example=1
    )
    month: Annotated[int, conint(ge=1)] = Field(
        ..., description="Month number (1 to duration in months).", example=1
    )

    class Config:
        extra = "forbid"


class LearningJourneyOutPut(BaseModel):
    plan: List[WeekPlan] = Field(
        ...,
        description="An array of dictionaries where each entry represents a week with an objective, activity, theory, week number, and month.",
    )
