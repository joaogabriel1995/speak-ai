import asyncio
import json
import uuid
from aio_pika import Message, DeliveryMode
from aio_pika.channel import Channel, AbstractQueue
from aio_pika.queue import IncomingMessage


class RpcClient:
    def __init__(self, channel: Channel):
        self.channel = channel
        self.callback_queue: AbstractQueue | None = None
        self.futures = {}

    async def setup(self):
        self.callback_queue = await self.channel.declare_queue(
            "", exclusive=False, auto_delete=True
        )
        await self.callback_queue.consume(self.on_message)

    async def on_message(self, message: IncomingMessage):
        async with message.process():
            correlation_id = message.correlation_id

            if correlation_id in self.futures:
                future = self.futures.pop(correlation_id)
                future.set_result(message.body)

    async def call(self, queue_name: str, payload: dict, timeout: int = 10) -> str:
        correlation_id = str(uuid.uuid4())

        future = asyncio.get_event_loop().create_future()
        self.futures[correlation_id] = future

        try:
            message = Message(
                body=json.dumps(payload).encode(),
                correlation_id=correlation_id,
                reply_to=self.callback_queue.name,
                delivery_mode=DeliveryMode.PERSISTENT,
            )

            await self.channel.default_exchange.publish(message, routing_key=queue_name)

            response_body = await asyncio.wait_for(future, timeout=timeout)
            return response_body.decode()
        except asyncio.TimeoutError:
            if correlation_id in self.futures:
                del self.futures[correlation_id]
            raise Exception("Timeout aguardando resposta RPC")
        except Exception as e:
            if correlation_id in self.futures:
                del self.futures[correlation_id]
            raise Exception(f"Erro ao realizar chamada RPC: {str(e)}")
