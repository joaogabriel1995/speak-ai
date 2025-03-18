import json
import json
import aio_pika
from services.learning_hub_service import LearningHubService
from config.rabbitmq import RabbitMQ
from langchain.output_parsers import PydanticOutputParser
from schemas.classroom_schema import ClassRoomInput

rabbitmq = RabbitMQ()


async def learning_hub_consumer(message: aio_pika.IncomingMessage):

    async with message.process():
        raw_body = message.body
        body_str = raw_body.decode()
        data = json.loads(body_str)
        learning_detail_setting = LearningHubService(rabbitmq)
        # output_parser = PydanticOutputParser(pydantic_object=ClassRoomInput)
        print(data)
        await learning_detail_setting.execute(
            objective=data.get("objective"),
            activities=data.get("activities"),
            theory=data.get("theory"),
            days_week=data.get("daysWeek"),
            hour_day=data.get("hourDay"),
            level=data.get("level"),
            user_id=data.get("userId"),
        )
