# Modelo de Machine Learning - Previsão de Sucesso de Projetos

Este documento detalha a estrutura, configuração e decisões técnicas relacionadas ao modelo de Machine Learning para prever o sucesso de projetos, desenvolvido como parte do case da JusCash.

## 1. Visão Geral

O objetivo deste componente é treinar um modelo de classificação capaz de prever se um projeto será bem-sucedido ou não, com base em suas características e nos dados do gerente de projeto responsável. O modelo treinado é então salvo como um artefato (`.joblib`) para ser consumido por uma API.

## 2. Estrutura de Arquivos

```path
modelo_ml/
│
├── artefatos/
│   └── pipeline_predicao_sucesso_v2.joblib  # Pipeline de ML treinado e salvo
│
├── data/
│   ├── projetos_kaggle_v2.csv               # Dados históricos dos projetos
│   └── users.csv                            # Dados dos gerentes de projeto (usuários)
│
├── src/
│   └── index.py                             # Script de treinamento, avaliação e salvamento do modelo
│
├── api.py                                   # API (FastAPI) para servir o modelo treinado
├── requirements.txt                         # Dependências Python do projeto
└── README.md                                # Esta documentação

```

## 3. Tutorial de Configuração e Execução

Para configurar e executar este serviço, siga os passos abaixo.

### 3.1. Pré-requisitos

- Python 3.8 ou superior

- `pip` (gerenciador de pacotes do Python)

### 3.2. Instalação das Dependências

1. Navegue até a pasta `modelo_ml` no seu terminal.

2. Crie e ative um ambiente virtual (recomendado):

    ```bash

        python -m venv venv

        # No Linux:
        source venv/bin/activate
        
        # No Windows:
        venv\Scripts\activate

    ```

3. Instale as bibliotecas necessárias a partir do arquivo `requirements.txt`:

    ```bash
    
        pip install -r requirements.txt
    
    ```

### 3.3. Treinamento do Modelo

O script `src/index.py` é responsável por todo o ciclo de vida do treinamento. Para executá-lo:

```bash

    python src/index.py

```

Este comando irá:

1. Carregar os datasets de projetos e usuários.

2. Realizar uma análise exploratória básica.

3. Pré-processar os dados, lidando com valores ausentes e codificando variáveis categóricas.

4. Treinar dois modelos: **Regressão Logística** e **Random Forest**.

5. Avaliar ambos os modelos usando o **F1-Score** e selecionar o melhor.

6. Salvar o pipeline completo (pré-processador + modelo) no arquivo `artefatos/pipeline_predicao_sucesso_v2.joblib`.

### 3.4. Execução da API

A API, construída com **FastAPI**, serve o modelo treinado. Para iniciá-la:

1. Certifique-se de que o arquivo `pipeline_predicao_sucesso_v2.joblib` existe na pasta `artefatos`.

2. Na raiz da pasta `modelo_ml`, execute o seguinte comando:

    ```bash
        
        uvicorn api:app --reload
        
    ```

3. A API estará disponível no endereço `http://127.0.0.1:8000`.

4. Para interagir com a API e ver a documentação dos endpoints, acesse `http://127.0.0.1:8000/docs` no seu navegador.

## 4. Escolhas Técnicas e Pontos Importantes do Código

### 4.1. Script de Treinamento (`src/index.py`)

- **Pipeline do Scikit-learn**: A escolha de usar `Pipeline` e `ColumnTransformer`garante que o pré-processamento (imputação de dados faltantes, escalonamento de features numéricas e one-hot encoding de features categóricas) seja aplicado de forma consistente tanto no treino quanto na inferência pela API, isso evita data leakage.

- **Tratamento de Dados Ausentes**: O `SimpleImputer` foi adicionado para lidar com valores `NaN`. Para features numéricas, a estratégia foi a `mediana`, que é robusta a outliers. Para as categóricas, usou-se a `most_frequent` (valor mais frequente, moda).

- **Seleção de Modelo**: Foram treinados dois modelos distintos: `LogisticRegression` e `RandomForestClassifier`. A seleção do melhor modelo é feita automaticamente com base no **F1-Score**, uma métrica de avaliação para problemas de classificação, especialmente quando pode haver desbalanceamento de classes.

### 4.2. API (`api.py`)

- **FastAPI**: A escolha do FastAPI como framework para a API se deve à sua alta performance, documentação automática (via Swagger UI, que pode ser acessada e testada quando executada a API) e uso de tipagem de dados com Pydantic, o que torna a API mais robusta e fácil de usar.

- **Pydantic para Validação**: O `BaseModel` do Pydantic é usado para definir o "contrato" dos dados de entrada (`DadosEntradaProjeto`). Isso garante que qualquer requisição feita à API com dados em formato incorreto (e.g., um tipo de projeto que não existe ou um valor não numérico para o orçamento) seja automaticamente rejeitada com uma mensagem de erro clara, aumentando a confiabilidade do serviço.

- **Alias de Campos**: O uso de `alias` na classe Pydantic, como `alias="Experiencia (anos)"`. Isso permite que a API aceite um nome de campo amigável para JSON (`Experiencia_anos`) e o mapeie internamente para o nome da coluna usado no treinamento do modelo (`Experiencia (anos)`), facilitando a integração.

### 4.3. Dependências (`requirements.txt`)

- **scikit-learn**: Biblioteca central para o treinamento do modelo de Machine Learning.

- **pandas/numpy**: Essenciais para a manipulação e pré-processamento dos dados.

- **fastapi/uvicorn**: Utilizados para construir e servir a API REST.

- **joblib**: Necessário para serializar (salvar) e desserializar (carregar) o pipeline do scikit-learn de forma eficiente.
