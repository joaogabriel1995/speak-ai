import asyncio
import json
import aio_pika
from config.rabbitmq import RabbitMQ
from consumers.learning_journey_consumer import learning_journey_consumer
from consumers.learning_detail_consumer import learning_detail_consumer
from consumers.classroom_consumer import classroom_consumer
from consumers.learning_hub_consumer import learning_hub_consumer


rabbitmq = RabbitMQ()


async def main():
    """
    Função principal que configura a conexão com RabbitMQ,
    assina as filas e aguarda indefinidamente.
    """
    try:
        RabbitMQ.set_url("amqp://guest:guest@localhost:5672")
        await rabbitmq.connection()
        await rabbitmq.create_channel()

        await rabbitmq.subscribe("agent-plan-study", learning_journey_consumer)
        await rabbitmq.subscribe("weekly_plan_queue", learning_detail_consumer)
        await rabbitmq.subscribe("classroom_queue", classroom_consumer)
        await rabbitmq.subscribe("learning_hub", learning_hub_consumer)

        print("entrei")
        # Mantém o loop rodando
        await asyncio.Future()

    except Exception as e:
        print(f"Erro ao processar: {e}")


if __name__ == "__main__":

    asyncio.run(main())
