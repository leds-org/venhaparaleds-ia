O código apresentado é bem simples e seu funcionamento foi pensado para ser intuitivo.

# Funcionamento
Ao iniciar o código pelo terminal, inclua também os caminhos dos pdf's a serem utilizados.
Caso isso não aconteça, uma mensagem de erro será mostrada e os agentes não vão dar prosseguimento em suas tarefas
### Execução de tarefas
A primeira tarefa a ser executada é a extração do texto puro pelo agente 'processador_de_texto', que usa uma ferramenta customizada com a biblioteca PyMuPDF, que transcreve o conteúdo do PDF diretamente para texto pleno. É importante ressaltar que tantos quantos arquivos forem colocados nos argumentos do terminal serão processados em ordem. 

A segunda tarefa é realizada pelo agente 'analista_textual' e consiste em ler o texto extraído e compreender o tema e as palavras-chave. Isso acontece para que o agente que sintetiza os textos consiga captar a mensagem e garantir uma entrega sem esquecer de nenhum dos pontos mais importantes.

A terceira tarefa é justamente a do agente 'sintetizador' e consiste em receber as palavras-chave e o tema do agente anterior, e, em conjunto com o texto inicial extraído dos arquivos, resumir bem os textos separadamente.

A quarta e última tarefa é do agente 'formatador_blog' e consiste em pegar os resumos, complementar com as informações dos textos iniciais e, de maneira fiel às informações contidas nos arquivos originais, separar em tópicos coesos os assuntos.

O exemplo enviado é de um blog sobre o momento do deepseek no mercado global, no terminal foram fornecidos três PDFs sobre esse mesmo tema, e com base nas informações contidas e nos processos descritos acima, recebemos como resultado um texto com um título relevante, subtítulos que ajudam a organizar o conteúdo e um texto coeso no seu conteúdo no geral.
