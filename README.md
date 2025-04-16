# Projeto de Banco de Dados para Universidade

## Integrantes
- **Gustavo Bertoluzzi Cardoso** – RA 22.123.016-2  
- **Isabella Vieira Silva Rosseto** – RA 22.222.036-0  

---

## Descrição do Projeto
Este repositório contém a implementação de um sistema de banco de dados relacional para uma universidade. O objetivo é:

- Modelar entidades como **Pessoas** (alunos e professores), **Departamentos**, **Cursos** e **Disciplinas**.  
- Registrar **Aulas** ministradas, **Histórico Escolar** (notas, reprovações e aprovações) e **Grupos de TCC** com seus orientadores.  
- Garantir normalização até a 3FN e estruturar consultas SQL para análises acadêmicas.

---

## Como executar o Projeto

1. **Criar um banco no Supabase**  
   - Acesse [Supabase](https://supabase.com/) e crie um novo projeto.  
   - No painel do projeto, acesse **Database → SQL Editor**.

2. **Executar o script DDL**  
   - Encontre o arquivo `criar.sql` neste repositório.  
   - No SQL Editor do Supabase, copie e cole todo o conteúdo de `criar.sql` e execute para criar as tabelas.

3. **Popular com dados fictícios**  
   - Abra o arquivo `gerador.py`.  
   - Ajuste a variável `PASSWORD` para a senha do seu database Supabase.  
   - No terminal, instale as dependências (se ainda não estiverem instaladas):
     ```bash
     pip install psycopg2-binary Faker
     ```
   - Execute:
     ```bash
     python gerador.py
     ```
   - Isso irá conectar-se ao seu banco Supabase e inserir dados fictícios em todas as tabelas.

4. **Rodar as consultas SQL**  
   - No mesmo SQL Editor, abra o arquivo `queries.sql` e execute cada query para validar as respostas.

---

## Modelo Relacional (MR)
![Modelo Relacional](https://github.com/user-attachments/assets/22456bf6-4f9c-46b0-85c9-f50a2df9ed00)

---

## Modelo Entidade‑Relacionamento (MER)
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

  %% Atributos de Pessoa
  p_cpf((cpf))
  p_nome((nome))
  Pessoa --> p_cpf
  Pessoa --> p_nome

  %% Aluno
  a_id((id_aluno))
  a_sem(((semestre atual)))
  Aluno --> a_id
  Aluno --> a_sem
  Pessoa --> Aluno

  %% Professor
  pr_id((id_professor))
  Professor --> pr_id
  Pessoa --> Professor

  %% Depto
  d_id((id_depto))
  d_nome((nome))
  Depto --> d_id
  Depto --> d_nome

  %% Curso
  c_id((id_curso))
  Curso --> c_id
  %% Disciplina
  dis_id((id_disciplina))
  Disciplina --> dis_id

  %% Turma
  t_id((id_turma))
  Turma --> t_id

  %% Relações (losangos)
  FazParteAlunoCurso{'faz parte'}
  Aluno --> FazParteAlunoCurso
  FazParteAlunoCurso --> Curso

  MatrizCurricular{'matriz curricular'}
  Curso --> MatrizCurricular
  MatrizCurricular --> Disciplina

  HistoricoAluno{'histórico'\}
  Aluno --> HistoricoAluno
  HistoricoAluno --> Turma
  Turma --> Disciplina

  HistoricoProfessor{'histórico''}
  Professor --> HistoricoProfessor
  HistoricoProfessor --> Disciplina

  Chefia{'chefia'}
  Professor --> Chefia
  Chefia --> Depto

  CoordenacaoCurso{'coordena'}
  Professor --> CoordenacaoCurso
  CoordenacaoCurso --> Curso

  CoordenacaoDisc{'coordena'}
  Professor --> CoordenacaoDisc
  CoordenacaoDisc --> Disciplina

  Orientacao{'orienta'}
  Professor --> Orientacao
  Orientacao --> TCC

  TccAluno{'faz parte TCC'}
  Aluno --> TccAluno
  TccAluno --> TCC

  AulaMinistrada{'ministra'}
  Professor --> AulaMinistrada
  AulaMinistrada --> Turma

  %% Conectores adicionais
  GrupoTCC --> TCC

  NotaRel{'gera nota'}
  Avaliacao --> NotaRel
  NotaRel --> Nota
  Nota --> Historico
```

