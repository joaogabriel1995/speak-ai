from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from schemas.week_plan_schema import LearningJourneyOutPut, WeekPlan
from prompts.learning_journey_prompt import learning_journey_prompt
from schemas.learning_journey_schema import LearningJourneyInput
from typing import List


class LearningJourneyChain:
    def __init__(self, api_key):
        self.prompt = learning_journey_prompt()
        self.llm = ChatOpenAI(
            model="gpt-4o",
            api_key=api_key)
        self.output_parser = PydanticOutputParser(pydantic_object=LearningJourneyOutPut)
        self.format_instructions = self.output_parser.get_format_instructions()

    def execute(self, input_data: LearningJourneyInput) -> List[WeekPlan]:
        """
        Executa o chain com base nos dados de entrada e retorna a resposta parseada em JSON.

        :param input_data: Instância de LearningJourneyInput com os parâmetros 'level', 'duration', 'days_week', 'hour_day'.
        :return: Dicionário JSON com o plano estruturado.
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

