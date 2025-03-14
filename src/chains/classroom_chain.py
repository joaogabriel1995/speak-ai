from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from prompts.weekly_activity_prompt import weekly_activity_prompt
from schemas.classroom_schema import ClassRoomInput
from tools.listening_tool import ListeningChain
from config.env_load import EnvLoad
import json


class ClassRoomChain:
    def __init__(self, api_key):

        self.prompt = weekly_activity_prompt()
        self.llm = ChatOpenAI(
            model="gpt-4o",
            api_key=api_key)
        self.output_parser = PydanticOutputParser(pydantic_object=ClassRoomInput)
        self.format_instructions = self.output_parser.get_format_instructions()
        self.llm_with_tool = self.llm.bind_tools([self.listening])

    async def execute(self, input_data: ClassRoomInput):
        self.output_parser = PydanticOutputParser(pydantic_object=ClassRoomInput)
        self.output = self.output_parser.parse(json.dumps(input_data))
        for day in self.output.daily_plan:
            for activitie in day.activities:

                if activitie.skill == "listening":
                    await self.listening(
                        activitie.task,
                        activitie.resource,
                        activitie.duration,
                        self.output.level,
                    )

                if activitie.skill == "speaking":
                    pass

                if activitie.skill == "vocabulary":
                    pass

                if activitie.skill == "pronunciation":
                    pass

                if activitie.skill == "grammar":
                    pass

                if activitie.skill == "writing":
                    pass

                if activitie.skill == "reading":
                    pass

    async def listening(self, task: str, resource: str, duration: int, level: str):
        """Ferramenta utilizada para criar o listening"""
        listeningChain = ListeningChain()
        await listeningChain.execute(task, resource, duration, level)
        # self.llm.invoke()
