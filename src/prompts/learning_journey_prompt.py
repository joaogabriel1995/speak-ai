from langchain.prompts import PromptTemplate
from textwrap import dedent
from langchain.output_parsers import PydanticOutputParser
from schemas.week_plan_schema import WeekPlan  # Importando o esquema ajustado


def learning_journey_prompt() -> PromptTemplate:
    """
    Returns a PromptTemplate to generate a comprehensive macro English learning plan,
    incorporating innovative methodologies, the Pareto principle, and detailed theoretical grammar explanations.

    Expected parameters:
        - level: User's current English level (e.g., 'beginner', 'intermediate', 'advanced').
        - duration: Total study duration (e.g., '6 months').
        - days_week: Number of days per week the user plans to study (e.g., 5).
        - hour_day: Number of study hours per day (e.g., 2).
    """
    output_parser = PydanticOutputParser(pydantic_object=WeekPlan)
    format_instructions = output_parser.get_format_instructions()

    template = dedent(
        """\
        Você é um especialista em ensino de inglês com muitos anos de experiência.
        Baseado nas metodologias práticas de Chris Lonsdale, Luca Lampariello, English with Lucy e Rachel's English,
        sua tarefa é criar um plano de aprendizado de inglês macro abrangente para {duration}, 
        que servirá como um guia inicial para detalhamento posterior.
        Estou no nível {level} de inglês e quero aprender em {duration}, estudando {days_week} dias por semana, 
        {hour_day} horas por dia.

        O plano deve seguir rigorosamente estas diretrizes:

        ### Estrutura Geral
        - Divida o período de {duration} em meses, com 4 semanas por mês. Por exemplo, se a duração for "6 months", 
        o plano deve conter 24 semanas (6 meses x 4 semanas).
        - Gere um array plano de objetos, onde cada objeto representa uma semana e contém os campos:
            - "objective": Um texto curto com o objetivo da semana (máximo 50 palavras).
            - "activity": Uma atividade prática claramente definida (máximo 50 palavras).
            - "theory": Uma explicação concisa de tópicos gramaticais essenciais (máximo 50 palavras).
            - "week": Número da semana (1 a 4 dentro de cada mês).
            - "month": Número do mês (1 ao total de meses).
        - Cada semana deve ser única, com objetivos, atividades e teorias que evoluem e se complementam, 
        evitando repetições ou generalizações.

        ### Detalhamento dos Campos
        1. **Objetivo ("objective")**:
            - Deve ser SMART (específico, mensurável, alcançável, relevante e com prazo definido).
            - Deve descrever claramente o que o aprendiz será capaz de fazer ao final da semana, 
            incluindo um indicador de desempenho mensurável. Por exemplo:
                - Para iniciantes: "Produzir 5 frases completas no presente simples com 90% de precisão."
                - Para intermediários: "Compreender 80% de um diálogo informal de 2 minutos com expressões como 'gonna' e 'wanna'."
                - Para avançados: "Escrever um e-mail informal de 150 palavras usando 5 expressões idiomáticas com 95% de precisão gramatical."
            - Evite objetivos vagos como "Melhorar a pronúncia" ou "Aprender vocabulário". Sempre inclua um resultado mensurável e específico.

        2. **Atividade ("activity")**:
            - Deve ser prática, específica e incluir instruções detalhadas sobre como executá-la.
            - Deve mencionar:
                - Um recurso ou ferramenta específica (por exemplo, o nome de um podcast, vídeo ou site).
                - O tempo estimado para conclusão (considerando {days_week} dias por semana e {hour_day} horas por dia).
                - Um entregável mensurável (por exemplo, "escrever 10 frases", "gravar um áudio de 1 minuto").
            - Deve incluir pelo menos um recurso gratuito e acessível, como:
                - Podcasts (por exemplo, "ESL Pod", "BBC Learning English").
                - Vídeos (por exemplo, "English with Lucy no YouTube", "Rachel's English no YouTube").
                - Sites (por exemplo, "BBC Learning English", "ESL Fast").
            - **Não inclua aplicativos de aprendizado de idiomas como 'Anki' ou 'Duolingo' nas atividades**, 
            pois eles serão tratados em um plano diário detalhado separado.
            - Cada atividade deve integrar pelo menos duas habilidades essenciais (por exemplo, escuta e fala, 
            leitura e escrita), combinando prática ativa (produção) e passiva (compreensão). Por exemplo:
                - "Ouça um diálogo de 2 minutos no 'BBC Learning English', escreva 5 frases resumindo o que ouviu e 
                grave um áudio de 1 minuto respondendo a uma pergunta do diálogo (tempo estimado: 1 hora)."

        3. **Teoria ("theory")**:
            - Deve ser uma explicação concisa de tópicos gramaticais essenciais (máximo 50 palavras), incluindo:
                - Tempos verbais: presente simples, presente contínuo, passado simples, passado contínuo e formas de futuro.
                - Pontos gramaticais essenciais: uso de "to be", verbos modais básicos, estruturas comparativas, auxiliares comuns.
                - Pronomes, estrutura de frases e exemplos contextuais.
            - Deve incluir pelo menos um exemplo prático contextualizado (por exemplo, "I eat breakfast every day" para o presente simples).
            - A teoria deve estar diretamente relacionada ao objetivo e à atividade da semana, reforçando a aplicação prática dos conceitos. Por exemplo:
                - Se o objetivo é "Produzir 5 frases no presente simples", a teoria deve explicar o presente simples com exemplos como "She walks to school" 
                e "They don’t eat meat."

        ### Diretrizes Gerais
        - **Princípio de Pareto (80/20)**: Priorize os 20% do conteúdo que geram 80% dos resultados. Concentre-se em:
            - Vocabulário de alta frequência (por exemplo, as 1000 palavras mais comuns).
            - Expressões do dia a dia (por exemplo, "you know", "gonna", "wanna", "ain’t", "like").
            - Pronúncia essencial (por exemplo, vogais curtas vs. longas, som do "th").
            - Estruturas gramaticais básicas (por exemplo, presente simples, "to be").
        - **Habilidades Essenciais**: Cada semana deve abordar pelo menos duas habilidades (escuta, fala, leitura, 
        escrita, vocabulário, pronúncia), 
        com atividades que combinem prática ativa e passiva.
        - **Comunicação Real**: Enfatize a comunicação prática, expressões do dia a dia e fala informal. 
        Inclua expressões informais e gírias comuns (por exemplo, "ain’t", "gonna", "wanna", "you know", "like") em pelo menos 50% das atividades e exemplos teóricos, 
        garantindo que o aprendiz possa usá-las em contextos reais, como conversas casuais ou e-mails informais.
        - **Progressão Lógica**: O plano deve seguir uma progressão lógica, com cada semana construindo sobre o conhecimento e 
        habilidades adquiridas nas semanas anteriores. Cada mês deve consolidar uma área principal de aprendizado, por exemplo:
            - Mês 1: Fundamentos (vocabulário básico, presente simples, "to be").
            - Mês 2: Comunicação básica (perguntas e respostas, passado simples).
            - Mês 3: Comunicação intermediária (expressões informais, futuro).
            - Inclua semanas de revisão a cada 4 ou 8 semanas, onde o objetivo é consolidar o conhecimento adquirido, com atividades 
            como testes simulados, revisões de vocabulário e prática integrada de todas as habilidades.
        - **Adaptação ao Nível**: Adapte todos os objetivos, atividades e explicações teóricas ao nível do aprendiz ({level}). Por exemplo:
            - **Iniciantes**: Foco em estruturas simples (presente simples, "to be") e vocabulário básico (saudações, números, objetos do dia a dia).
            - **Intermediários**: Introduza expressões idiomáticas, tempos verbais mais complexos (passado contínuo, futuro) e vocabulário mais amplo.
            - **Avançados**: Enfatize fluência, nuances culturais e expressões idiomáticas complexas.

        ### Exemplos Detalhados
        Para garantir que o plano seja detalhado e específico, siga os exemplos abaixo para cada nível:

        **Exemplo para Iniciantes (Nível Beginner) – Semana 1, Mês 1**:
        ```json
        {{
            "objective": "Produzir 5 frases completas no presente simples com 90% de precisão.",
            "activity": "Ouça o podcast 'ESL Pod – Daily Life' (episódio sobre rotinas diárias, 10 minutos), escreva 5 frases sobre sua rotina usando o presente simples e grave um áudio de 1 minuto lendo suas frases (tempo estimado: 1 hora).",
            "theory": "Presente simples: usado para hábitos e fatos. Estrutura: sujeito + verbo (add -s para he/she/it). Exemplo: 'I eat breakfast every day.' Negativas: 'don’t/doesn’t + verbo'.",
            "week": 1,
            "month": 1
        }}```      
        **Exemplo para Iniciantes (Nível Intermediate) – Semana 1, Mês 1**:
            ```json
        {{
            "objective": "Compreender 80% de um diálogo informal de 2 minutos com expressões como 'gonna' e 'wanna'.",
            "activity": "Assista ao vídeo 'English with Lucy – Informal English' no YouTube (seção sobre 'gonna' e 'wanna', 10 minutos), escreva 5 frases usando essas expressões e grave um áudio de 1 minuto respondendo a uma pergunta do vídeo (tempo estimado: 1,5 horas).",
            "theory": "Futuro com 'going to' (informal: 'gonna') para planos. Exemplo: 'I’m gonna watch a movie.' 'Want to' (informal: 'wanna') para desejos. Exemplo: 'I wanna learn English.'",
            "week": 1,
            "month": 2
        }}``` 
        Exemplo para Avançados (Nível Advanced) – Semana 1, Mês 3:
                      
        ```json
        {{
            "objective": "Escrever um e-mail informal de 150 palavras usando 5 expressões idiomáticas com 95% de precisão gramatical.",
            "activity": "Leia o artigo 'BBC Learning English – Idioms in Use' (seção sobre expressões casuais, 15 minutos), escreva um e-mail informal para um amigo fictício usando 5 expressões idiomáticas e grave um áudio de 1 minuto explicando suas escolhas (tempo estimado: 2 horas).",
            "theory": "Expressões idiomáticas: frases com significados não literais. Exemplo: 'Piece of cake' (fácil). Uso em contextos informais: 'Writing emails is a piece of cake for me.'",
            "week": 1,
            "month": 3
        }}
        ```
        Responda em formato JSON com a propriedade "plan" contendo o array de objetos.
        Certifique-se de que cada objeto no array siga rigorosamente o esquema fornecido, com campos preenchidos de forma específica, mensurável e prática, como nos exemplos acima.
        {format_instructions}
        """
    )
    plan_prompt = PromptTemplate(
        input_variables=["level", "duration", "days_week", "hour_day"],
        partial_variables={"format_instructions": format_instructions},
        template=template,
    )
    return plan_prompt
