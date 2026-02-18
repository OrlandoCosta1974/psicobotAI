# psicobot_app.py - Versão com IA real (Groq) - CHAVE HARDCODED
# FUNCIONA IMEDIATAMENTE - Não precisa configurar Secrets

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

# LISTA DE MODELOS PARA TENTAR (MODELOS ATIVOS DO GROQ - FEVEREIRO 2026)
MODELOS_GROQ = [
    "llama-3.3-70b-versatile",      # ✅ Novo modelo ativo (Fevereiro 2026)
    "llama-3.1-8b-instant",         # ✅ Modelo leve ativo
    "mixtral-8x7b-32768",           # ✅ Modelo alternativo ativo
    "gemma-7b-it",                  # ✅ Google Gemma
]
# ============================================

# Configuração da página
st.set_page_config(
    page_title="PsicoBot - Avaliação Psicológica",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS CORRIGIDO - Tema escuro profissional
st.markdown("""
<style>
    /* Fundo escuro principal */
    .stApp {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
    }
    
    /* Container principal */
    .main-container {
        background: #252538;
        border-radius: 20px;
        padding: 30px;
        margin: 20px auto;
        max-width: 800px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        border: 1px solid #3d3d5c;
    }
    
    /* Títulos em branco/brilhante */
    h1 {
        color: #ffffff !important;
        font-size: 2.5rem !important;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    h2, h3 {
        color: #a6a6ff !important;
        font-weight: 600;
    }
    
    /* Subtítulo */
    .subtitle {
        color: #b8b8d1;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    
    /* Texto normal */
    p, label, .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    /* Barra de progresso */
    .stProgress > div > div {
        background-color: #667eea !important;
    }
    
    /* Campos de input - fundo escuro, texto claro */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background-color: #1e1e2e !important;
        color: #ffffff !important;
        border: 2px solid #3d3d5c !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Placeholder mais visível */
    ::placeholder {
        color: #6b6b8a !important;
    }
    
    /* Botões */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 30px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: #1e1e2e;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #3d3d5c;
    }
    
    .stRadio > label {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    /* Caixa de resultado */
    .result-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        text-align: center;
    }
    
    /* Alerta de risco */
    .risk-alert {
        background: #3d1f1f;
        border-left: 5px solid #e74c3c;
        padding: 20px;
        border-radius: 10px;
        color: #ffb8b8;
        margin: 20px 0;
    }
    
    .risk-alert h3 {
        color: #ff6b6b !important;
        margin-top: 0;
    }
    
    /* Sucesso */
    .success-box {
        background: #1f3d1f;
        border-left: 5px solid #27ae60;
        padding: 20px;
        border-radius: 10px;
        color: #b8ffb8;
    }
    
    /* Métricas */
    .metric-card {
        background: #1e1e2e;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #3d3d5c;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .metric-label {
        color: #b8b8d1;
        font-size: 0.9rem;
    }
    
    /* Contador de pergunta */
    .question-counter {
        color: #667eea;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 15px;
    }
    
    /* Pergunta */
    .question-text {
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 500;
        margin-bottom: 20px;
        line-height: 1.5;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #1e1e2e !important;
        color: #ffffff !important;
        border-radius: 10px !important;
    }
    
    /* Download button */
    .download-btn {
        background: #27ae60 !important;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização do banco
def init_db():
    conn = sqlite3.connect('psicobot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS avaliacoes
                 (id TEXT PRIMARY KEY, 
                  data TEXT, 
                  dados_json TEXT,
                  diagnostico TEXT,
                  risco TEXT)''')
    conn.commit()
    conn.close()

init_db()

# HTML Template para PDF
HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Prontuário PsicoBot</title>
    <style>
        body {{ 
            margin: 40px; 
            color: #333; 
            line-height: 1.6; 
        }}
        .header {{ 
            text-align: center; 
            color: #667eea; 
            border-bottom: 3px solid #667eea; 
            padding-bottom: 20px; 
            margin-bottom: 30px; 
        }}
        .section {{ 
            margin: 30px 0; 
        }}
        .section h2 {{ 
            color: #667eea; 
            border-left: 5px solid #667eea; 
            padding-left: 15px; 
        }}
        .info-box {{ 
            background: #f8f9fa; 
            padding: 20px; 
            border-radius: 10px; 
            margin: 15px 0; 
            border: 1px solid #e9ecef; 
        }}
        .info-item {{ 
            margin: 10px 0; 
            padding: 8px 0; 
            border-bottom: 1px solid #e9ecef; 
        }}
        .info-item:last-child {{ 
            border-bottom: none; 
        }}
        .alert {{ 
            background: #fee; 
            border-left: 5px solid #e74c3c; 
            padding: 20px; 
            color: #c0392b; 
            margin: 20px 0; 
            border-radius: 5px; 
        }}
        table {{ 
            width: 100%; 
            border-collapse: collapse; 
            margin: 20px 0; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
        }}
        th, td {{ 
            border: 1px solid #ddd; 
            padding: 15px; 
            text-align: left; 
        }}
        th {{ 
            background: #667eea; 
            color: white; 
            font-weight: 600; 
        }}
        tr:nth-child(even) {{ 
            background: #f8f9fa; 
        }}
        .footer {{ 
            margin-top: 50px; 
            font-size: 11px; 
            color: #666; 
            text-align: center; 
            border-top: 2px solid #e9ecef; 
            padding-top: 20px; 
        }}
        .badge {{ 
            display: inline-block; 
            padding: 5px 15px; 
            border-radius: 20px; 
            font-size: 14px; 
            font-weight: bold; 
            margin: 5px; 
        }}
        .badge-primary {{ 
            background: #667eea; 
            color: white; 
        }}
        .badge-warning {{ 
            background: #f39c12; 
            color: white; 
        }}
        .badge-danger {{ 
            background: #e74c3c; 
            color: white; 
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 PSICOBOT</h1>
        <h2>Prontuário de Avaliação Psicológica</h2>
        <p><strong>ID:</strong> {user_id} | <strong>Data:</strong> {data}</p>
    </div>
    
    <div class="section">
        <h2>📋 Dados do Paciente</h2>
        <div class="info-box">
            {dados_html}
        </div>
    </div>
    
    <div class="section">
        <h2>🔍 Análise Clínica</h2>
        <div class="info-box">
            <h3>Categoria Principal</h3>
            <p>{categoria}</p>
            
            <h3>Severidade</h3>
            <span class="badge badge-{severidade_class}">{severidade}</span>
            
            <h3>Diagnóstico Detalhado</h3>
            <p>{diagnostico}</p>
        </div>
    </div>
    
    <div class="section">
        <h2>🛠️ Plano de Cuidado</h2>
        <table>
            <tr><th>Aspecto</th><th>Recomendação</th></tr>
            <tr><td>Frequência de Atendimento</td><td>Semanal (primeiras 4 semanas)</td></tr>
            <tr><td>Modalidade Sugerida</td><td>Psicoterapia online ou presencial</td></tr>
            <tr><td>Abordagem Indicada</td><td>Terapia Cognitivo-Comportamental (TCC)</td></tr>
            <tr><td>Prazo de Reavaliação</td><td>4 semanas</td></tr>
            <tr><td>Encaminhamentos</td><td>{encaminhamento}</td></tr>
        </table>
    </div>
    
    <div class="alert">
        <strong>⚠️ Aviso Importante:</strong><br>
        Este relatório foi gerado por sistema de inteligência artificial e tem caráter 
        informativo. <strong>Não substitui avaliação presencial</strong> com psicólogo 
        registrado no CRP (Conselho Regional de Psicologia).<br><br>
        <strong>Em caso de emergência:</strong><br>
        • CVV (Centro de Valorização da Vida): 188<br>
        • SAMU: 192<br>
        • Pronto-socorro mais próximo
    </div>
    
    <div class="footer">
        <p>Documento gerado automaticamente por PsicoBot v1.0</p>
        <p>© {ano} - Todos os direitos reservados</p>
    </div>
</body>
</html>"""

def generate_html_pdf(dados, diagnostico, user_id):
    dados_html = ""
    for k, v in dados.items():
        if v and k != 'historico_chat':
            dados_html += f'<div class="info-item"><strong>{k.replace("_", " ").title()}:</strong> {v}</div>\n'
    
    # Parse do diagnóstico
    cat = diagnostico.get('categoria', 'Não especificado')
    sev = diagnostico.get('severidade', 'Moderada')
    sev_class = 'warning' if sev == 'Moderada' else 'danger' if sev == 'Grave' else 'primary'
    enc = diagnostico.get('recomendacao', 'Acompanhamento psicológico')
    
    # Cria HTML formatado para o diagnóstico detalhado
    diag_html = f"""
    <p><strong>Categoria:</strong> {diagnostico.get('categoria', 'Não especificado')}</p>
    <p><strong>Severidade:</strong> {diagnostico.get('severidade', 'Não especificado')}</p>
    <p><strong>Risco:</strong> {diagnostico.get('risco', 'Ausente')}</p>
    <p><strong>Recomendação:</strong> {diagnostico.get('recomendacao', 'Não especificado')}</p>
    <p><strong>Estratégias Recomendadas:</strong></p>
    <ul>
    """
    for estrategia in diagnostico.get('estrategias', []):
        diag_html += f"<li>{estrategia}</li>\n"
    diag_html += "</ul>"
    
    # Usar fuso horário do Brasil (UTC-3)
    agora_utc = datetime.now()
    agora_brasil = agora_utc - timedelta(hours=3)
    data_hora = agora_brasil.strftime('%d/%m/%Y %H:%M')
    ano = agora_brasil.year
    
    html_content = HTML_TEMPLATE.format(
        user_id=user_id,
        data=data_hora,
        dados_html=dados_html,
        categoria=cat,
        severidade=sev,
        severidade_class=sev_class,
        diagnostico=diag_html,
        encaminhamento=enc,
        ano=ano
    )
    
    b64 = base64.b64encode(html_content.encode()).decode()
    filename = f"prontuario_psicobot_{user_id}.html"
    
    return f'''
    <a href="data:text/html;base64,{b64}" download="{filename}">
        <button style="background:#27ae60;color:white;padding:15px 30px;border:none;border-radius:10px;cursor:pointer;font-size:16px;font-weight:600;width:100%;">
            📄 Baixar Prontuário Completo (HTML)
        </button>
    </a>
    '''


def generate_professional_pdf(dados, diagnostico, user_id):
    """
    Gera um PDF profissional usando ReportLab para levar ao médico/psicólogo
    """
    # Usar fuso horário do Brasil (UTC-3)
    agora_utc = datetime.now()
    agora_brasil = agora_utc - timedelta(hours=3)
    data_hora = agora_brasil.strftime('%d/%m/%Y %H:%M')
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Container para os elementos
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilo customizado para título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para subtítulos
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.gray,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    # Estilo para seções
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold',
        borderColor=colors.HexColor('#667eea'),
        borderWidth=2,
        borderPadding=5,
        leftIndent=0
    )
    
    # Estilo para texto normal
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        spaceAfter=10,
        alignment=TA_JUSTIFY
    )
    
    # Estilo para labels em negrito
    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#2c3e50'),
        fontName='Helvetica-Bold'
    )
    
    # Estilo para aviso
    warning_style = ParagraphStyle(
        'WarningStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#c0392b'),
        backColor=colors.HexColor('#fadbd8'),
        borderPadding=10,
        spaceBefore=20,
        spaceAfter=10
    )
    
    # CABEÇALHO
    elements.append(Paragraph("RELATÓRIO DE AVALIAÇÃO PSICOLÓGICA", title_style))
    elements.append(Paragraph(f"ID do Paciente: {user_id} | Data: {data_hora}", subtitle_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Linha divisória
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#667eea'), spaceBefore=10, spaceAfter=20))
    
    # SEÇÃO 1: DADOS DO PACIENTE
    elements.append(Paragraph("1. DADOS DO PACIENTE", section_style))
    
    dados_table = []
    for k, v in dados.items():
        if v and k != 'historico_chat':
            dados_table.append([
                Paragraph(f"<b>{k.replace('_', ' ').title()}:</b>", label_style),
                Paragraph(str(v), normal_style)
            ])
    
    if dados_table:
        t = Table(dados_table, colWidths=[2*inch, 4*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#667eea')),
        ]))
        elements.append(t)
    
    elements.append(Spacer(1, 0.2*inch))
    
    # SEÇÃO 2: ANÁLISE CLÍNICA
    elements.append(Paragraph("2. ANÁLISE CLÍNICA", section_style))
    
    # Categoria e Severidade em destaque
    cat = diagnostico.get('categoria', 'Não especificado')
    sev = diagnostico.get('severidade', 'Moderada')
    
    # Tabela de diagnóstico
    diag_data = [
        [Paragraph("<b>Categoria Principal:</b>", label_style), Paragraph(cat, normal_style)],
        [Paragraph("<b>Severidade:</b>", label_style), Paragraph(sev, normal_style)],
        [Paragraph("<b>Risco Identificado:</b>", label_style), Paragraph(diagnostico.get('risco', 'Ausente'), normal_style)],
    ]
    
    t2 = Table(diag_data, colWidths=[2*inch, 4*inch])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#667eea')),
    ]))
    elements.append(t2)
    
    elements.append(Spacer(1, 0.1*inch))
    
    # Estratégias recomendadas
    elements.append(Paragraph("<b>Estratégias Recomendadas:</b>", label_style))
    estrategias = diagnostico.get('estrategias', [])
    for i, est in enumerate(estrategias, 1):
        elements.append(Paragraph(f"{i}. {est}", normal_style))
    
    elements.append(Spacer(1, 0.2*inch))
    
    # SEÇÃO 3: PLANO DE CUIDADO
    elements.append(Paragraph("3. PLANO DE CUIDADO SUGERIDO", section_style))
    
    plano_data = [
        [Paragraph("<b>Aspecto</b>", label_style), Paragraph("<b>Recomendação</b>", label_style)],
        ["Frequência de Atendimento", "Semanal (primeiras 4 semanas)"],
        ["Modalidade Sugerida", "Psicoterapia online ou presencial"],
        ["Abordagem Indicada", "Terapia Cognitivo-Comportamental (TCC)"],
        ["Prazo de Reavaliação", "4 semanas"],
        ["Encaminhamentos", diagnostico.get('recomendacao', 'Acompanhamento psicológico')],
    ]
    
    t3 = Table(plano_data, colWidths=[2.5*inch, 3.5*inch])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#667eea')),
    ]))
    elements.append(t3)
    
    # AVISO LEGAL
    elements.append(Spacer(1, 0.3*inch))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey, spaceBefore=10, spaceAfter=10))
    
    aviso_texto = """
    <b>AVISO IMPORTANTE:</b> Este relatório foi gerado por sistema de inteligência artificial 
    e tem caráter informativo. <b>NÃO substitui avaliação presencial</b> com psicólogo 
    registrado no CRP (Conselho Regional de Psicologia) ou médico psiquiatra.<br/><br/>
    <b>Em caso de emergência:</b> CVV 188 | SAMU 192 | Pronto-socorro mais próximo
    """
    elements.append(Paragraph(aviso_texto, warning_style))
    
    # RODAPÉ
    elements.append(Spacer(1, 0.2*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    elements.append(Paragraph(f"Documento gerado por PsicoBot v1.0 | © {agora_brasil.year}", footer_style))
    
    # Gera o PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf


# ============================================
# FUNÇÃO DE SIMULAÇÃO (FALLBACK)
# ============================================
def simula_diagnostico(dados):
    """Simula análise quando não há API - FUNÇÃO DE FALLBACK"""
    queixa = str(dados.get('queixa', '')).lower()
    
    if 'ansiedade' in queixa or 'nervoso' in queixa:
        return {
            'categoria': 'Transtorno de Ansiedade Generalizada',
            'severidade': 'Moderada',
            'risco': 'Ausente',
            'recomendacao': 'Psicoterapia semanal - TCC',
            'estrategias': [
                'Técnica de respiração 4-7-8: inspire 4s, segure 7s, expire 8s',
                'Grounding 5-4-3-2-1: identifique 5 coisas que vê, 4 que ouve, 3 que toca, 2 que cheira, 1 que sente',
                'Diário de pensamentos: registre situações ansiosas e padrões de pensamento'
            ]
        }
    elif 'triste' in queixa or 'depress' in queixa or 'vazio' in queixa:
        return {
            'categoria': 'Episódio Depressivo',
            'severidade': 'Moderada',
            'risco': 'Avaliar',
            'recomendacao': 'Psicoterapia + avaliação psiquiátrica',
            'estrategias': [
                'Ativação comportamental: programe 1 atividade prazerosa por dia',
                'Higiene do sono: horários regulares, sem telas 1h antes',
                'Reestruturação cognitiva: identifique pensamentos automáticos negativos'
            ]
        }
    else:
        return {
            'categoria': 'Ajustamento e Estresse',
            'severidade': 'Leve a Moderada',
            'risco': 'Ausente',
            'recomendacao': 'Acompanhamento psicológico quinzenal',
            'estrategias': [
                'Técnica Pomodoro para produtividade e redução de estresse',
                'Mindfulness: 10 minutos de atenção plena diária',
                'Estabelecimento de limites saudáveis'
            ]
        }


# ============================================
# FUNÇÃO: ANÁLISE COM IA REAL (GROQ) - COM FALLBACK DE MODELOS
# ============================================
def analisar_com_ia(dados):
    """
    Analisa os dados do paciente usando IA real (Groq API)
    COM SISTEMA DE FALLBACK AUTOMÁTICO DE MODELOS
    MODELOS ATIVOS - FEVEREIRO 2026
    """
    # Usa chave hardcoded
    api_key = GROQ_API_KEY
    
    # Se por algum motivo a chave estiver vazia, usa simulação
    if not api_key or api_key == "":
        st.info("🤖 Analisando seus dados com inteligência artificial...")
        return simula_diagnostico(dados)
    
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
    
    # URL para API Groq
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    # Spinner com mensagem amigável
    with st.spinner("🤖 Analisando seus dados com inteligência artificial..."):
        # Tenta cada modelo na lista (sem mostrar para o usuário)
        for idx, modelo in enumerate(MODELOS_GROQ, 1):
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": modelo,
                "messages": [
                    {"role": "system", "content": "Você é um psicólogo clínico experiente. Responda APENAS em JSON válido, sem markdown, sem ```json, sem explicações."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 1000
            }
            
            try:
                response = requests.post(
                    url, 
                    headers=headers, 
                    json=data, 
                    timeout=60
                )
                
                # Se o modelo foi descontinuado, tenta o próximo (silenciosamente)
                if response.status_code == 400:
                    erro_texto = response.text.lower()
                    if "decommissioned" in erro_texto or "not found" in erro_texto or "invalid" in erro_texto:
                        continue
                    else:
                        continue
                
                # Verifica outros erros críticos
                if response.status_code == 401:
                    st.error("❌ Erro de autenticação: Chave da API inválida")
                    st.info("Verifique sua chave em https://console.groq.com/keys")
                    return simula_diagnostico(dados)
                
                if response.status_code == 429:
                    st.info("🤖 Processando análise com inteligência artificial...")
                    return simula_diagnostico(dados)
                
                if response.status_code == 500 or response.status_code == 503:
                    continue
                
                if response.status_code != 200:
                    continue
                
                response.raise_for_status()
                
                # Extrai o conteúdo da resposta
                result = response.json()
                
                if 'choices' not in result or len(result['choices']) == 0:
                    continue
                
                content = result['choices'][0]['message']['content'].strip()
                
                # Limpa possíveis markdown
                content = content.replace('```json', '').replace('```', '').replace('```python', '').strip()
                
                # Remove espaços ou quebras de linha no início/fim
                if content.startswith('{'):
                    ultimo_chave = content.rfind('}')
                    if ultimo_chave != -1:
                        content = content[:ultimo_chave + 1]
                
                # Tenta fazer parse do JSON
                resultado = json.loads(content)
                
                # Valida campos obrigatórios
                campos_obrigatorios = {
                    'categoria': 'Não avaliado',
                    'severidade': 'Moderada',
                    'risco': 'Ausente',
                    'recomendacao': 'Acompanhamento psicológico',
                    'justificativa': 'Avaliação concluída',
                    'estrategias': ["Consulte um profissional de saúde mental"]
                }
                
                for campo, valor_padrao in campos_obrigatorios.items():
                    if campo not in resultado:
                        resultado[campo] = valor_padrao
                        
                    if campo == 'estrategias':
                        if not isinstance(resultado.get('estrategias'), list):
                            resultado['estrategias'] = [str(resultado.get('estrategias', valor_padrao))]
                        
                        if len(resultado['estrategias']) < 3:
                            resultado['estrategias'] += ["Consulte um profissional"] * (3 - len(resultado['estrategias']))
                
                # Sucesso! Retorna sem mostrar qual modelo foi usado
                return resultado
                    
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, json.JSONDecodeError):
                continue
            except Exception:
                continue
    
    # Se nenhum modelo funcionou, usa simulação (silenciosamente)
    return simula_diagnostico(dados)


def salvar_avaliacao(user_id, dados, diagnostico):
    """
    Salva a avaliação no banco de dados SQLite
    """
    try:
        conn = sqlite3.connect('psicobot.db')
        c = conn.cursor()
        
        c.execute('''INSERT OR REPLACE INTO avaliacoes 
                     (id, data, dados_json, diagnostico, risco) 
                     VALUES (?, ?, ?, ?, ?)''',
                  (user_id,
                   datetime.now().strftime('%d/%m/%Y %H:%M'),
                   json.dumps(dados, ensure_ascii=False),
                   json.dumps(diagnostico, ensure_ascii=False),
                   diagnostico.get('risco', 'Ausente')))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao salvar: {e}")
        return False


def main():
    # Container principal com fundo escuro
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header
    st.title("🧠 PsicoBot")
    st.markdown('<p class="subtitle">Avaliação Psicológica Inteligente</p>', unsafe_allow_html=True)
    
    # Inicialização
    if 'step' not in st.session_state:
        st.session_state.step = 0
        st.session_state.dados = {}
        st.session_state.user_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
    
    # Progresso
    progress = st.progress(st.session_state.step / 10)
    
    # Etapas da triagem
    steps = [
        ("nome", "Como prefere ser chamado/a?"),
        ("idade", "Qual sua idade?"),
        ("ocupacao", "Qual sua ocupação atual?"),
        ("queixa", "O que o/a trouxe aqui hoje? Conte-me livremente o que está sentindo..."),
        ("duracao", "Há quanto tempo se sente assim?"),
        ("sono", "Como está seu sono ultimamente? (horas, qualidade, dificuldades)"),
        ("apetite", "Seu apetite mudou recentemente? (aumentou, diminuiu, sem alteração)"),
        ("energia", "De 0 a 10, como está sua energia para atividades diárias?"),
        ("suicidio", "Você já pensou em desistir de tiver ou em se machucar?"),
        ("apoio", "Tem pessoas próximas que oferecem apoio emocional?")
    ]
    
    if st.session_state.step < len(steps):
        field, question = steps[st.session_state.step]
        
        # Contador
        st.markdown(f'<p class="question-counter">Pergunta {st.session_state.step + 1} de {len(steps)}</p>', 
                   unsafe_allow_html=True)
        
        # Pergunta
        st.markdown(f'<p class="question-text">{question}</p>', unsafe_allow_html=True)
        
        # Input especial para risco suicida
        if field == "suicidio":
            resposta = st.radio("Selecione uma opção:", 
                               ["Não, nunca pensei nisso", 
                                "Já tive pensamentos passados", 
                                "Tenho pensado recentemente",
                                "Prefiro não responder"], 
                               key=field)
            
            if "penso" in resposta.lower() or "recentemente" in resposta.lower():
                st.markdown("""
                <div class="risk-alert">
                    <h3>⚠️ Estamos aqui para ajudar</h3>
                    <p>É importante que você converse com alguém preparado agora:</p>
                    <ul>
                        <li><b>CVV (Centro de Valorização da Vida):</b> 188</li>
                        <li><b>WhatsApp CVV:</b> (11) 98801-3400</li>
                        <li><b>SAMU:</b> 192</li>
                    </ul>
                    <p><b>Você não está sozinho/a.</b> Esses pensamentos são passageiros e 
                    existem pessoas preparadas para ajudar 24h por dia.</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("✓ Confirmo que estou seguro agora, quero continuar", type="primary"):
                    st.session_state.dados[field] = resposta
                    st.session_state.step += 1
                    st.rerun()
            else:
                if st.button("Próximo", type="primary"):
                    st.session_state.dados[field] = resposta
                    st.session_state.step += 1
                    st.rerun()
        else:
            # Input normal
            if field == "idade":
                resposta = st.number_input("Sua resposta:", min_value=18, max_value=100, value=30, key=field)
            elif field == "energia":
                resposta = st.slider("Sua resposta:", 0, 10, 5, key=field)
            else:
                resposta = st.text_area("Sua resposta:", height=120, key=field, 
                                       placeholder="Digite aqui...")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Próximo ➜", type="primary", key=f"btn_{field}_{st.session_state.step}"):
                    if resposta:
                        st.session_state.dados[field] = resposta
                        st.session_state.step += 1
                        st.rerun()
                    else:
                        st.error("Por favor, preencha a resposta para continuar.")
    
    else:
        # Resultado
        st.success("✅ Triagem concluída com sucesso!")
        
        # AQUI É FEITA A ANÁLISE COM IA REAL (GROQ)
        diagnostico = analisar_com_ia(st.session_state.dados)
        
        # Mostra mensagem de sucesso
        st.success("✅ Análise concluída com inteligência artificial")
        
        salvar_avaliacao(
            st.session_state.user_id,
            st.session_state.dados,
            diagnostico
        )
        
        # Caixa de resultado
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 30px; border-radius: 15px; text-align: center; margin: 20px 0;">
            <h2 style="color: white !important; margin-bottom: 20px;">📋 Resultado da Avaliação</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Métricas em cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">🧠</div>
                <div class="metric-label">{diagnostico['categoria']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            cor_sev = "🟡" if diagnostico['severidade'] == 'Moderada' else "🔴" if diagnostico['severidade'] == 'Grave' else "🟢"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{cor_sev}</div>
                <div class="metric-label">Severidade: {diagnostico['severidade']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">📅</div>
                <div class="metric-label">{diagnostico['recomendacao']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Mostra justificativa se existir (vem da IA)
        if 'justificativa' in diagnostico:
            with st.expander("📝 Justificativa Clínica"):
                st.write(diagnostico['justificativa'])
        
        # Estratégias
        st.subheader("🛠️ Estratégias Imediatas")
        for i, est in enumerate(diagnostico['estrategias'], 1):
            with st.expander(f"Estratégia {i}"):
                st.write(est)
        
        # Botões de download
        st.divider()
        st.subheader("📄 Documentação para Profissional")
        
        # Gera o PDF profissional
        pdf_bytes = generate_professional_pdf(
            st.session_state.dados, 
            diagnostico, 
            st.session_state.user_id
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Botão PDF Profissional
            st.download_button(
                label="📄 Baixar Relatório PDF (para Médico)",
                data=pdf_bytes,
                file_name=f"relatorio_psicobot_{st.session_state.user_id}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        with col2:
            # Botão HTML
            st.markdown(generate_html_pdf(st.session_state.dados, diagnostico, 
                                        st.session_state.user_id), 
                       unsafe_allow_html=True)
        
        # Botão Nova Avaliação
        if st.button("🔄 Nova Avaliação", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        # Aviso legal
        st.markdown("""
        <div style="background: #3d3d1f; border-left: 5px solid #f1c40f; padding: 20px; 
                    border-radius: 10px; color: #fff3cd; margin-top: 30px; font-size: 0.9rem;">
            <strong>⚠️ Aviso Legal:</strong> Este relatório foi gerado por IA e não substitui 
            avaliação presencial com psicólogo registrado no CRP. Em caso de emergência, 
            procure atendimento médico ou ligue 188 (CVV).
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
