from chains.classroom_chain import ClassRoomChain
from schemas.classroom_schema import ClassRoomInput
from config.env_load import EnvLoad


class ClassRoomService:

    def __init__(self, broker):
        self.rabbitmq = broker
        env = EnvLoad()
        self.config = env.get_variables()

    async def execute(self, weeklyStudyPlanDetail: ClassRoomInput):
        class_room_chain = ClassRoomChain(self.config.get("open_api_key"))
        result = await class_room_chain.execute(weeklyStudyPlanDetail)

        return result
