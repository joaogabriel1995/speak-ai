import json
import json
import aio_pika
from services.classrom_service import ClassRoomService
from config.rabbitmq import RabbitMQ
from langchain.output_parsers import PydanticOutputParser
from schemas.classroom_schema import ClassRoomInput

rabbitmq = RabbitMQ()


async def classroom_consumer(message: aio_pika.IncomingMessage):
    """
    Processa as mensagens da fila 'agent-plan-study' para gerar um plano de estudos.
    """
    async with message.process():
        raw_body = message.body
        body_str = raw_body.decode()
        data = json.loads(body_str)
        class_room_service = ClassRoomService(rabbitmq)
        output_parser = PydanticOutputParser(pydantic_object=ClassRoomInput)

        await class_room_service.execute(data)
