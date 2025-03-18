from dataclasses import dataclass, asdict
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from prompts.weekly_activity_prompt import weekly_activity_prompt
from schemas.wekly_plan_detail_schema import (
    WeeklyStudyPlanDetail,
    WeeklyActivityChainInput,
)
from typing import List


class WeeklyLearningDetailChain:
    def __init__(self, api_key):
        """
        Inicializa a WeeklyActivityChain com o prompt e o LLM configurados.
        """
        self.prompt = weekly_activity_prompt()
        self.llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
        self.output_parser = PydanticOutputParser(pydantic_object=WeeklyStudyPlanDetail)
        self.format_instructions = self.output_parser.get_format_instructions()

    def execute(self, input_data: WeeklyActivityChainInput) -> WeeklyStudyPlanDetail:
        """
        Executa o chain para gerar o plano diário de estudos para uma semana,
        retornando a resposta parseada em JSON.

        :param input_data: instância de WeeklyActivityChainInput contendo
            week_objective, activities, theory, days_week, hour_day e level.
        :return: dicionário JSON com o plano diário (daily_plan).
        """
        # Convert Pydantic model to dictionary
        input_dict = input_data.model_dump()
        input_dict["format_instructions"] = self.format_instructions

        # Debugging: Print the prompt template and input dictionary

        # Create the chain
        chain = self.prompt | self.llm

        # Invoke the chain with the dictionary, not the Pydantic model
        response = chain.invoke(input_dict)

        # Parse the response
        output_json = self.output_parser.parse(response.content)
        return output_json
