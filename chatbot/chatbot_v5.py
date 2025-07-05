import streamlit as st
import pandas as pd
import requests
import json
import os
import re
from dotenv import load_dotenv

# Importações do LangChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

# =============================================================================
# CONFIGURAÇÃO INICIAL
# =============================================================================
load_dotenv()

st.set_page_config(
    page_title="JusCash | Análise de Projetos com JIA",
    page_icon="https://juscash.com.br/wp-content/uploads/2023/05/favicon_juscash.svg",
    layout="wide"
)

URL_API = "http://127.0.0.1:8000/v2/prever"

# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================
@st.cache_data
def carregar_dados_usuarios():
    """Carrega o arquivo CSV de usuários e calcula os valores padrão."""
    caminho_csv = os.path.join('..', 'modelo_ml', 'data', 'users.csv')
    try:
        df = pd.read_csv(caminho_csv, sep=';')
        df['Experiencia (anos)'] = pd.to_numeric(df['Experiencia (anos)'], errors='coerce')
        df['Historico de Projetos'] = pd.to_numeric(df['Historico de Projetos'], errors='coerce')
        df['Sucesso Medio (percentual)'] = df['Sucesso Medio (percentual)'].str.replace(',', '.', regex=False).astype(float)
        
        default_user = {
            "Nome": "Visitante",
            "Experiencia (anos)": df['Experiencia (anos)'].median(),
            "Historico de Projetos": df['Historico de Projetos'].median(),
            "Sucesso Medio (percentual)": df['Sucesso Medio (percentual)'].median()
        }
        return df, default_user
    except FileNotFoundError:
        st.error(f"Arquivo 'users.csv' não encontrado em '{caminho_csv}'. Verifique o caminho.")
        return None, None

def formatar_historico_chat(messages):
    """Formata o histórico do chat para ser enviado ao modelo de linguagem."""
    return "\n".join([f"{'Usuário' if msg['role'] == 'user' else 'JIA'}: {msg['content']}" for msg in messages])

def chamar_api_predicao(payload):
    """Encapsula a chamada para a API de predição de Machine Learning."""
    try:
        response = requests.post(URL_API, json=payload, timeout=10)
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"Erro na API: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return None, f"Ocorreu um erro de conexão com a API: {e}"

def extrair_json_da_string(text):
    """Usa regex para encontrar e extrair um bloco JSON de uma string de texto."""
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    return None

def reset_for_new_project():
    """Reseta o estado para uma nova análise com o mesmo usuário."""
    st.session_state.dados_coletados = {}
    st.session_state.app_state = "DATA_COLLECTION"
    # Mantém apenas a mensagem de boas-vindas do usuário atual
    st.session_state.assistente_messages = [
        msg for msg in st.session_state.assistente_messages if "Identificação confirmada" in msg.get('content', '')
    ]
    st.session_state.assistente_messages.append({
        "role": "assistant",
        "content": "Vamos lá! Pode me falar sobre o seu novo projeto."
    })
    st.rerun()

