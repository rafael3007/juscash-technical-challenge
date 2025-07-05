# Case | Vaga Analista de Machine Learning com foco em IA - JusCash

Este repositório contém a resolução do case para a vaga de Analista de Machine Learning com foco em IA na JusCash.

## 1. Contextualização

O desafio consiste em construir um chatbot para prever o sucesso de novos projetos. A solução deve utilizar um modelo de Machine Learning treinado com dados históricos de projetos anteriores para fornecer previsões e recomendações úteis. O chatbot deverá interagir com o usuário (gerente de projeto ou membro da equipe), combinar os dados fornecidos com informações de uma base de usuários e, a partir disso, utilizar o modelo de ML para gerar as previsões.

## 2. Objetivo

Construir uma aplicação composta por três partes principais:
**Modelo de Machine Learning Tradicional:** Treinar um modelo em Python para prever o sucesso de projetos.
**Deploy do Modelo:** Disponibilizar o modelo treinado através de uma API simplificada.
**Chatbot Interativo:** Criar um chatbot que interaja com o usuário, colete dados, consulte uma base de usuários e forneça previsões personalizadas utilizando a API do modelo.

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

*(Esta seção deve ser preenchida por você para detalhar as tecnologias que utilizou, como estruturou o seu projeto, como treinou o modelo e como os componentes se comunicam.)*

### Tecnologias Utilizadas

* **Linguagem:**
* **Modelo de ML:**
* **API:**
* **Chatbot:**
* **Outras bibliotecas:**

### Como Executar o Projeto

*(Inclua aqui as instruções para instalar dependências, treinar o modelo, iniciar a API e interagir com o chatbot.)*"# juscash-technical-challenge" 
"# juscash-technical-challenge" 
