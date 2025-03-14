import json
import json
import aio_pika
from services.generate_daily_plain_service import GenerateLearningDetailService
from config.rabbitmq import RabbitMQ

rabbitmq = RabbitMQ()


async def learning_detail_consumer(message: aio_pika.IncomingMessage):
    """
    Processa as mensagens da fila 'agent-plan-study' para gerar um plano de estudos.
    """
    async with message.process():
        raw_body = message.body
        body_str = raw_body.decode()
        data = json.loads(body_str)

        learning_detail = GenerateLearningDetailService(rabbitmq)
        await learning_detail.execute(
            objective=data.get("objective"),
            activities=data.get("activities"),
            theory=data.get("theory"),
            days_week=data.get("days_week"),
            hour_day=data.get("hour_day"),
            level=data.get("level"),
        )
