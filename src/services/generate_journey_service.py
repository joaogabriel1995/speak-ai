from schemas.learning_journey_schema import LearningJourneyInput
from chains.learning_journey_chain import LearningJourneyChain
from config.env_load import EnvLoad 


class GenerateLearningJourneyService:

    def __init__(self, broker):
        self.rabbitmq = broker
        env = EnvLoad()
        self.config = env.get_variables()

    async def execute(
        self, level: str, duration: str, days_week: str, hour_day: str, userId: str
    ):
        learning_journey_input = LearningJourneyInput(
            level=level, duration=duration, days_week=days_week, hour_day=hour_day
        )
        learningJourneyChain = LearningJourneyChain(self.config.open_api_key)
        result = learningJourneyChain.execute(learning_journey_input)
        print("result result result result", result)

        plan = [
            {
                "objective": week.objective,
                "activity": week.activity,
                "theory": week.theory,
                "week": week.week,
                "month": week.month,
            }
            for week in result.plan
        ]
        data = {
            "plan": plan,
            "userId": userId,
            "settings": {
                "level": level,
                "duration": int(duration),
                "daysWeek": int(days_week),
                "hourDay": int(hour_day),
            },
        }
        await self.rabbitmq.publish("learning_plan_response", data)
        return result
