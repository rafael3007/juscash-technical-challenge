from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
import joblib
import os
from typing import Literal

# --- INICIALIZAÇÃO DA API E CARREGAMENTO DO MODELO ---
app = FastAPI(
    title="JusCash - API de Previsão de Sucesso",
    version="2.1.5"
)

# Carregando o novo pipeline
caminho_artefato = os.path.join('artefatos', 'pipeline_predicao_sucesso_v2.joblib')
pipeline = None
try:
    pipeline = joblib.load(caminho_artefato)
    print(f"Pipeline carregado com sucesso de: {caminho_artefato}")
except Exception as e:
    print(f"Erro ao carregar o pipeline: {e}")
    pipeline = None

# --- DEFINIÇÃO DO MODELO DE DADOS DE ENTRADA (PYDANTIC) ---
class DadosEntradaProjeto(BaseModel):
    # Features do projeto
    Duracao_Meses: int = Field(..., example=12, description="Duração total do projeto em meses.")
    Orcamento_Milhares_Reais: float = Field(..., example=500.0, description="Orçamento em milhares de R$. Ex: 500.0 para R$500.000.")
    Tamanho_Equipe: int = Field(..., example=8)
    Tipo_Projeto: Literal['Software', 'Infraestrutura', 'Marketing', 'P&D']
    Complexidade: Literal['Baixa', 'Media', 'Alta']
    Risco_Inicial: Literal['Baixo', 'Medio', 'Alto']

    # Features dos usuarios que serão combinadas
    Experiencia_anos: int = Field(..., example=5, alias="Experiencia (anos)")
    Historico_de_Projetos: int = Field(..., example=15, alias="Historico de Projetos")
    Sucesso_Medio_percentual: float = Field(..., example=0.8, alias="Sucesso Medio (percentual)")

    class Config:
        populate_by_name = True

# --- ENDPOINT DE PREVISÃO ---
@app.post("/v2/prever")
def prever_sucesso_v2(dados: DadosEntradaProjeto):
    """
    Recebe os dados de um novo projeto e do gerente para prever o sucesso.
    """
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Modelo v2 não está disponível.")

    try:
        # Converte os dados Pydantic para um dicionário
        dados_dict = dados.dict(by_alias=True)

        # Transforma o dicionário em um DataFrame
        df_para_prever = pd.DataFrame([dados_dict])

        # Garante a ordem correta das colunas como no treinamento
        colunas_treinamento = [
            'Duracao_Meses', 'Orcamento_Milhares_Reais', 'Tamanho_Equipe',
            'Tipo_Projeto', 'Complexidade', 'Risco_Inicial',
            'Historico de Projetos', 'Experiencia (anos)', 'Sucesso Medio (percentual)'
        ]
        df_para_prever = df_para_prever[colunas_treinamento]

        # Faz a previsão de probabilidade
        probabilidade = pipeline.predict_proba(df_para_prever)
        probabilidade_sucesso = probabilidade[0][1]

        return {
            "previsao": "Sucesso" if probabilidade_sucesso > 0.5 else "Fracasso",
            "probabilidade_de_sucesso": round(probabilidade_sucesso, 4)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro na previsão: {str(e)}")

@app.get("/")
def read_root():
    return {"status": "API da JusCash no ar!", "docs_url": "/docs"}

