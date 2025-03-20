from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from prompts.weekly_activity_prompt import weekly_activity_prompt
from schemas.classroom_schema import ClassRoomInput
from schemas.wekly_plan_detail_schema import (
    DailyActivityWithContent,
    DailyPlanWithContent,
    WeeklyStudyPlanDetailWithContent,
)

from tools.listening_tool import ListeningChain
from typing import List

class ClassRoomChain:
    def __init__(self, api_key):

        self.api_key = api_key
        self.prompt = weekly_activity_prompt()
        self.llm = ChatOpenAI(model="gpt-4o", api_key=api_key)
        self.output_parser = PydanticOutputParser(pydantic_object=ClassRoomInput)
        self.format_instructions = self.output_parser.get_format_instructions()
        self.llm_with_tool = self.llm.bind_tools([self.listening])

    async def execute(
        self, input_data: ClassRoomInput
    ) -> WeeklyStudyPlanDetailWithContent:
        # Cria uma lista para armazenar os dias atualizados
        updated_daily_plan:List[DailyPlanWithContent] = []

        # Parseia a entrada usando o output parser configurado
        self.output_parser = PydanticOutputParser(pydantic_object=ClassRoomInput)
        self.output = self.output_parser.parse(input_data.to_json())

        # Itera por cada dia do plano
        for daily in self.output.weekly_plan:
            updated_activities:List[DailyActivityWithContent] = []

            # Processa cada atividade do dia
            for activity in daily.activities:
                if activity.skill == "LISTENING":
                    # Gera o conteúdo utilizando a ferramenta de listening

                    generated_content = await self.listening(
                        activity.task,
                        activity.resource,
                        activity.duration,
                        self.output.level,
                    )

                    # Cria uma cópia da atividade atualizando o campo "content"
                    #  validar se é objetc ou string
                    updated_activity = DailyActivityWithContent(
                        **activity.model_dump(), content=generated_content.model_dump() 
                    )
                    updated_activities.append(updated_activity)

                elif activity.skill == "SPEAKING":
                    # Implementar atualização específica para speaking, se necessário
                    updated_activity = DailyActivityWithContent(
                        **activity.model_dump(), content=None
                    )
                    updated_activities.append(updated_activity)

                elif activity.skill == "VOCABULARY":
                    updated_activity = DailyActivityWithContent(
                        **activity.model_dump(), content=None
                    )
                    updated_activities.append(updated_activity)

                elif activity.skill == "PRONUNCIATION":
                    updated_activity = DailyActivityWithContent(
                        **activity.model_dump(), content=None
                    )
                    updated_activities.append(updated_activity)

                elif activity.skill == "GRAMMAR":
                    updated_activity = DailyActivityWithContent(
                        **activity.model_dump(), content=None
                    )
                    updated_activities.append(updated_activity)

                elif activity.skill == "WRITING":
                    updated_activity = DailyActivityWithContent(
                        **activity.model_dump(), content=None
                    )
                    updated_activities.append(updated_activity)

                elif activity.skill == "READING":
                    updated_activity = DailyActivityWithContent(
                        **activity.model_dump(), content=None
                    )
                    updated_activities.append(updated_activity)

                else:
                    # Caso a atividade não se enquadre nas skills mapeadas, mantém inalterada
                    updated_activity = DailyActivityWithContent(
                        **activity.model_dump(), content=None
                    )
                    updated_activities.append(updated_activity)

            updated_day = DailyPlanWithContent(
                day=daily.day,
                activities=updated_activities,
                total_duration=daily.total_duration,
            )
            updated_daily_plan.append(updated_day)

        # Atualiza o objeto completo com o novo daily_plan
        weekly = WeeklyStudyPlanDetailWithContent(weekly_plan=updated_daily_plan)
        return weekly

    async def listening(self, task: str, resource: str, duration: int, level: str):
        """Ferramenta utilizada para criar o listening"""
        listeningChain = ListeningChain(self.api_key)
        return await listeningChain.execute(task, resource, duration, level)
