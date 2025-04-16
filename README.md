<!-- README.md gerado automaticamente  -->
<p align="center">
  <img src="https://img.shields.io/badge/SQL-PostgreSQL-blue?logo=postgresql&logoColor=white" alt="PostgreSQL Badge"/>
  <img src="https://img.shields.io/badge/Python-3.10+-yellow?logo=python&logoColor=white" alt="Python Badge"/>
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License Badge"/>
</p>

<h1 align="center">🎓 Banco de Dados Universitário</h1>
<p align="center">Um projeto acadêmico completo que modela todo o ecossistema de uma universidade – de alunos a TCCs – usando <strong>PostgreSQL</strong> e <strong>Python</strong>.</p>

---

## 👥 Integrantes
| Nome | RA |
|------|----|
| **Gustavo Bertoluzzi Cardoso** | 22.123.016-2 |
| **Isabella Vieira Silva Rosseto** | 22.222.036-0 |

---

## 🗺️ Visão Geral
> **Objetivo:** Criar um sistema relacional totalmente normalizado (3FN) capaz de gerenciar:
> 
> - **Pessoas** (alunos & professores)  
> - **Departamentos, Cursos & Disciplinas**  
> - **Aulas**, **Histórico Escolar** e **Matriz Curricular**  
> - **Grupos & Projetos de TCC**  

O projeto inclui **DDL**, **scripts de popularização**, **validações** e **consultas SQL** que respondem às perguntas de negócio exigidas.

---

## 🧭 Índice
1. [Pré‑requisitos](#pré‑requisitos)
2. [Configuração Rápida](#configuração-rápida)
3. [Scripts Essenciais](#scripts-essenciais)
4. [Modelos](#modelos)
5. [Consultas SQL](#consultas-sql)
6. [Licença](#licença)

---

## 📦 Pré‑requisitos
- Conta gratuita no **Supabase**  
- **Python 3.10+**  
- **pip** (ou **pipx**)  
- Acesso ao **SQL Editor** do Supabase  

---

## ⚡ Configuração Rápida
<details>
<summary><strong>Passo‑a‑passo detalhado (clique para expandir)</strong></summary>

1. ### 🚀 Criar banco no Supabase  
   - Acesse <https://supabase.com> → **New Project** → defina nome, senha e região.

2. ### 🗄️ Executar DDL  
   - No dashboard → **Database ▸ SQL Editor** → crie nova query.  
   - Cole o conteúdo de <kbd>criar.sql</kbd> e clique <kbd>Run</kbd>.

3. ### 🐍 Popular com dados fictícios  
   - Abra <kbd>gerador.py</kbd> conecte com o seu banco de dados mudando a senha e outros dados.

4. ### 🔍 Rodar consultas  
   - Abra <kbd>queries.sql</kbd> no SQL Editor do Supabase ou no seu cliente favorito (DBeaver, psql etc.)  
   - Execute e observe os resultados.  

</details>

---

## 🛠️ Scripts Essenciais
| Arquivo | Descrição |
|---------|-----------|
| `criar.sql` | Criação de todas as tabelas, chaves e restrições. |
| `gerador.py` | Gera CPFs, nomes, turmas, notas, TCCs e populariza o banco. |
| `queries.sql` | Contém as 5 queries obrigatórias + 10 queries extras. |
| `valida_dados.sql` | Checa consistência referencial & contagens esperadas. |

---

## 🗂️ Modelos

### Modelo Relacional (MR)
![MR](https://github.com/user-attachments/assets/22456bf6-4f9c-46b0-85c9-f50a2df9ed00)

### Modelo Entidade‑Relacionamento (MER)
```mermaid
flowchart LR
  %% Entidades
  Pessoa[Pessoa]
  Aluno[Aluno]
  Professor[Professor]
  Depto[Departamento]
  Curso[Curso]
  Disciplina[Disciplina]
  Turma[Turma]
  Avaliacao['Avaliação']
  Nota[Nota]
  Historico['Histórico Escolar']
  Aula[Aula]
  GrupoTCC['Grupo TCC']
  TCC[TCC]

  %% Atributos e relacionamentos (resumidos para clareza)
  Pessoa -->|cpf| Aluno
  Pessoa -->|cpf| Professor
  Depto -->|1,N| Curso
  Depto -->|1,N| Disciplina
  Curso -->|1,N| Turma
  Disciplina -->|1,N| Turma
  Professor -->|1,N| Aula
  Turma -->|1,N| Aula
  Aluno -->|N,N| Turma
  Turma -->|1,N| Nota
  Nota -->|N,1| Avaliacao
  Professor -->|1,N| TCC
  Aluno -->|N,N| GrupoTCC
  GrupoTCC -->|1,1| TCC
```

---

## 📊 Consultas SQL
As queries obrigatórias e adicionais estão em `queries.sql´
---

## 📝 Licença
Este projeto utiliza a licença **MIT** – fique à vontade para estudar, modificar e distribuir. Divirta‑se! ✨
