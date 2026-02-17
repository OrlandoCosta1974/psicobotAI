# psicobot_app.py - Versão com IA real (Groq) - CHAVE HARDCODED

import streamlit as st
import sqlite3
import hashlib
from datetime import datetime, timedelta
import json
import base64
import requests
import os

# ============================================
# IMPORTS PARA PDF PROFISSIONAL
# ============================================
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from io import BytesIO
# ============================================

# ============================================
# CHAVE DA API GROQ (HARDCODED - FUNCIONA IMEDIATAMENTE)
# ============================================
GROQ_API_KEY = "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"
# ============================================

# Configuração da página
st.set_page_config(
    page_title="PsicoBot - Avaliação Psicológica",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ... [RESTO DO CSS PERMANECE IGUAL] ...

# [TODAS AS FUNÇÕES PERMANECEM IGUAIS ATÉ analisar_com_ia]

def analisar_com_ia(dados):
    """
    Analisa os dados do paciente usando IA real (Groq API)
    """
    # Usa chave hardcoded (funciona imediatamente)
    api_key = GROQ_API_KEY
    
    # Monta o prompt com os dados do paciente
    prompt = f"""
    Você é um psicólogo clínico experiente com 20 anos de prática. Analise os seguintes 
    dados de um paciente e forneça uma avaliação profissional detalhada em formato JSON.
    
    DADOS DO PACIENTE:
    - Nome: {dados.get('nome', 'Não informado')}
    - Idade: {dados.get('idade', 'Não informado')}
    - Ocupação: {dados.get('ocupacao', 'Não informado')}
    - Queixa principal: {dados.get('queixa', 'Não informado')}
    - Duração dos sintomas: {dados.get('duracao', 'Não informado')}
    - Qualidade do sono: {dados.get('sono', 'Não informado')}
    - Alterações no apetite: {dados.get('apetite', 'Não informado')}
    - Nível de energia (0-10): {dados.get('energia', 'Não informado')}
    - Histórico de pensamentos suicidas: {dados.get('suicidio', 'Não informado')}
    - Apoio social disponível: {dados.get('apoio', 'Não informado')}
    
    INSTRUÇÕES PARA ANÁLISE:
    1. Faça uma hipótese diagnóstica precisa baseada nos sintomas apresentados
    2. Classifique a severidade considerando impacto funcional (Leve, Moderada, Grave)
    3. Avalie cuidadosamente o risco suicida (Ausente, Ideação, Plano, Intenção)
    4. Recomende o tratamento mais adequado (tipo de terapia, frequência, necessidade de medicação)
    5. Forneça uma breve justificativa clínica da sua avaliação
    6. Sugira 3 estratégias práticas e específicas para o caso deste paciente
    
    IMPORTANTE: Seja específico e personalizado. Não use respostas genéricas.
    Considere a idade, ocupação e contexto do paciente nas recomendações.
    
    RETORNE APENAS ESTE FORMATO JSON (sem markdown, sem explicações extras):
    {{
        "categoria": "Nome específico do quadro clínico",
        "severidade": "Leve/Moderada/Grave",
        "risco": "Ausente/Ideação/Plano/Intenção",
        "recomendacao": "Tipo de tratamento específico recomendado",
        "justificativa": "Breve explicação do raciocínio clínico (2-3 frases)",
        "estrategias": [
            "Estratégia 1 específica e acionável para este paciente",
            "Estratégia 2 específica e acionável para este paciente", 
            "Estratégia 3 específica e acionável para este paciente"
        ]
    }}
    """
    
    # Chama a API do Groq
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "Você é um psicólogo clínico experiente. Responda apenas em JSON válido, sem markdown."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 1200
    }
    
    try:
        with st.spinner("🧠 Analisando com IA..."):
            response = requests.post(url, headers=headers, json=data, timeout=45)
            response.raise_for_status()
            
            # Extrai o conteúdo da resposta
            content = response.json()['choices'][0]['message']['content']
            
            # Limpa possíveis markdown
            content = content.replace('```json', '').replace('```', '').strip()
            
            # Tenta fazer parse do JSON
            resultado = json.loads(content)
            
            # Valida campos obrigatórios
            campos_obrigatorios = ['categoria', 'severidade', 'risco', 'recomendacao', 'estrategias']
            for campo in campos_obrigatorios:
                if campo not in resultado:
                    resultado[campo] = "Não avaliado" if campo != 'estrategias' else ["Consulte um profissional"]
            
            # Garante que estrategias é uma lista
            if not isinstance(resultado.get('estrategias'), list):
                resultado['estrategias'] = [str(resultado.get('estrategias', 'Consulte um profissional'))]
            
            return resultado
            
    except requests.exceptions.RequestException as e:
        st.warning("⚠️ Erro de conexão com IA. Usando análise local...")
        return simula_diagnostico(dados)
    except json.JSONDecodeError as e:
        st.warning("⚠️ Erro ao processar resposta da IA. Usando análise local...")
        return simula_diagnostico(dados)
    except Exception as e:
        st.warning(f"⚠️ Erro inesperado. Usando análise local...")
        return simula_diagnostico(dados)


# [RESTO DO CÓDIGO PERMANECE IGUAL: salvar_avaliacao, main, etc]

def main():
    # Container principal com fundo escuro
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header
    st.title("🧠 PsicoBot")
    st.markdown('<p class="subtitle">Avaliação Psicológica Inteligente</p>', unsafe_allow_html=True)
    
    # Badge de status da IA
    st.success("🤖 IA Ativa (Groq/Llama 3)")
    
    # Inicialização
    if 'step' not in st.session_state:
        st.session_state.step = 0
        st.session_state.dados = {}
        st.session_state.user_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
    
    # ... RESTO DO MAIN PERMANECE IGUAL ...
    
    # [COLE O RESTO DO SEU CÓDIGO AQUI]

if __name__ == "__main__":
    main()
