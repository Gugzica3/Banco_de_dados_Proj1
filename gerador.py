from faker import Faker
import random
from math import ceil

fake = Faker('pt_BR')
random.seed(42)

# CONFIGURAÇÕES
TOTAL_PROFESSORES = 20
TOTAL_ALUNOS = 60
TOTAL_PESSOAS = TOTAL_PROFESSORES + TOTAL_ALUNOS
TOTAL_DEPTOS = 4
TOTAL_CURSOS = 4
# Usaremos 4 disciplinas fixas, conforme solicitado
TOTAL_DISCIPLINAS = 4  
TOTAL_TURMAS = 12
TOTAL_AVALIACOES = 8  # Número reduzido para manter a saída razoável
ALUNOS_POR_GRUPO = 5
TOTAL_GRUPOS_TCC = TOTAL_ALUNOS // ALUNOS_POR_GRUPO

# Nomes fixos conforme especificado:
DEPTOS_FIXOS = ["Matemática", "Computador", "Engenharia", "Fisica"]
CURSOS_FIXOS = ["Ciencias da Computação", "Ciencias de dados", "Inteligencia Artificial", "Engenharia de Reprodução"]
DISCIPLINAS_FIXAS = ["Calculo", "deus é acreditar", "Banco de dados", "Python"]

# Gerar CPFs únicos para todas as pessoas
pessoas_cpfs = [fake.unique.cpf() for _ in range(TOTAL_PESSOAS)]
professores_cpfs = pessoas_cpfs[:TOTAL_PROFESSORES]
alunos_cpfs = pessoas_cpfs[TOTAL_PROFESSORES:]

# Gera o SQL de inserção para cada tabela

### 1. Tabela Pessoa
print("-- PESSOA")
for cpf in pessoas_cpfs:
    print(f"INSERT INTO Pessoa (cpf, nome) VALUES ('{cpf}', '{fake.name()}');")

### 2. Tabela Depto (usando nomes fixos)
print("\n-- DEPTO")
for i in range(1, TOTAL_DEPTOS + 1):
    nome_depto = DEPTOS_FIXOS[i - 1]
    # A coluna chefe_depto ficará NULL para início; será atualizado depois.
    print(f"INSERT INTO Depto (id_depto, nome, chefe_depto) VALUES ({i}, '{nome_depto}', NULL);")

### 3. Tabela Professor
print("\n-- PROFESSOR")
for i, cpf in enumerate(professores_cpfs, start=1):
    # Distribuir os professores de forma cíclica nos departamentos
    id_depto = ((i - 1) % TOTAL_DEPTOS) + 1
    print(f"INSERT INTO Professor (id_professor, cpf, id_depto) VALUES ({i}, '{cpf}', {id_depto});")

### 4. Atualização dos Chefes de Depto
print("\n-- CHEFES DE DEPTO (UPDATE)")
for i in range(1, TOTAL_DEPTOS + 1):
    chefe_id = i  # Define o professor com id = i como chefe do depto i
    print(f"UPDATE Depto SET chefe_depto = {chefe_id} WHERE id_depto = {i};")

### 5. Tabela Curso (usando nomes fixos)
print("\n-- CURSO")
for i in range(1, TOTAL_CURSOS + 1):
    nome_curso = CURSOS_FIXOS[i - 1]
    id_depto = ((i - 1) % TOTAL_DEPTOS) + 1
    # Coordenador: usa professor com id = i (ajuste se preferir)
    coord_id = i
    print(f"INSERT INTO Curso (id_curso, nome, id_depto, coordenador_curso) VALUES ({i}, '{nome_curso}', {id_depto}, {coord_id});")

### 6. Tabela Disciplina (usando nomes fixos)
print("\n-- DISCIPLINA")
for i in range(1, TOTAL_DISCIPLINAS + 1):
    nome_disciplina = DISCIPLINAS_FIXAS[i - 1]
    id_depto = ((i - 1) % TOTAL_DEPTOS) + 1
    # Coordenador da disciplina: professor com id = i (pode ser ajustado)
    coord_id = i
    print(f"INSERT INTO Disciplina (id_disciplina, nome, id_depto, coordenador_disciplina) VALUES ({i}, '{nome_disciplina}', {id_depto}, {coord_id});")

### 7. Tabela Turma
print("\n-- TURMA")
for i in range(1, TOTAL_TURMAS + 1):
    periodo = random.randint(1, 8)
    ano = random.choice([2022, 2023, 2024])
    semestre = random.choice(['1', '2'])
    id_disciplina = ((i - 1) % TOTAL_DISCIPLINAS) + 1
    id_curso = ((i - 1) % TOTAL_CURSOS) + 1
    print(f"INSERT INTO Turma (id_turma, periodo, ano, semestre_ano, id_disciplina, id_curso) VALUES ({i}, {periodo}, {ano}, '{semestre}', {id_disciplina}, {id_curso});")

### 8. Tabela Aluno
print("\n-- ALUNO")
for i, cpf in enumerate(alunos_cpfs, start=1):
    id_curso = ((i - 1) % TOTAL_CURSOS) + 1
    id_turma = ((i - 1) % TOTAL_TURMAS) + 1
    print(f"INSERT INTO Aluno (id_aluno, cpf, id_curso, id_turma) VALUES ({i}, '{cpf}', {id_curso}, {id_turma});")

### 9. Tabela Grupo_TCC e TCC
print("\n-- GRUPO_TCC e TCC")
for grupo_id in range(1, TOTAL_GRUPOS_TCC + 1):
    alunos_grupo = [((grupo_id - 1) * ALUNOS_POR_GRUPO) + j + 1 for j in range(ALUNOS_POR_GRUPO)]
    print(f"INSERT INTO Grupo_TCC (id_grupo, aluno1, aluno2, aluno3, aluno4, aluno5) VALUES ({grupo_id}, {alunos_grupo[0]}, {alunos_grupo[1]}, {alunos_grupo[2]}, {alunos_grupo[3]}, {alunos_grupo[4]});")
    orientador = random.randint(1, TOTAL_PROFESSORES)
    titulo = fake.sentence(nb_words=5)
    print(f"INSERT INTO TCC (orientador, titulo, id_grupo) VALUES ({orientador}, '{titulo}', {grupo_id});")

### 10. Tabela Aula
print("\n-- AULA")
for i in range(1, TOTAL_TURMAS + 1):
    prof = ((i - 1) % TOTAL_PROFESSORES) + 1
    print(f"INSERT INTO Aula (id_aula, id_turma, professor_aula) VALUES ({i}, {i}, {prof});")

### 11. Tabelas Avaliacao, Nota e HistoricoEscolar
print("\n-- AVALIACAO / NOTA / HISTORICO_ESCOLAR")
avaliacao_id = 1
nota_id = 1
for disciplina_id in range(1, TOTAL_DISCIPLINAS + 1):
    nota_valor = random.randint(5, 10)
    print(f"INSERT INTO Avaliacao (id_avaliacao, nota, id_disciplina) VALUES ({avaliacao_id}, {nota_valor}, {disciplina_id});")
    for aluno_id in range(1, TOTAL_ALUNOS + 1):
        id_turma = ((aluno_id - 1) % TOTAL_TURMAS) + 1
        print(f"INSERT INTO Nota (id_nota, id_aluno, id_turma, concluido, id_avaliacao) VALUES ({nota_id}, {aluno_id}, {id_turma}, TRUE, {avaliacao_id});")
        print(f"INSERT INTO HistoricoEscolar (id_aluno, id_turma, id_nota) VALUES ({aluno_id}, {id_turma}, {nota_id});")
        nota_id += 1
    avaliacao_id += 1
