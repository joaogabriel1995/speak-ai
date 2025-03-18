from .generate_daily_plain_service import GenerateLearningDetailService
from .classrom_service import ClassRoomChain
from config.env_load import EnvLoad
from schemas.classroom_schema import ClassRoomInput
from schemas.wekly_plan_detail_schema import WeeklyStudyPlanDetailWithContent

from config.rabbitmq import RabbitMQ

class LearningHubService:
    def __init__(self, rabbit: RabbitMQ):
        env = EnvLoad()
        self.config = env.get_variables()
        self.rabbit: RabbitMQ = rabbit
        self.classroom_service = ClassRoomChain(self.config.get("open_api_key"))
        self.generate_learning_detail_service = GenerateLearningDetailService(rabbit)

    async def execute(
        self,
        objective: str,
        activities: str,
        theory: str,
        days_week: int,
        hour_day: int,
        level: str,
        user_id: str,
    ):
        weekly_study_plan_detail = await self.generate_learning_detail_service.execute(
            objective, activities, theory, days_week, hour_day, level
        )
        class_room_input = ClassRoomInput(
            weekly_plan=weekly_study_plan_detail.weekly_plan, level=level
        )

        result = await self.classroom_service.execute(class_room_input)
        weekly = WeeklyStudyPlanDetailWithContent(**result,user_id=user_id)
        weekly_plan_json = weekly.model_dump_json(indent=2)
        await self.rabbit.publish("weekly_detail_plan", weekly_plan_json)
