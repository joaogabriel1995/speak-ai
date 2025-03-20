from pydantic import BaseModel, Field, conint, constr, ConfigDict
from typing import List, Literal, Annotated, Optional, Union
from schemas.listening_tool_schema import ListeningToolOutput


# Modelo para uma única atividade do dia
class DailyActivity(BaseModel):
    task: Annotated[str, constr(max_length=50)] = Field(
        ..., description="A specific, actionable task to be performed (max 50 words)."
    )
    resource: str = Field(
        ...,
        description="The specific resource or tool to be used (e.g., 'ESL Pod podcast', 'Anki app').",
    )
    skill: Literal[
        "LISTENING",
        "SPEAKING",
        "VOCABULARY",
        "PRONUNCIATION",
        "GRAMMAR",
        "WRITING",
        "READING",
    ] = Field(..., description="The primary skill being practiced by the task.")
    duration: Annotated[int, conint(ge=1)] = Field(
        ..., description="The estimated time for the task in minutes (min: 1)."
    )
    repetitions: Annotated[int, conint(ge=1)] = Field(
        ...,
        description="The number of times the task should be repeated during the session (min: 1).",
    )


class DailyActivityWithContent(DailyActivity):
    content: Optional[Union[ListeningToolOutput, str]] = Field(
        None, description="Generated content for the activity."
    )


# Modelo para um dia do plano de estudo
class DailyPlan(BaseModel):
    day: Annotated[int, conint(ge=1)] = Field(
        ...,
        description="The day of the week within the study schedule (1 to {days_week}).",
    )
    activities: List[DailyActivity] = Field(
        ...,
        min_items=1,
        description="Array of activity objects representing specific tasks for the day.",
    )
    total_duration: Annotated[int, conint(ge=1)] = Field(
        ...,
        description="The total duration of all activities in the day, in minutes. Must equal {hour_day} * 60.",
    )


# Modelo para um dia do plano de estudo
class DailyPlanWithContent(BaseModel):
    day: Annotated[int, conint(ge=1)] = Field(
        ...,
        description="The day of the week within the study schedule (1 to {days_week}).",
    )
    activities: List[DailyActivityWithContent] = Field(
        ...,
        min_items=1,
        description="Array of activity objects representing specific tasks for the day.",
    )
    total_duration: Annotated[int, conint(ge=1)] = Field(
        ...,
        description="The total duration of all activities in the day, in minutes. Must equal {hour_day} * 60.",
    )

# Modelo para o plano diário completo
class WeeklyStudyPlanDetail(BaseModel):
    weekly_plan: List[DailyPlan] = Field(
        ...,
        description="An array of dictionaries where each entry represents a day's study plan.",
    )

    def to_dict(self) -> dict:
        """Converts the model to a dictionary."""
        return self.model_dump()

    def to_json(self) -> str:
        """Converts the model to a JSON string."""
        return self.model_dump_json(indent=2)


class WeeklyStudyPlanDetailWithContent(BaseModel):
    weekly_plan: List[DailyPlanWithContent] = Field(
        ...,
        description="An array of dictionaries where each entry represents a day's study plan.",
    )
    user_id: Optional[str] = Field(
        None, description="The unique identifier of the user associated with this study plan.",
    )
    learning_journey_id: Optional[str] = Field(
        None, description="The unique identifier of the learning journey associated with this study plan.")

    def to_dict(self) -> dict:
        """Converts the model to a dictionary."""
        return self.model_dump()

    def to_json(self) -> str:
        """Converts the model to a JSON string."""
        return self.model_dump_json(indent=2)


class WeeklyActivityChainInput(BaseModel):
    objective: str = Field(..., description="Objective of the week's study activities.")
    activities: str = Field(..., description="Activities planned for the week.")
    theory: str = Field(
        ..., description="Theoretical concepts covered during the week."
    )
    days_week: Annotated[int, conint(ge=1)] = Field(
        ..., description="Number of study days per week (1 to 7)."
    )
    hour_day: Annotated[int, conint(ge=1)] = Field(
        ..., description="Number of study hours per day (minimum 1)."
    )
    level: str = Field(
        ..., description="User's English level  (  A1, A2, B1, B2, C1, C2)."
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

