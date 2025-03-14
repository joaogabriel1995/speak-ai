import json
import json
import aio_pika
from services.generate_journey_service import GenerateLearningJourneyService
from config.rabbitmq import RabbitMQ

rabbitmq = RabbitMQ()


async def learning_journey_consumer(message: aio_pika.IncomingMessage):
    """
    Processa as mensagens da fila 'agent-plan-study' para gerar um plano de estudos.
    """
    async with message.process():
        raw_body = message.body
        body_str = raw_body.decode()
        data = json.loads(body_str)

        learning_journey = GenerateLearningJourneyService(rabbitmq)
        await learning_journey.execute(
            level=data.get("level"),
            duration=data.get("duration"),
            days_week=data.get("days_week"),
            hour_day=data.get("hour_day"),
            userId=data.get("userId"),
        )