def reset_for_new_user():
    """Reseta completamente a sessão para um novo usuário."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# =============================================================================
# INICIALIZAÇÃO DO APP E DO ESTADO DA SESSÃO
# =============================================================================
st.title("Análise de Projetos com a JIA")
st.markdown("Sua assistente de IA para análise de risco e sucesso de projetos.")

df_usuarios, default_info_usuario = carregar_dados_usuarios()
if df_usuarios is None:
    st.stop()

# Gerenciador de estado centralizado
if "app_state" not in st.session_state:
    st.session_state.app_state = "IDENTIFICATION"
if "assistente_messages" not in st.session_state:
    st.session_state.assistente_messages = []
if "info_usuario" not in st.session_state:
    st.session_state.info_usuario = None
if "dados_coletados" not in st.session_state:
    st.session_state.dados_coletados = {}

try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.2, convert_system_message_to_human=True)
except Exception as e:
    st.error(f"Erro ao inicializar o modelo Gemini: {e}")
    st.stop()

# =============================================================================
# LÓGICA PRINCIPAL DO CHAT (MÁQUINA DE ESTADOS)
# =============================================================================

# Exibe o histórico de mensagens
for message in st.session_state.assistente_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ESTADO 1: IDENTIFICATION
if st.session_state.app_state == "IDENTIFICATION":
    if not st.session_state.assistente_messages:
        st.session_state.assistente_messages.append({
            "role": "assistant",
            "content": "Olá! Eu sou a JIA. Para começarmos, por favor, me diga o seu nome."
        })
        st.rerun()

    if prompt := st.chat_input("Digite seu nome..."):
        st.session_state.assistente_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Verificando..."):
            identificacao_prompt = PromptTemplate.from_template("Extraia o nome completo da pessoa da seguinte frase: '{frase}'. Retorne APENAS o nome.")
            chain = LLMChain(llm=llm, prompt=identificacao_prompt)
            nome_extraido = chain.invoke({"frase": prompt}).get('text', '').strip()

            match = df_usuarios[df_usuarios['Nome'].str.lower() == nome_extraido.lower()]
            
            with st.chat_message("assistant"):
                if not match.empty:
                    st.session_state.info_usuario = match.iloc[0].to_dict()
                    nome_formatado = st.session_state.info_usuario['Nome']
                    resposta = f"Perfeito, {nome_formatado}! Identificação confirmada. Agora, vamos ao projeto. Me conte sobre ele."
                else:
                    st.session_state.info_usuario = default_info_usuario
                    st.session_state.info_usuario['Nome'] = nome_extraido if nome_extraido else "Visitante"
                    resposta = f"Olá, {st.session_state.info_usuario['Nome']}! Não encontrei seu histórico, então usarei dados médios para a análise. Vamos começar! Me fale sobre a duração, orçamento e equipe do seu projeto."
                
                st.session_state.assistente_messages.append({"role": "assistant", "content": resposta})
                st.session_state.app_state = "DATA_COLLECTION"
                st.rerun()

# ESTADO 2: DATA_COLLECTION
elif st.session_state.app_state == "DATA_COLLECTION":
    coleta_prompt_template = """
    Você é a JIA. Seu objetivo é coletar os seguintes dados: {campos_necessarios}.
    Dados já coletados: {dados_coletados_json}
    REGRAS DE CLASSIFICAÇÃO: Mapeie a resposta do usuário para uma das opções válidas:
    - "Tipo_Projeto": ['Software', 'Infraestrutura', 'Marketing', 'P&D']
    - "Complexidade": ['Baixa', 'Media', 'Alta']
    - "Risco_Inicial": ['Baixo', 'Medio', 'Alto']
    Ações: Extraia os dados, confirme o que entendeu e peça a próxima informação.
    Histórico: {chat_history}
    Usuário: {user_input}
    Sua resposta DEVE SER APENAS um JSON: {{"dados_extraidos": {{"Campo": "Valor"}}, "resposta_conversacional": "Sua resposta."}}
    """
    campos_necessarios = ["Duracao_Meses", "Orcamento_Milhares_Reais", "Tamanho_Equipe", "Tipo_Projeto", "Complexidade", "Risco_Inicial"]

    if prompt := st.chat_input("Descreva seu projeto..."):
        st.session_state.assistente_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("JIA está pensando..."):
                dados_coletados_keys = st.session_state.dados_coletados.keys()
                dados_faltantes = [item for item in campos_necessarios if item not in dados_coletados_keys]
                
                prompt_para_llm = coleta_prompt_template.format(
                    campos_necessarios=", ".join(dados_faltantes),
                    dados_coletados_json=json.dumps(st.session_state.dados_coletados, indent=2),
                    chat_history=formatar_historico_chat(st.session_state.assistente_messages),
                    user_input=prompt
                )
                
                response_llm_text = llm.invoke(prompt_para_llm).content
                parsed_json = extrair_json_da_string(response_llm_text)
                
                if parsed_json and isinstance(parsed_json.get("dados_extraidos"), dict):
                    dados_novos = parsed_json.get("dados_extraidos")
                    resposta_assistente = parsed_json.get("resposta_conversacional", "Entendi. O que mais?")
                else:
                    dados_novos, resposta_assistente = {}, "Não entendi bem. Pode reformular?"

                if dados_novos:
                    st.session_state.dados_coletados.update(dados_novos)
                
                dados_coletados_final_keys = st.session_state.dados_coletados.keys()
                if all(campo in dados_coletados_final_keys for campo in campos_necessarios):
                    st.markdown("Excelente, tenho todas as informações! Um momento enquanto processo a análise...")
                    
                    info_usuario = st.session_state.info_usuario
                    payload = st.session_state.dados_coletados.copy()
                    payload['Duracao_Meses'] = int(payload.get('Duracao_Meses', 0))
                    payload['Orcamento_Milhares_Reais'] = float(payload.get('Orcamento_Milhares_Reais', 0))
                    payload['Tamanho_Equipe'] = int(payload.get('Tamanho_Equipe', 0))
                    payload.update({
                        "Experiencia (anos)": int(info_usuario['Experiencia (anos)']),
                        "Historico de Projetos": int(info_usuario['Historico de Projetos']),
                        "Sucesso Medio (percentual)": float(info_usuario['Sucesso Medio (percentual)'])
                    })

                    resultado_ml, erro = chamar_api_predicao(payload)
                    
                    if resultado_ml:
                        prob = resultado_ml.get('probabilidade_de_sucesso', 0)
                        previsao = resultado_ml.get('previsao', 'Indefinida')
                        
                        template_final = """
                        Apresente o resultado da análise para {nome_usuario} de forma concisa e direta.
                        Resultado: Previsão de '{previsao}' com {probabilidade:.1%} de chance de sucesso.
                        Explique brevemente o que isso significa e pergunte o que ele gostaria de fazer a seguir (analisar outro projeto ou mudar de usuário).
                        """
                        chain_final = LLMChain(llm=llm, prompt=PromptTemplate.from_template(template_final))
                        response_dict = chain_final.invoke({"previsao": previsao, "probabilidade": prob, "nome_usuario": info_usuario['Nome']})
                        resposta_final = response_dict.get('text', 'Análise concluída!')
                        
                        st.markdown(resposta_final)
                        st.session_state.assistente_messages.append({"role": "assistant", "content": resposta_final})
                        st.session_state.app_state = "POST_ANALYSIS"
                        st.rerun()
                    else:
                        st.error(erro)
                else:
                    st.markdown(resposta_assistente)
                    st.session_state.assistente_messages.append({"role": "assistant", "content": resposta_assistente})

# ESTADO 3: POST_ANALYSIS
elif st.session_state.app_state == "POST_ANALYSIS":
    post_analysis_prompt = """
    Analise a resposta do usuário e classifique sua intenção em uma das três categorias: 'new_project', 'new_user', ou 'end_conversation'.
    - 'novo projeto', 'outro', 'sim': 'new_project'
    - 'mudar de usuário', 'outro gerente', 'não sou eu': 'new_user'
    - 'não', 'obrigado', 'tchau': 'end_conversation'
    Retorne APENAS a categoria.
    Usuário: {user_input}
    """
    
    if prompt := st.chat_input("O que deseja fazer?"):
        st.session_state.assistente_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("..."):
            chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(post_analysis_prompt))
            action = chain.invoke({"user_input": prompt}).get('text', 'end_conversation').strip()

            if "new_project" in action:
                reset_for_new_project()
            elif "new_user" in action:
                reset_for_new_user()
            else:
                with st.chat_message("assistant"):
                    st.markdown("Ok! Se precisar de algo mais, é só chamar. Até logo!")
                st.session_state.app_state = "ENDED"
