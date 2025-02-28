from crewai import Agent, Task, Crew, LLM, Process
from crewai.tools import BaseTool, tool
import fitz  # PyMuPDF
import sys
#------------------------------+ Importação da API
gemini = LLM(

    model="gemini/gemini-1.5-flash",
    temperature=0.1,
    api_key="AIzaSyClgsetCnFXfE52bbCZMOqgo7A62uu7P5U"

)
#------------------------------+

# Função para extrair o texto de um PDF
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

# Função que será chamada para extrair texto de múltiplos PDFs fornecidos via terminal
@tool("Extrator de textos de arquivos PDF")
def extrator(question: str) -> str:
    """
    Função que usa a ferramenta para receber arquivos em formato PDF e transformá-los em textos manipuláveis.
    Os caminhos dos arquivos PDF serão recebidos como argumentos do terminal.
    """

    pdf_paths = sys.argv[1:]
    
    if not pdf_paths:
        return "Nenhum arquivo PDF foi fornecido."
    
    extracted_text = ""
    
    # Iterando sobre os caminhos dos PDFs e extraindo o texto
    for pdf_path in pdf_paths:
        try:
            extracted_text += f"Texto extraído do arquivo {pdf_path}:\n"
            extracted_text += extract_text_from_pdf(pdf_path)
            extracted_text += "\n\n"  # Adiciona uma linha em branco entre os textos dos PDFs
        except Exception as e:
            extracted_text += f"Erro ao processar o arquivo {pdf_path}: {str(e)}\n"
    
    return extracted_text
#------------------------------+ Declaração de agentes

processador_de_texto = Agent(
    role="Especialista em extrair textos com base em arquivos PDF",
    goal="Extrair textos de arquivos PDF com fidelidade ao documento original",
    backstory="""
    Você é um especialista em extração de texto de arquivos PDF. Seu trabalho é garantir que o conteúdo do arquivo seja transcrito de maneira fiel, respeitando tanto o texto quanto a formatação e estrutura do documento original.
    Seu objetivo é fornecer um recurso útil para outros agentes, transformando PDFs em dados pesquisáveis e acessíveis.
    """,
    llm=gemini
)

analista_textual = Agent(
    role="Leitor de textos",
    goal="Ler os textos extraídos e identificar o tema e palavras-chave relevantes",
    backstory="""
     Você é um agente especializado em ler os textos extraídos e identificar os temas principais e as palavras-chave mais relevantes. 
    Seu trabalho é focado em extrair de maneira objetiva as informações que serão usadas para criar resumos ou análises mais profundas em etapas subsequentes.
    """,
    llm=gemini
)

sintetizador = Agent(
    role="Sintetizador de conteúdo a partir de textos extraídos de PDFs",
    goal="""Criar resumos concisos e estruturados em tópicos com base no texto extraído dos arquivos PDF,
      considerando as informações sobre o tema e palavras-chave fornecidas pelo agente de análise. 
      O resumo deve ser preciso, mantendo os pontos principais e a integridade do conteúdo original.
        """,
    backstory="""Você está colaborando com uma equipe de agentes que extraem o conteúdo dos PDFs e 
    identificam os temas e palavras-chave dos documentos. 
    Sua tarefa é transformar essas informações em resumos claros, objetivos e bem organizados, 
    que ajudem os autores a entender rapidamente os pontos mais importantes dos textos, 
    sem perder informações essenciais.""",
    llm=gemini
)

formatador_blog=Agent(
    role="Escritor de blogs com base em textos e resumos previamente recebidos",
    goal="""Formatar o conteúdo do resumo fornecido pelo agente sintetizador em um estilo de blog. 
    O objetivo é criar um post coeso e bem estruturado, com título relevante, subtítulos, e tópicos organizados de maneira clara e envolvente. 
    O conteúdo deve ser fiel aos textos originais extraídos dos PDFs, preservando as informações essenciais, 
    e deve ser apresentado de forma que o leitor do blog consiga entender rapidamente os pontos mais importantes do documento.
    """,
    backstory="""Você faz parte de uma equipe que extrai informações de PDFs, identifica temas e palavras-chave, 
    e sintetiza essas informações em resumos. Sua tarefa é transformar esses resumos em um formato de blog, 
    tilizando uma estrutura organizada e clara. O blog deve ter um título relevante, subtítulos para facilitar a leitura, 
    e um texto bem formatado e coeso, sem perder as informações essenciais do conteúdo original.""",
    llm=gemini
)
#----------------------------------------+ Declaração de tarefas

extrair_texto = Task(
    description="Extraia o texto do arquivo PDF dado",
    expected_output = "Um texto igual ao original, sem alterações, extraído do arquivo PDF",
    agent=processador_de_texto,
    tools=[extrator]
)

le_texto= Task(
    description="Ler o texto extraído do PDF e identificar o tema e palavras-chave",
    expected_output="Uma boa descrição do tema do texto e palavras-chave importantes para um bom resumo sobre o assunto",
    agent= analista_textual,
    context=[extrair_texto],
)

sintetiza_texto= Task(
    description="Resuma o texto original com base no tema recebido do agente que analisa o texto",
    expected_output="Um resumo coeso contendo informações baseadas no texto original, que sejam capazes de informar uma pessoa sobre o tema em questão",
    agent=sintetizador,
    context=[extrair_texto, le_texto]

)

formata_blog=Task(
    description="Recebe o texto da tarefa anterior e formata o texto como um blog",
    expected_output="Um blog com título relevante, subtítulos que organizem o conteúdo e conteúdo que seja fiel ao texto original, mas sem a necessidade de falar que o texto é a fonte das informações. Mesmo assim, todo o conteúdo do blog deve ser estritamente referenciado pelo conteúdo dos textos extraídos",
    agent=formatador_blog,
    context=[sintetiza_texto]
)
#----------------------------------------+ Formação do Crew

crew = Crew(
    agents=[processador_de_texto, analista_textual,sintetizador,formatador_blog],
    tasks=[extrair_texto, le_texto,sintetiza_texto,formata_blog],
    process=Process.sequential,
    verbose=True
)

#----------------------------------------+
crew.kickoff()

