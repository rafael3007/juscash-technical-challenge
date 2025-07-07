# Case | Vaga Analista de Machine Learning com foco em IA - JusCash

Este repositório contém a resolução do case para a vaga de Analista de Machine Learning com foco em IA na JusCash, feito por Rafael Brito.

## 1. Contextualização

O desafio consiste em construir um chatbot para prever o sucesso de novos projetos. A solução deve utilizar um modelo de Machine Learning treinado com dados históricos de projetos anteriores para fornecer previsões e recomendações úteis. O chatbot deverá interagir com o usuário (gerente de projeto ou membro da equipe), combinar os dados fornecidos com informações de uma base de usuários e, a partir disso, utilizar o modelo de ML para gerar as previsões.

## 2. Objetivo

Construir uma aplicação composta por três partes principais:
**Modelo de Machine Learning Tradicional** - Treinar um modelo em Python para prever o sucesso de projetos.
**Deploy do Modelo:** - Disponibilizar o modelo treinado através de uma API simplificada.
**Chatbot Interativo:** - Criar um chatbot que interaja com o usuário, colete dados, consulte uma base de usuários e forneça previsões personalizadas utilizando a API do modelo.

## 3. Componentes do Projeto

### 3.1. Treinamento de Modelo de ML Tradicional

* **Tecnologia:** O modelo deve ser implementado em Python, utilizando bibliotecas como `scikit-learn` ou `XGBoost`.
* **Objetivo do Modelo:** Prever o sucesso ou fracasso de um projeto (classificação).
* **Dados de Entrada (Features):** Duração do projeto, orçamento, número de membros da equipe, recursos disponíveis, entre outras variáveis relevantes.

### 3.2. Deploy do Modelo

* **Tecnologia:** Criar uma API simples em Python utilizando `Flask` ou `FastAPI`.
* **Funcionalidade:** A API deve receber os dados de um novo projeto e retornar a previsão do modelo, como a probabilidade de sucesso.

### 3.3. Chatbot para Interação

* **Interação:** O chatbot deve fazer perguntas ao usuário para coletar dados sobre um novo projeto.
* **Coleta de Dados Adicionais:** Deve acessar uma base de dados de usuários para obter informações contextuais, como histórico e experiência do usuário.
* **Previsão Personalizada:** Combinar os dados do chat com os dados do usuário para consultar o modelo via API e fornecer respostas personalizadas, como: "Com base nos dados fornecidos e no seu histórico de projetos, o seu projeto tem 75% de chance de ser bem-sucedido."

## 4. Base de Dados Sugerida

O case sugere o uso de datasets públicos (como os do Kaggle) ou a criação de uma base de dados própria em formato CSV, JSON, etc.

* **Base de Dados de Projetos:** Para o treinamento do modelo.
* **Estrutura Exemplo:** `Projeto_ID`, `Duração (meses)`, `Orçamento (R$)`, `Tamanho da Equipe`, `Recursos Disponíveis`, `Sucesso (1=sim, 0=não)`
* **Base de Dados de Usuários:** Para ser acessada pelo chatbot.
* **Estrutura Exemplo:** `Usuario_ID`, `Nome`, `Cargo`, `Histórico de Projetos`, `Experiência (anos)`, `Sucesso Médio (percentual)`

## 5. Restrições

* O relatório do chatbot deve ser conciso e direto.
* O treinamento do modelo de ML deve ser simples e eficiente.
* O deploy da API deve ser simples, porém funcional.
* O chatbot precisa ser interativo e de fácil utilização.

## 6. Entregáveis

  **Modelo de ML Tradicional:** Código do treinamento e validação do modelo.
  **API de Deploy:** Código da API que expõe o modelo.
  **Chatbot Funcional:** Implementação do chatbot interativo.
  **Documentação:** Explicação da abordagem, escolhas técnicas, processo de treinamento e implementação.

## 7. Critérios de Avaliação

* **Capacidade Técnica:** Qualidade e organização do código e eficácia da implementação do modelo e da API.
* **Desempenho do Modelo:** Acurácia, precisão, recall e F1-score.
* **Funcionalidade do Chatbot:** Integração com a API e a base de usuários, e personalização das respostas.
* **Explicabilidade:** Justificativas claras para as escolhas técnicas.
* **Inovação e Criatividade:** Soluções inovadoras e personalizações que demonstrem habilidades adicionais.

## 8. Submissão

* **Formato:** Repositório no GitHub.
* **Estrutura:** Duas pastas: uma para o código do modelo de ML (com README) e outra para o código do chatbot.
* **Prazo:** 7 dias corridos.

## Minha Abordagem

Para resolver o desafio, o projeto foi estruturado em dois componentes principais e desacoplados: um **serviço de Machine Learning** responsável pela análise preditiva e uma **assistente de IA conversacional** que serve como interface para o usuário.

O **modelo de Machine Learning**, desenvolvido na pasta `modelo_ml`, utiliza um `Pipeline` do Scikit-learn. Esta abordagem garante que o pré-processamento dos dados (como tratamento de valores ausentes e codificação de variáveis) seja aplicado de forma consistente tanto no treinamento quanto na inferência. O script de treinamento (`modelo_ml/src/index.py`) avalia dois algoritmos (Regressão Logística e Random Forest), selecionando o de melhor performance com base na métrica F1-Score. O pipeline treinado é então serializado e salvo como um artefato (`.joblib`).

