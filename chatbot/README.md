
# Documentação: Chatbot e Assistente de IA JusCash

Este documento detalha as duas implementações de chatbot desenvolvidas, explicando como configurar e executar cada uma, as escolhas técnicas e a arquitetura correta de cada solução.

## 1. Visão Geral

Foram exploradas duas abordagens distintas para o desafio:

1.  **Abordagem Low-Code (n8n)**: Uma prova de conceito que implementa um chatbot de Perguntas Frequentes (FAQ). O conhecimento do chatbot está **embutido diretamente no fluxo de trabalho** do n8n.
    
2.  **Abordagem com Código (Python)**: A aplicação principal, que funciona como uma **Assistente de IA (JIA)**. Seu propósito é **coletar dados de um projeto através de uma conversa**, consultar um arquivo `users.csv` para identificar o gerente do projeto, e orquestrar uma chamada para a API de Machine Learning para realizar uma análise de risco.
    

## 2. Estrutura de Arquivos

```
chatbot/
│
├── .env                     # Contém GOOGLE_API_KEY usada na implementação com código python
│
├── chatbot_v5.py            # Aplicação da assistente JIA com Streamlit e LangChain.
├── docker-compose.yml       # Orquestração dos serviços n8n e Redis para a prova de conceito.
├── requirements.txt         # Dependências Python para a assistente JIA.
├── workflow.json            # Fluxo do chatbot para importação no n8n. Contém o texto do FAQ embutido.
└── README.md                # Esta documentação.

# NOTA: O arquivo 'users.csv' que a assistente JIA utiliza está localizado em ../modelo_ml/data/users.csv, porém para a implementação low-code foi adaptado e inserido no workflow

```

----------

## 3. Abordagem 1: Chatbot JIA com n8n

Esta abordagem utiliza o n8n para criar um chatbot simples.

### 3.1. Visão Geral da Solução

-   **n8n**: Ferramenta de automação que executa um fluxo de trabalho visual.
-   **Tools**
-  **Modelo**
- **HTTP**    
-   **Docker & Redis**: Usados para executar o n8n e para gerenciar a memória (histórico) da conversa.
    

### 3.2. Tutorial de Configuração e Execução

1.  **Pré-requisitos**: Docker e Docker Compose instalados.
    
2.  **Iniciar Serviços**: No terminal, na pasta `chatbot`, execute `docker-compose up -d`.
    
3.  **Importar Workflow**: Acesse a interface do n8n (`http://localhost:5678`), vá em `Workflows`, `Import from File` e selecione `workflow.json`. O fluxo já contém todo o conhecimento necessário. Configure as credenciais para os serviços dentro da interface do n8n.
    
4.  **Testar**: Use o chat (visível no nó de mesmo nome no n8n) para enviar perguntas.
    

----------

## 4. Abordagem II: Assistente JIA com LangChain e Streamlit

Implementação de um assistente de IA que executa uma tarefa específica de coleta de dados e análise de projetos.

### 4.1. Visão Geral da Solução

A aplicação guia um usuário por um processo de múltiplos estágios para analisar um projeto. Ela **não** é um chatbot de conhecimento geral, tem como objetivo auxiliar no cálculo e predição sobre projetos consumindo a API local.

-   **Fluxo de Trabalho**:
    
    1.  **Identificação**: A JIA pergunta o nome do usuário e busca correspondência no arquivo `../modelo_ml/data/users.csv`.
        
    2.  **Coleta de Dados**: Através de uma conversa, a JIA extrai informações estruturadas sobre o projeto (duração, orçamento, complexidade, etc.).
        
    3.  **Análise**: Com os dados coletados, a JIA chama a API do modelo de Machine Learning.
        
    4.  **Apresentação**: A JIA apresenta o resultado da análise (probabilidade de sucesso) ao usuário.
        
-   **Componentes**:
    
    -   **Streamlit**: Constrói a interface web do chat.
        
    -   **LangChain**: Orquestra a lógica da conversa usando `PromptTemplate` e `LLMChain` para guiar o LLM em cada etapa.
        
    -   **Gemini (Google)**: Usado para tarefas de extração de dados, classificação de intenção e geração de respostas em linguagem natural.
        
    -   **Pandas**: Para carregar e consultar o `users.csv`.
        

### 4.2. Tutorial de Configuração e Execução

1.  **Pré-requisitos**: Python 3.8+ e `pip`.
    
2.  **Instalar Dependências**:
    
    -   Crie e ative um ambiente virtual: `python -m venv venv` e `source venv/bin/activate`.
        
    -   Instale as bibliotecas: `pip install -r requirements.txt`.
        
3.  **Configurar a Chave de API**:
    
    -   Crie um arquivo `.env` na pasta `chatbot`.
        
    -   Adicione a linha: `GOOGLE_API_KEY="SUA_CHAVE_API_DO_GEMINI_AQUI"`.
        
4.  **API de ML**: Garanta que a API do `modelo_ml` esteja em execução (conforme o `README.md` daquela pasta).
    
5.  **Executar a Aplicação**:
    
    -   No terminal (com ambiente virtual ativado), execute:
        
        Bash
        
        ```
        
        streamlit run chatbot_v5.py
        
        ```
        
    -   A interface da assistente JIA abrirá no seu navegador.
        

### 4.3. Pontos Importantes do Código (`chatbot_v5.py`)

-   **Máquina de Estados (`app_state`)**: O fluxo da aplicação é rigidamente controlado, movendo-se entre os estados `IDENTIFICATION`, `DATA_COLLECTION` e `POST_ANALYSIS`, o que garante que a conversa siga o caminho correto.
    
-   **Engenharia de Prompt Focada**: O `coleta_prompt_template` é a peça chave. Ele instrui o LLM a agir como um extrator de dados que deve retornar um JSON, uma técnica muito mais robusta do que simplesmente esperar uma resposta em texto.
    
-   **Desacoplamento de Serviços**: A assistente (frontend e lógica de conversação) é totalmente separada da API de ML (backend de predição). A comunicação ocorre via uma chamada de API (`chamar_api_predicao`), o que é uma excelente prática de arquitetura de software.
    
-   **Validação de Usuário**: O carregamento inicial do `users.csv` serve como uma etapa de "autenticação" leve, permitindo que a JIA personalize a interação e utilize os dados históricos do gerente de projeto na análise.
