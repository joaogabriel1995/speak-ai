from pydantic import BaseModel, Field, constr, ConfigDict
from typing import List, Annotated
from .wekly_plan_detail_schema import DailyPlan


# Modelo para o plano diário completo
class ClassRoomInput(BaseModel):
    weekly_plan: List[DailyPlan] = Field(
        ...,
        description="An array of dictionaries where each entry represents a day's study plan.",
    )
    level: Annotated[str, constr(max_length=300)] = Field(
        ...,
        description="Level of student.",
        example="User's English level  (  A1, A2, B1, B2, C1, C2).",
    )

    def to_dict(self) -> dict:
        """Converts the model to a dictionary."""
        return self.model_dump()

    def to_json(self) -> str:
        """Converts the model to a JSON string."""
        return self.model_dump_json(indent=2)

    model_config = ConfigDict(
        alias_generator=lambda x: ''.join(
            word.capitalize() if i else word for i, word in enumerate(x.split("_"))
        ),
        populate_by_name=True
    )
