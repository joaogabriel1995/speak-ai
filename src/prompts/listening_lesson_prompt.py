from langchain.prompts import PromptTemplate
from textwrap import dedent
from langchain.output_parsers import PydanticOutputParser
from schemas.week_plan_schema import WeekPlan  # Importando o esquema ajustado


def listening_exercise_prompt() -> PromptTemplate:
    """
    Expected parameters:
        - level: User's current English level (e.g., 'beginner', 'intermediate', 'advanced').
        - task: str
        - duration: int
        - transcription: Document
    """
    # output_parser = PydanticOutputParser(pydantic_object=WeekPlan)
    # format_instructions = output_parser.get_format_instructions()

    template = dedent(
        """\
                
        Objetivo: Criar uma aula interativa de inglês com base na transcrição e no vídeo fornecidos, adaptada para o nível {level} do aluno.

        Estrutura da Aula
        Introdução
        
        tarefa: {task}
        Duração da atividade: {duration}

        📍 Instruções para a IA:

        Analise o vídeo e a transcrição fornecidos.

        Identifique o tema central da aula.
        Extraia vocabulário essencial e expressões-chave.
        Estruture o conteúdo de maneira lógica e progressiva.
        Crie uma aula interativa dividida nas seguintes seções:

        📖 Estrutura da Aula
        1. Introdução
        Breve explicação do tema abordado no vídeo.
        Objetivos da aula (por exemplo, aprender como pedir café em inglês).
        Material necessário para a aula (áudio, vídeo, imagens de apoio).
        2. Atividade de Escuta (Listening)
        Primeira escuta: O aluno ouve o áudio/vídeo sem a transcrição e responde a perguntas gerais.
        Segunda escuta: O aluno lê a transcrição enquanto escuta, identificando palavras e expressões-chave.
        3. Vocabulário Essencial e Expressões Comuns
        Liste palavras importantes extraídas do vídeo e suas traduções.
        Inclua expressões informais e comuns no contexto (exemplo: Can I get…? ou I’d like…).
        Adicione frases de exemplo para cada termo, incentivando a aplicação no dia a dia.
        4. Atividade de Pronúncia (Speaking & Shadowing)
        Selecione frases do vídeo para que os alunos ouçam e repitam, focando na entonação e no ritmo natural.
        Sugira a gravação da própria voz para comparação.
        5. Prática de Conversação (Speaking Practice)
        Crie um diálogo simulado baseado no tema do vídeo.
        Exemplo: se o tema for pedir café, inclua interações comuns entre cliente e atendente.
        Sugira perguntas e respostas para reforçar o aprendizado.
        6. Atividade de Escrita (Writing)
        Peça ao aluno para escrever um pequeno parágrafo ou diálogo usando as palavras e expressões aprendidas.
        Exemplo: Escreva um diálogo entre você e um atendente em uma cafeteria.
        7. Revisão e Fixação
        Resumo dos pontos principais da aula.
        Reforço do vocabulário aprendido.
        Sugestões de práticas reais (como tentar pedir um café em inglês na próxima oportunidade).
        💡 Personalização da Aula
        Se o nível do aluno for iniciante: Use frases curtas e estruturas simples.
        Se for intermediário: Introduza conectores e variações nas frases.
        Se for avançado: Inclua expressões idiomáticas e variações de linguagem natural.
        📌 Formato esperado da resposta:
        A IA deve fornecer o conteúdo estruturado como um documento de aula, pronto para ser utilizado, incluindo exemplos práticos e atividades interativas.

        Crie a aula a da transcrição fornecida do video 
        Segue abaixo a transcrição: 
        {transcription}

    """
    )
    listening_lesson_prompt = PromptTemplate(
        input_variables=["level", "task", "duration", "transcription"],
        # partial_variables={"format_instructions": format_instructions},
        template=template,
    )
    return listening_lesson_prompt
