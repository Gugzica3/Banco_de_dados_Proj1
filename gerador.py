from faker import Faker
import random
from math import ceil

fake = Faker('pt_BR')
random.seed(42)

# CONFIGURAÇÕES
TOTAL_PROFESSORES = 20
TOTAL_ALUNOS = 60
TOTAL_DEPARTAMENTOS = 5
TOTAL_CURSOS = 4
TOTAL_DISCIPLINAS = 20
TOTAL_TURMAS = 10
TOTAL_AVALIACOES = 30
GRUPO_TAMANHO = 5
TOTAL_GRUPOS = ceil(TOTAL_ALUNOS / GRUPO_TAMANHO)

# DADOS
output = []

# CPFs únicos
cpfs = [fake.unique.cpf() for _ in range(TOTAL_PROFESSORES + TOTAL_ALUNOS)]
prof_cpfs = cpfs[:TOTAL_PROFESSORES]
alu_cpfs = cpfs[TOTAL_PROFESSORES:]

# PESSOAS
output.append("-- PESSOAS")
for cpf in cpfs:
    nome = fake.name()
    output.append(f"INSERT INTO Pessoa (cpf, nome) VALUES ('{cpf}', '{nome}');")

# DEPARTAMENTOS
output.append("\n-- DEPARTAMENTOS")
for i in range(1, TOTAL_DEPARTAMENTOS + 1):
    nome = f"Departamento {fake.word().capitalize()}"
    output.append(f"INSERT INTO Depto (id_depto, nome, chefe_depto) VALUES ({i}, '{nome}', NULL);")

# PROFESSORES
output.append("\n-- PROFESSORES")
for i, cpf in enumerate(prof_cpfs, start=1):
    id_depto = ((i - 1) % TOTAL_DEPARTAMENTOS) + 1
    output.append(f"INSERT INTO Professor (id_professor, cpf, id_depto) VALUES ({i}, '{cpf}', {id_depto});")

# DEFINIR CHEFES DE DEPARTAMENTO
output.append("\n-- CHEFES DE DEPARTAMENTO")
for i in range(1, TOTAL_DEPARTAMENTOS + 1):
    output.append(f"UPDATE Depto SET chefe_depto = {i} WHERE id_depto = {i};")

# CURSOS
output.append("\n-- CURSOS")
for i in range(1, TOTAL_CURSOS + 1):
    nome = f"Curso de {fake.job().split()[0]}"
    id_depto = ((i - 1) % TOTAL_DEPARTAMENTOS) + 1
    coordenador = ((i * 2 - 1) % TOTAL_PROFESSORES) + 1
    output.append(f"INSERT INTO Curso (id_curso, nome, id_depto, coordenador_curso) VALUES ({i}, '{nome}', {id_depto}, {coordenador});")

# DISCIPLINAS
output.append("\n-- DISCIPLINAS")
for i in range(1, TOTAL_DISCIPLINAS + 1):
    nome = f"Disciplina {fake.word().capitalize()}"
    id_depto = ((i - 1) % TOTAL_DEPARTAMENTOS) + 1
    coordenador = ((i * 3 - 1) % TOTAL_PROFESSORES) + 1
    output.append(f"INSERT INTO Disciplina (id_disciplina, nome, id_depto, coordenador_disciplina) VALUES ({i}, '{nome}', {id_depto}, {coordenador});")

# TURMAS
output.append("\n-- TURMAS")
for i in range(1, TOTAL_TURMAS + 1):
    periodo = random.randint(1, 8)
    ano = random.choice([2022, 2023, 2024])
    semestre = random.choice(['1', '2'])
    id_disc = ((i - 1) % TOTAL_DISCIPLINAS) + 1
    id_curso = ((i - 1) % TOTAL_CURSOS) + 1
    output.append(f"INSERT INTO Turma (id_turma, periodo, ano, semestre_ano, id_disciplina, id_curso) VALUES ({i}, {periodo}, {ano}, '{semestre}', {id_disc}, {id_curso});")

# ALUNOS
output.append("\n-- ALUNOS")
for i, cpf in enumerate(alu_cpfs, start=1):
    id_curso = ((i - 1) % TOTAL_CURSOS) + 1
    id_turma = ((i - 1) % TOTAL_TURMAS) + 1
    output.append(f"INSERT INTO Aluno (id_aluno, cpf, id_curso, id_turma) VALUES ({i}, '{cpf}', {id_curso}, {id_turma});")

# AULAS
output.append("\n-- AULAS")
for i in range(1, TOTAL_TURMAS + 1):
    professor = ((i - 1) % TOTAL_PROFESSORES) + 1
    output.append(f"INSERT INTO Aula (id_aula, id_turma, professor_aula) VALUES ({i}, {i}, {professor});")

# AVALIAÇÕES
output.append("\n-- AVALIAÇÕES")
for i in range(1, TOTAL_AVALIACOES + 1):
    nota = random.randint(1, 10)
    id_disc = ((i - 1) % TOTAL_DISCIPLINAS) + 1
    output.append(f"INSERT INTO Avaliacao (id_avaliacao, nota, id_disciplina) VALUES ({i}, {nota}, {id_disc});")

# NOTAS e HISTÓRICO
output.append("\n-- NOTAS E HISTÓRICO")
nota_id = 1
for id_aluno in range(1, TOTAL_ALUNOS + 1):
    for _ in range(3):
        id_turma = ((id_aluno + _) % TOTAL_TURMAS) + 1
        id_aval = ((id_aluno + _) % TOTAL_AVALIACOES) + 1
        output.append(f"INSERT INTO Nota (id_nota, id_aluno, id_turma, concluido, id_avaliacao) VALUES ({nota_id}, {id_aluno}, {id_turma}, TRUE, {id_aval});")
        output.append(f"INSERT INTO HistoricoEscolar (id_aluno, id_turma, id_nota) VALUES ({id_aluno}, {id_turma}, {nota_id});")
        nota_id += 1

# GRUPOS DE TCC
output.append("\n-- GRUPOS DE TCC")
aluno_id = 1
for grupo_id in range(1, TOTAL_GRUPOS + 1):
    alunos_grupo = []
    for _ in range(GRUPO_TAMANHO):
        if aluno_id <= TOTAL_ALUNOS:
            alunos_grupo.append(aluno_id)
            aluno_id += 1
        else:
            alunos_grupo.append("NULL")
    while len(alunos_grupo) < 5:
        alunos_grupo.append("NULL")
    output.append(f"INSERT INTO Grupo_TCC (id_grupo, aluno1, aluno2, aluno3, aluno4, aluno5) "
                  f"VALUES ({grupo_id}, {alunos_grupo[0]}, {alunos_grupo[1]}, "
                  f"{alunos_grupo[2]}, {alunos_grupo[3]}, {alunos_grupo[4]});")

# TCCs
output.append("\n-- TCCs")
for grupo_id in range(1, TOTAL_GRUPOS + 1):
    orientador_id = ((grupo_id - 1) % TOTAL_PROFESSORES) + 1
    output.append(f"INSERT INTO TCC (orientador, titulo, id_grupo) "
                  f"VALUES ({orientador_id}, 'TCC do Grupo {grupo_id}', {grupo_id});")

# Exportar para arquivo SQL
with open("dados_grandes_gerados.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("Arquivo dados_grandes_gerados.sql gerado com sucesso.")
