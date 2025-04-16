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

1. **Clone o repositório**  
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd banco-de-dados-universidade
   ```

2. **Crie o banco e execute o DDL**  
   - Instale o PostgreSQL (≥ 12) e crie um database chamado `postgres` (ou ajuste no script).  
   - Rode:
     ```bash
     psql -U <seu_usuario> -d postgres -f ddl.sql
     ```

3. **Popule com dados fictícios**  
   - Instale dependências Python:
     ```bash
     pip install psycopg2-binary Faker
     ```
   - Execute o gerador de dados:
     ```bash
     python popula_tudo.py
     ```

4. **Valide a consistência**  
   - Caso exista, rode:
     ```bash
     python valida_dados.py
     ```

5. **Execute as queries**  
   - Abra e rode `queries.sql` no seu cliente favorito (psql, DBeaver, PgAdmin).

---

## Modelo Relacional (MR)
![Modelo Relacional](https://github.com/user-attachments/assets/22456bf6-4f9c-46b0-85c9-f50a2df9ed00)

---

## Modelo Entidade‑Relacionamento (MER)
![Modelo Entidade-Relacionamento](https://github.com/user-attachments/assets/e7232d11-df87-4023-a5e7-099c65db1f7d)
