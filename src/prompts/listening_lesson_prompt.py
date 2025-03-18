from langchain.prompts import PromptTemplate
from textwrap import dedent
from langchain.output_parsers import PydanticOutputParser
from schemas.week_plan_schema import WeekPlan  # Importando o esquema ajustado

from schemas.listening_tool_schema import (
    ListeningToolOutput,
)  # Importando o esquema ajustado


def listening_exercise_prompt() -> PromptTemplate:
    """
    Expected parameters:
        - level: User's current English level (e.g., 'beginner', 'intermediate', 'advanced').
        - task: str
        - duration: int
        - transcription: Document
    """
    output_parser = PydanticOutputParser(pydantic_object=ListeningToolOutput)
    format_instructions = output_parser.get_format_instructions()

    template = dedent(
        """\
    📚 **Aula Interativa de Inglês**

    🎯 **Tema da Aula:** {task}

    **Duração:** {duration}
    **Nível:** {level}

    📖 **Estrutura da Aula**

    ## 📝 **Introdução**
    - **Tema da aula:** Identifique o tema principal com base no vídeo.
    - **Objetivos:** Defina objetivos específicos adaptados ao nível do aluno.
    - **Materiais Necessários:** áudio, transcrição e materiais adicionais para suporte.

    ## 🎧 **Atividade de Escuta (Listening)**

    ### Primeira Escuta:
    Ouça o áudio sem ler a transcrição.
    Responda:
    1. Qual é o assunto central discutido?
    2. Quem são as pessoas envolvidas?
    3. O que está sendo solicitado ou negociado?

    ## 🔎 **Segunda Escuta - Detalhes e Vocabulário**
    - **Escute novamente acompanhando a transcrição abaixo.**
    - Identifique palavras e expressões importantes usadas no diálogo:
      - Liste ao menos 5 palavras-chave ou expressões importantes do áudio.
      - Exemplo: expressões comuns, frases úteis e vocabulário essencial.

    ## 🎙️ **Atividade de Pronúncia (Shadowing)**
    - Identifique e liste pelo menos duas frases do vídeo/transcrição para o aluno praticar a pronúncia.
    - Instrua o aluno a ouvir o áudio e repetir as frases, tentando copiar a entonação e ritmo.

    ## 💬 **Prática de Conversação**
    - Desenvolva um diálogo simples e interativo relacionado ao tema do vídeo.
    - Inclua perguntas e respostas práticas para o aluno treinar interação oral.

    ## ✏️ **Atividade de Escrita**
    - Proponha uma atividade curta de escrita baseada no tema, usando o vocabulário identificado.
    - Exemplo: Crie um breve diálogo ou email utilizando as novas palavras e expressões.

    ## ✅ **Revisão e Dicas Finais**
    - Faça um resumo curto dos principais pontos aprendidos na aula.
    - Dê uma dica prática de como usar o vocabulário aprendido na vida real.

    📍 **Personalização da Aula**
    - **Iniciante:** Utilize frases simples e repetições.
    - **Intermediário:** Incentive o uso de conectores e diferentes tempos verbais.
    - **Avançado:** Estimule a inclusão de expressões idiomáticas e frases mais complexas.
    
    ## 📜 **Transcrição Fornecida**
    {transcription} 
    
    {format_instructions}

    """
    )
    listening_lesson_prompt = PromptTemplate(
        input_variables=["level", "task", "duration", "transcription"],
        partial_variables={"format_instructions": format_instructions},
        template=template,
    )
    return listening_lesson_prompt
