<div align="center">

# 🧠 PsicobotAI
### Assistente com IA para conversação, prompts e automações (com opção de RAG/base de conhecimento)

<a href="#pt-br"><b>🇧🇷 Português</b></a> • <a href="#en-us"><b>🇺🇸 English</b></a>

<br/>

<img src="https://img.shields.io/badge/Status-Em%20Evolu%C3%A7%C3%A3o-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/Foco-IA%20%7C%20Chatbot%20%7C%20Automa%C3%A7%C3%A3o-7c3aed?style=for-the-badge" />
<img src="https://img.shields.io/badge/Build-Manual-lightgrey?style=for-the-badge" />

<br/>

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/LLM-111827?style=for-the-badge" />
<img src="https://img.shields.io/badge/RAG-111827?style=for-the-badge" />
<img src="https://img.shields.io/badge/API%20Ready-0052CC?style=for-the-badge" />

<br/>

<img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" />
<a href="https://github.com/OrlandoCosta1974/psicobotAI">
  <img src="https://img.shields.io/badge/GitHub-Reposit%C3%B3rio-181717?style=for-the-badge&logo=github&logoColor=white" />
</a>

</div>

---

## 📌 Sumário | Table of Contents
- <a href="#pt-br">🇧🇷 Português</a>
  - <a href="#-visao-geral">Visão Geral</a>
  - <a href="#-objetivo-1-frase">Objetivo (1 frase)</a>
  - <a href="#-funcionalidades">Funcionalidades</a>
  - <a href="#-como-rodar-localmente">Como rodar localmente</a>
  - <a href="#-configuracao-env">Configuração (.env)</a>
  - <a href="#-modo-rag-opcional">Modo RAG (opcional)</a>
  - <a href="#-boas-praticas-de-seguranca">Boas práticas de segurança</a>
  - <a href="#-roadmap">Roadmap</a>
  - <a href="#-contribuicao">Contribuição</a>
- <a href="#en-us">🇺🇸 English</a>

---

<a id="pt-br"></a>

# 🇧🇷 Português

## 🔎 Visão Geral
O **PsicobotAI** é um assistente com IA focado em **experimentos de conversação**, **engenharia de prompts** e **automações**, podendo evoluir para um modelo com **base de conhecimento (RAG)**.

> ⚠️ **Aviso importante:** este projeto é educacional/experimental e **não substitui atendimento profissional** médico/psicológico.

## 🎯 Objetivo (1 frase)
Criar um assistente com IA para testar conversação, prompts e automações voltadas a suporte e orientação ao usuário, com possibilidade de RAG.

---

## ✨ Funcionalidades

### ✅ Núcleo (base)
- 🗣️ Chat com persona/configuração
- 🧩 Prompts organizados por objetivo
- 🧠 Contexto de sessão (memória curta)
- 📝 Logs e histórico (opcional)

### 🧠 IA/LLM (integrações possíveis)
- 🔌 Integração com **LLM local** (LM Studio / OpenAI-compatible)
- ☁️ Integração com **LLM online** (quando aplicável)
- 🧰 Configuração por `.env` (provider, url, modelo)

### 📚 RAG (opcional)
- 📄 Upload de documentos (PDF/TXT/MD) *(planejado)*
- 🔎 Busca semântica + respostas com contexto
- 🧱 Vetorização (ex.: FAISS/Chroma) *(planejado)*

---

## 🗂️ Estrutura sugerida do projeto

```text
psicobotAI/
├─ src/
│  ├─ main.py
│  ├─ config.py
│  ├─ core/
│  │  ├─ chat.py
│  │  ├─ prompts.py
│  │  └─ memory.py
│  ├─ providers/        # integrações LLM
│  ├─ safety/           # regras e avisos
│  ├─ rag/              # opcional
│  └─ utils/
├─ data/
│  ├─ logs/
│  └─ knowledge_base/   # docs para RAG
├─ requirements.txt
├─ .env.example
└─ README.md
