# =============================================================================
# PASSO 0: IMPORTAÇÃO DAS BIBLIOTECAS
# =============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer # <-- IMPORTANTE: Adicionado para lidar com valores ausentes
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score

sns.set_style('whitegrid')
print("Bibliotecas importadas.")

# =============================================================================
# PASSO 1: CARREGAMENTO DOS DADOS
# =============================================================================
print("\n--- Carregando os dados v2 ---")
PASTA_DADOS = '../data'
try:
    df_projetos = pd.read_csv('../data/projetos_kaggle_v2.csv', sep=';', decimal='.')
    df_usuarios = pd.read_csv('../data/users.csv', sep=';', decimal='.')
    print("Arquivos CSV v2 carregados com sucesso.")
except FileNotFoundError as e:
    print(f"Erro: Arquivo não encontrado. Execute o script 'gerar_dados_v2.py' primeiro.")
    exit()

# Juntando os dados do gerente (usuário) ao dataset de projetos para o treinamento
df_treinamento = pd.merge(df_projetos, df_usuarios, left_on='ID_Gerente', right_on='Usuario_ID', how='left')
print("Shape do DataFrame de treinamento combinado:", df_treinamento.shape)
print(df_treinamento.head())

# =============================================================================
# PASSO 2: ANÁLISE EXPLORATÓRIA DE DADOS (EDA)
# =============================================================================
print("\n--- Análise Exploratória (EDA) ---")
df_treinamento.info()

# Verificando valores ausentes (NaN) - a causa do erro
print("\nVerificando valores ausentes (NaN) por coluna:")
print(df_treinamento.isnull().sum())
# Se houver NaNs, eles aparecerão aqui. O passo de imputação abaixo irá corrigi-los.

# Visualizando a influência das novas variáveis categóricas no sucesso
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
sns.countplot(ax=axes[0], x='Tipo_Projeto', hue='Sucesso', data=df_treinamento)
axes[0].set_title('Sucesso por Tipo de Projeto')
sns.countplot(ax=axes[1], x='Complexidade', hue='Sucesso', data=df_treinamento)
axes[1].set_title('Sucesso por Complexidade')
sns.countplot(ax=axes[2], x='Risco_Inicial', hue='Sucesso', data=df_treinamento)
axes[2].set_title('Sucesso por Risco Inicial')
plt.tight_layout()
plt.show()

# =============================================================================
# PASSO 3: PRÉ-PROCESSAMENTO E DEFINIÇÃO DO PIPELINE
# =============================================================================
print("\n--- Pré-processamento e Pipeline ---")

# A variável alvo é 'Sucesso'. As features são todas as outras colunas relevantes.
features_para_remover = ['ID_Projeto', 'ID_Gerente', 'Usuario_ID', 'Nome', 'Cargo', 'Sucesso']
X = df_treinamento.drop(columns=features_para_remover)
y = df_treinamento['Sucesso']

# Dividindo em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Identificando colunas numéricas e categóricas para o pré-processamento
numeric_features = X.select_dtypes(include=np.number).columns.tolist()
categorical_features = X.select_dtypes(exclude=np.number).columns.tolist()

print("\nFeatures numéricas para escalar:", numeric_features)
print("Features categóricas para OneHotEncode:", categorical_features)

# CORREÇÃO: Criando pipelines separados para features numéricas e categóricas
# para incluir a etapa de imputação (preenchimento de NaNs).

# Pipeline para dados numéricos: preenche NaNs com a mediana e depois escala.
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Pipeline para dados categóricos: preenche NaNs com o valor mais frequente e depois aplica OneHotEncoding.
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Juntando os transformadores com ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# =============================================================================
# PASSO 4: TREINAMENTO E AVALIAÇÃO DOS MODELOS
# =============================================================================
print("\n--- Treinando e Avaliando Modelos ---")

# Modelo 1: Regressão Logística
pipeline_logreg = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', LogisticRegression(random_state=42))])
pipeline_logreg.fit(X_train, y_train)
y_pred_logreg = pipeline_logreg.predict(X_test)
print("\nRelatório de Classificação - Regressão Logística:")
print(classification_report(y_test, y_pred_logreg))

# Modelo 2: Random Forest
pipeline_rf = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', RandomForestClassifier(random_state=42))])
pipeline_rf.fit(X_train, y_train)
y_pred_rf = pipeline_rf.predict(X_test)
print("\nRelatório de Classificação - Random Forest:")
print(classification_report(y_test, y_pred_rf))

# =============================================================================
# PASSO 5: SELEÇÃO E SALVAMENTO DO MELHOR MODELO
# =============================================================================
print("\n--- Seleção do Modelo Final ---")
f1_rf = f1_score(y_test, y_pred_rf)
f1_logreg = f1_score(y_test, y_pred_logreg)

if f1_rf > f1_logreg:
    melhor_pipeline = pipeline_rf
    nome_modelo = "Random Forest"
else:
    melhor_pipeline = pipeline_logreg
    nome_modelo = "Regressão Logística"

print(f"Modelo selecionado: {nome_modelo} com F1-Score de {max(f1_rf, f1_logreg):.4f}")

# Salvando o pipeline v2
PASTA_ARTEFATOS = '../artefatos'
os.makedirs(PASTA_ARTEFATOS, exist_ok=True)
caminho_artefato = os.path.join(PASTA_ARTEFATOS, 'pipeline_predicao_sucesso_v2.joblib')
joblib.dump(melhor_pipeline, caminho_artefato)
print(f"Pipeline v2 salvo com sucesso em: '{caminho_artefato}'")
