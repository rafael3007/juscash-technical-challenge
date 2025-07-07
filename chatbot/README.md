# Documentação: Chatbot e Assistente de IA JusCash

Este documento detalha duas implementações de chatbot desenvolvidas, explicando como configurar e executar cada uma, as escolhas técnicas e a arquitetura correta de cada solução.

## 1. Visão Geral

Foram exploradas duas abordagens distintas para o desafio. Fiz essa escolha (de duas abordagens), pois
as instruções pedem um chatbot, porém analisando o case, percebi que o mais adequado seria um assistente virtual. Ainda pelo documento, que pede um json como entregável, portanto acredito que era esperado um chatbot feito com alguma ferramenta low-code e assim escolhi o n8n para isso. Apesar de conseguir desenvolver com o n8n, desenvolvi também um código com python utilizando langchain, sabendo que é uma das stacks para a vaga achei que seria adequado também.

1. **Abordagem Low-Code (n8n)**: Implementação de um chatbot que é capaz de conversar com o usuário, entender sobre o projeto, enviar as informações para API e responder o usuario de acordo com a resposta da API.
2. **Abordagem com Código (Python)**: A aplicação principal, que funciona como uma **Assistente de IA (JIA)**. Seu propósito é **coletar dados de um projeto através de uma conversa**, consultar um arquivo `users.csv` para identificar o gerente do projeto, e orquestrar uma chamada para a API de Machine Learning para realizar uma análise de risco.

## 2. Estrutura de Arquivos

```path
chatbot/
│
├── .env                     # Contém GOOGLE_API_KEY usada na implementação com código python
├── chatbot_v5.py            # Aplicação da assistente JIA com Streamlit e LangChain.
├── docker-compose.yml       # Orquestração dos serviços n8n e Redis para a prova de conceito.
├── requirements.txt         # Dependências Python para a assistente JIA.
├── workflow.json            # Fluxo do chatbot para importação no n8n. Contém o texto do FAQ embutido.
└── README.md                # Esta documentação.

# NOTA: O arquivo 'users.csv' que a assistente JIA utiliza está localizado em ../modelo_ml/data/users.csv, porém para a implementação low-code foi adaptado e inserido no workflow

```

----------

## 3. Abordagem I: Chatbot JIA com n8n

Esta abordagem utiliza o n8n e o Gemini para criar um chatbot simples.

### 3.1. Visão Geral

- **n8n**: Ferramenta de automação low-code que executa um fluxo de trabalho visual.
- **Tools**: Ferramentas que o nó de IA vai utilizar quando entender que for necessário
- **Modelo**: LLM utilizada no nó de IA, no caso do workflow foi utilizado o Gemini
- **HTTP**: Nó que faz requisição HTTP para a API
- **Docker & Redis**: Usados para executar o n8n e para gerenciar a memória (histórico) da conversa.

### 3.2. Configuração e Execução

1. **Pré-requisitos**: Docker e Docker Compose instalados.( há outras formas de executar no n8n, como com o node, por exemplo `npx n8n`, com o node préviamente instalado)
2. **Iniciar Serviços**: No terminal, na pasta `chatbot`, execute `docker-compose up -d`.
3. **Importar Workflow**: Acesse a interface do n8n (`http://localhost:5678`),faça login ou crie um acesso, vá em `Workflows`, `Import from File` e selecione `workflow.json`. Configure as credenciais para os serviços dentro da interface do n8n.
4. **Testar**: Use o chat (visível no nó de mesmo nome no n8n) para enviar perguntas.

----------

## 4. Abordagem II: Assistente JIA com LangChain e Streamlit

Implementação de um assistente de IA que executa tarefas específicas de coleta de dados e análise de projetos.

### 4.1. Visão Geral

A aplicação guia um usuário por um processo de múltiplos estágios para analisar um projeto. Ela **não** é um chatbot de conhecimento geral, tem como objetivo auxiliar no cálculo e predição sobre projetos consumindo a API local. Foi utilizado o langchain com o langchain_google_genai para implementação da lógica do assistente e para interagir com o usuario foi utilizado o Streamlit para criação de uma interface simples.

- **Fluxo de Trabalho**:

    1. **Identificação**: A JIA pergunta o nome do usuário e busca correspondência no arquivo `../modelo_ml/data/users.csv`.

    2. **Coleta de Dados**: Através de uma conversa, a JIA extrai informações estruturadas sobre o projeto (duração, orçamento, complexidade, etc.).

    3. **Análise**: Com os dados coletados, a JIA chama a API do modelo de Machine Learning.

    4. **Apresentação**: A JIA apresenta o resultado da análise (probabilidade de sucesso) ao usuário.

- **Componentes**:

1. **Streamlit**: Constrói a interface web do chat.

2. **LangChain**: Orquestra a lógica da conversa usando `PromptTemplate` e `LLMChain` para guiar o LLM em cada etapa.

3. **Gemini (Google)**: Usado para tarefas de extração de dados, classificação de intenção e geração de respostas em linguagem natural.

4. **Pandas**: Para carregar e consultar o `users.csv`.

### 4.2. Configuração e Execução

1. **Pré-requisitos**: Python 3.8 ou maior e `pip` instalado.

2. **Instalar Dependências**:

    - Crie e ative um ambiente virtual: `python -m venv venv` e `source venv/bin/activate`.

    - Instale as bibliotecas: `pip install -r requirements.txt`.

3. **Configurar a Chave de API**:

    - Crie um arquivo `.env` na pasta `chatbot`.

    - Adicione a chave da API: `GOOGLE_API_KEY="SUA_CHAVE_API_DO_GEMINI_AQUI"`.( Vale ressaltar que a chave da api para o código em questão é para usar o Gemini como Modelo, caso use a openai, ollama ou outra deve ajustar a configuração do serviço e do código)

4. **API de ML**: Garanta que a API do `modelo_ml` esteja em execução (conforme o `modelo_ml\README.md`).

5. **Executar a Aplicação**:

    - No terminal (com ambiente virtual ativado[venv]), execute:

    ```bash

        streamlit run chatbot_v5.py

    ```

    - A interface da assistente JIA abrirá no seu navegador e então só testar/usar

### 4.3. Pontos Importantes do Código (`chatbot_v5.py`)

- **Máquina de Estados (`app_state`)**: O fluxo da aplicação é rigidamente controlado, movendo-se entre os estados `IDENTIFICATION`, `DATA_COLLECTION` e `POST_ANALYSIS`, garantindo o fluxo correto da conversa.

- **Engenharia de Prompt**: O `coleta_prompt_template` instrui o LLM a agir como um extrator de dados que deve retornar um JSON.

- **Desacoplamento de Serviços**: A assistente é totalmente separada da API de ML (backend de predição). A comunicação ocorre via uma chamada de API (`chamar_api_predicao`).

- **Validação de Usuário**: O carregamento inicial do `users.csv` serve como uma etapa de "autenticação" leve, permitindo que a JIA personalize a interação e utilize os dados históricos do gerente de projeto na análise.