Este artefato é consumido por uma **API REST**, construída com **FastAPI**. A API expõe um endpoint (`/v2/prever`) que recebe os dados de um novo projeto em formato JSON, realiza a predição e retorna a probabilidade de sucesso. O uso de Pydantic para validação dos dados de entrada torna a API robusta e segura.

A interface do usuário é a **Assistente JIA**, desenvolvida na pasta `chatbot`. Em vez de um chatbot de FAQ genérico, optei por criar uma assistente focada na tarefa, que funciona como uma **máquina de estados**. Ela guia o usuário através de um fluxo conversacional para coletar os dados necessários para a análise. As tecnologias-chave aqui são:

* **Streamlit**: Para a criação rápida da interface de chat.

* **LangChain e Google Gemini**: Para orquestrar a conversa. Através de uma engenharia de prompt cuidadosa, o modelo de linguagem generativa (LLM) é instruído a extrair informações específicas da fala do usuário e a formatá-las como um JSON estruturado.

O fluxo completo se dá da seguinte forma:

1. O usuário interage com a interface da JIA (Streamlit).

2. A JIA identifica o usuário consultando o arquivo `users.csv`.

3. A JIA conversa com o usuário para obter os detalhes do projeto, usando o Gemini para interpretar as respostas.

4. Com todos os dados em mãos, a aplicação Streamlit faz uma requisição HTTP para a API FastAPI.

5. A API utiliza o modelo de ML para processar os dados e retorna a predição.

6. A JIA recebe o resultado e, novamente com o auxílio do Gemini, apresenta a análise ao usuário de forma clara e humanizada.

Adicionalmente, explorei uma abordagem alternativa usando **n8n e Docker**, criando um chatbot simples para demonstrar versatilidade e conhecimento em plataformas low-code de automação, tendo em vista que o case pede um entregavel em json, não dando mais detalhes sobre a construção do chatbot, mas posso inferir que pelo formato de entrega era esperado a criação de um chatbot em alguma plataforma low-code.

### Tecnologias Utilizadas

* **Linguagem:** Python 3.9 ou maior

* **Modelo de ML:** Scikit-learn, Pandas, NumPy, Joblib

* **API:** FastAPI, Uvicorn

* **Chatbot (Assistente JIA):** Streamlit, LangChain, Google Generative AI (Gemini), Python-Dotenv, Requests

* **Exploração Alternativa:** n8n, Docker, Docker-Compose, Redis

### Como Executar o Projeto

Para executar a demonstração completa, você precisará de dois terminais rodando simultaneamente: um para a API do modelo e outro para o chatbot.

**Pré-requisitos:**

* Python 3.8 ou superior e `pip`.

* Git para clonar o repositório.

#### Passo 1: Clonar o Repositório

```bash

    git clone https://github.com/rafael3007/juscash-technical-challenge.git
    cd juscash-technical-challenge

```

#### Passo 2: Executar a API do Modelo de ML

1. Abra o **primeiro terminal**.

2. Navegue até a pasta do modelo, crie um ambiente virtual e instale as dependências:

    ```bash
    
        cd modelo_ml
        python -m venv venv
        
        # No Linux:
        source venv/bin/activate  
        
        # No Windows: 
        venv\Scripts\activate
        
        # Instalação das bibliotecas
        pip install -r requirements.txt
    
    ```

3. Inicie a API com o Uvicorn. O modelo já está treinado e salvo na pasta `artefatos/`.

    ```bash
    
        # No diretório
        uvicorn api:app --reload
    
    ```

4. A API estará rodando em `http://127.0.0.1:8000`. Mantenha este terminal aberto.

#### Passo 3: Executar a Assistente JIA com Streamlit (Web)

1. Abra um **segundo terminal**.

2. Navegue até a pasta do chatbot, crie seu próprio ambiente virtual e instale as dependências:

    ```bash
        
        cd chatbot
        python -m venv venv
        
        # No Linux
        source venv/bin/activate
        
        # No Windows: 
        venv\Scripts\activate
        
        pip install -r requirements.txt
        
    ```

3. Configure sua chave de API do Google Gemini. Crie um arquivo chamado `.env` dentro da pasta `chatbot`:

    ```.env

        # chatbot/.env
        GOOGLE_API_KEY="SUA_CHAVE_API_DO_GEMINI_AQUI"
    
    ```

4. Inicie a aplicação Streamlit:

    ```bash
    
    streamlit run chatbot_v5.py
    
    ```

5. Uma aba abrirá em seu navegador com a interface do chatbot, pronta para interagir.

#### Passo 4: Executar o chatbot com n8n

Se desejar testar a abordagem alternativa de chatbot

1. **Pré-requisitos**: Docker e Docker Compose instalados.

2. No terminal, dentro da pasta `chatbot`, execute: `docker-compose up -d`.

3. Acesse a interface do n8n em `http://localhost:5678` e verifique se está funcionando.
