from schemas.wekly_plan_detail_schema import WeeklyActivityChainInput
from chains.weekly_learning_detail_chain import WeeklyLearningDetailChain
from config.env_load import EnvLoad 


class GenerateLearningDetailService:

    def __init__(self, broker):
        self.rabbitmq = broker
        env = EnvLoad()
        self.config = env.get_variables()

    async def execute(
        self,
        objective: str,
        activities: str,
        theory: str,
        days_week: str,  #
        hour_day: str,
        level: str,
    ):
        weekly_activity_chain_input = WeeklyActivityChainInput(
            objective=objective,
            activities=activities,
            theory=theory,
            days_week=days_week,
            hour_day=hour_day,
            level=level,
            
        )
        weekly_detail_chain = WeeklyLearningDetailChain(self.config.open_api_key)
        result = weekly_detail_chain.execute(weekly_activity_chain_input,self.config.open_api_key)
        return result
