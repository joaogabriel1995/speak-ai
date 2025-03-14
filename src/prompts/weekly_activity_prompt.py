from langchain.prompts import PromptTemplate
from textwrap import dedent
from langchain.output_parsers import PydanticOutputParser
from schemas.wekly_plan_detail_schema import WeeklyStudyPlanDetail


def weekly_activity_prompt() -> PromptTemplate:
    """
    Retorna um PromptTemplate que gera um plano detalhado de atividades diárias para uma semana de estudos de inglês,
    alinhado ao plano macro gerado anteriormente.

    Parâmetros esperados:
        - objective: Objetivo da semana obtido no plano macro.
        - activities: Atividade geral da semana obtida no plano macro.
        - theory: Teoria da semana obtida no plano macro.
        - days_week: Número de dias que o usuário estuda na semana.
        - hour_day: Número de horas diárias de estudo.
        - level: Nível atual de inglês do usuário (por exemplo, A1, A2, B1, B2, C1, C2).
    """
    output_parser = PydanticOutputParser(pydantic_object=WeeklyStudyPlanDetail)
    format_instructions = output_parser.get_format_instructions()

    template = dedent(
        """\
        Você é um especialista em ensino de inglês com anos de experiência.
        Com base no objetivo semanal abaixo, na atividade geral sugerida e na teoria especificada, você deverá criar um plano detalhado diário para a semana de estudos.

        Informações semanais:
        - Objetivo semanal: {objective}
        - Atividade geral: {activities}
        - Teoria semanal: {theory}

        Nível do aluno: {level}
        Dias de estudo na semana: {days_week}
        Horas diárias de estudo: {hour_day}

        Diretrizes para o plano semanal:
        - O plano deve cobrir exatamente {days_week} dias, com cada dia contendo um conjunto de atividades detalhadas.
        - Mostre uma progressão lógica ao longo da semana: o primeiro dia deve introduzir conceitos básicos, os dias intermediários devem construir sobre o aprendizado anterior, e os últimos dias devem incluir prática mais complexa ou integrada.
        - Cada dia deve ter múltiplas atividades detalhadas (mínimo 2 por dia, máximo 5).
        - A soma das durações das atividades diárias deve sempre totalizar {hour_day} horas (em minutos).

        Diretrizes para cada atividade diária:
        - Cada atividade deve ser específica, prática e com instruções claras para execução.
        - Utilize recursos gratuitos e acessíveis, como podcasts ("ESL Pod"), vídeos ("English with Lucy") ou sites ("BBC Learning English"). Não utilizar aplicativos como Anki ou Duolingo, pois serão tratados separadamente.
        - Para cada recurso mencionado, forneça o título exato e, se possível, um link direto ou instruções claras de como encontrá-lo (por exemplo, "Acesse o vídeo 'Greetings and Introductions' no canal English with Lucy no YouTube: [link]").
        - Cada atividade deve explicitar claramente a habilidade praticada (listening, speaking, vocabulary, pronunciation, grammar, writing ou reading).
        - Cada atividade deve conter uma duração estimada (em minutos) e número de repetições.
        - Inclua exemplos concretos ou modelos nas descrições das atividades, especialmente para escrita e fala (por exemplo, "Escreva 5 frases como: 'My name is [nome]. I am from [cidade].'").
        - Inclua critérios de sucesso ou autoavaliação para cada atividade (por exemplo, "Grave sua leitura e verifique se pronuncia corretamente pelo menos 90% das palavras").
        - Inclua pelo menos uma atividade diária que integre duas habilidades (por exemplo, "Ouça um diálogo e, em seguida, recrie-o em voz alta para praticar listening e speaking").
        - Adapte as atividades ao nível do aluno ({level}). Por exemplo:
            - Nível A1/A2: Use frases curtas, vocabulário básico e atividades guiadas.
            - Nível B1/B2: Inclua textos mais longos, prática de inferência e produção independente.
            - Nível C1/C2: Foque em nuances, vocabulário avançado e prática em contextos reais.
        - Priorize o princípio de Pareto (20% de conteúdo mais efetivo para 80% dos resultados).

        Sempre responder em Português (BR).
        Responda em formato JSON com a propriedade "daily_plan" contendo um array de {days_week} objetos, cada um representando um dia de estudo, conforme instruções abaixo.

        {format_instructions}
    """
    )

    daily_plan_prompt = PromptTemplate(
        input_variables=[
            "objective",
            "activities",
            "theory",
            "days_week",
            "hour_day",
            "level",
            "format_instructions",
        ],
        template=template,
    )

    return daily_plan_prompt
