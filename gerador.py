import random
from faker import Faker
import psycopg2

# ── CONFIGURAÇÕES DE CONEXÃO ─────────────────────────────────
USER     = "postgres.qapvlmvkhuatubqlewrs"
PASSWORD = "aaaaaaaaaa789798798ghjgkjhg"
HOST     = "aws-0-sa-east-1.pooler.supabase.com"
PORT     = "6543"
DBNAME   = "postgres"
SSLMODE  = "require"

# ── CONEXÃO AO BANCO ────────────────────────────────────────
conn = psycopg2.connect(
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    dbname=DBNAME,
    sslmode=SSLMODE
)
cur = conn.cursor()

# ── INSTÂNCIAS PARA GERAÇÃO ─────────────────────────────────
fake = Faker('pt_BR')
random.seed(42)

# ── PARÂMETROS ─────────────────────────────────────────────
TOTAL_PROFESSORES = 20
TOTAL_ALUNOS      = 60
TOTAL_DEPTOS      = 4
TOTAL_CURSOS      = 4
TOTAL_DISCIPLINAS = 4
ALUNOS_POR_GRUPO  = 5

DEPTOS_FIXOS      = ["Matematica", "Computador", "Engenharia", "Fisica"]
CURSOS_FIXOS      = ["Ciencia da Computacao","Ciencia de Dados",
                     "Inteligencia Artificial","Engenharia de Reproducao"]
DISCIPLINAS_FIXAS = ["Calculo","Filosofia","Banco de Dados","Python"]

# ── GERA CPFs E CRIA PESSOAS ───────────────────────────────
cpfs = [fake.unique.cpf() for _ in range(TOTAL_PROFESSORES + TOTAL_ALUNOS)]
for cpf in cpfs:
    cur.execute("INSERT INTO Pessoa(cpf,nome) VALUES(%s,%s)", (cpf, fake.name()))

# ── CRIA DEPARTAMENTOS ────────────────────────────────────
for i, nome in enumerate(DEPTOS_FIXOS, start=1):
    cur.execute("INSERT INTO Depto(id_depto,nome,chefe_depto) VALUES(%s,%s,NULL)", (i, nome))

# ── CRIA PROFESSORES ──────────────────────────────────────
for pid, cpf in enumerate(cpfs[:TOTAL_PROFESSORES], start=1):
    dept = ((pid - 1) % TOTAL_DEPTOS) + 1
    cur.execute("INSERT INTO Professor(id_professor,cpf,id_depto) VALUES(%s,%s,%s)", (pid, cpf, dept))

# ── DEFINE CHEFES DEPARTAMENTO ───────────────────────────
for i in range(1, TOTAL_DEPTOS + 1):
    cur.execute("UPDATE Depto SET chefe_depto=%s WHERE id_depto=%s", (i, i))

# ── CRIA CURSOS ───────────────────────────────────────────
for cid, nome in enumerate(CURSOS_FIXOS, start=1):
    dept = ((cid - 1) % TOTAL_DEPTOS) + 1
    cur.execute(
        "INSERT INTO Curso(id_curso,nome,id_depto,coordenador_curso) VALUES(%s,%s,%s,%s)",
        (cid, nome, dept, cid)
    )

# ── CRIA DISCIPLINAS ──────────────────────────────────────
for did, nome in enumerate(DISCIPLINAS_FIXAS, start=1):
    dept = ((did - 1) % TOTAL_DEPTOS) + 1
    cur.execute(
        "INSERT INTO Disciplina(id_disciplina,nome,id_depto,coordenador_disciplina) VALUES(%s,%s,%s,%s)",
        (did, nome, dept, did)
    )

# ── CRIA TURMAS 1º E 2º SEMESTRE ───────────────────────────
turmas = []
tid = 1
for curso in range(1, TOTAL_CURSOS + 1):
    for disc in range(1, TOTAL_DISCIPLINAS + 1):
        for sem in ['1', '2']:
            periodo = random.randint(1, 8)
            cur.execute(
                "INSERT INTO Turma(id_turma,periodo,ano,semestre_ano,id_disciplina,id_curso) "
                "VALUES(%s,%s,2023,%s,%s,%s)",
                (tid, periodo, sem, disc, curso)
            )
            turmas.append((tid, disc, sem, curso))
            tid += 1

# ── CRIA ALUNOS ───────────────────────────────────────────
for aid, cpf in enumerate(cpfs[TOTAL_PROFESSORES:], start=1):
    curso = ((aid - 1) % TOTAL_CURSOS) + 1
    sem1 = next(t[0] for t in turmas if t[1] == 1 and t[2] == '1' and t[3] == curso)
    cur.execute("INSERT INTO Aluno(id_aluno,cpf,id_curso,id_turma) VALUES(%s,%s,%s,%s)",
                (aid, cpf, curso, sem1))

# ── GRUPOS DE TCC E PROJETOS ─────────────────────────────
for gid in range(1, TOTAL_ALUNOS // ALUNOS_POR_GRUPO + 1):
    membros = [((gid - 1) * ALUNOS_POR_GRUPO) + j + 1 for j in range(ALUNOS_POR_GRUPO)]
    cur.execute(
        "INSERT INTO Grupo_TCC(id_grupo,aluno1,aluno2,aluno3,aluno4,aluno5) "
        "VALUES(%s,%s,%s,%s,%s,%s)",
        (gid, *membros)
    )
    orient = random.randint(1, TOTAL_PROFESSORES)
    titulo = fake.sentence(nb_words=5)
    cur.execute("INSERT INTO TCC(orientador,titulo,id_grupo) VALUES(%s,%s,%s)",
                (orient, titulo, gid))

# ── CRIA AULAS ───────────────────────────────────────────
for t in turmas:
    tid = t[0]
    prof = ((tid - 1) % TOTAL_PROFESSORES) + 1
    cur.execute("INSERT INTO Aula(id_aula,id_turma,professor_aula) VALUES(%s,%s,%s)",
                (tid, tid, prof))

# ── INSERE AVALIACOES, NOTAS E HISTORICO ─────────────────
aval_id = 1
nota_id = 1
def insere_nota(aluno, turma, disc, val):
    global aval_id, nota_id
    cur.execute("INSERT INTO Avaliacao(id_avaliacao,nota,id_disciplina) VALUES(%s,%s,%s)",
                (aval_id, val, disc))
    concluido = val >= 6
    cur.execute("INSERT INTO Nota(id_nota,id_aluno,id_turma,concluido,id_avaliacao) "
                "VALUES(%s,%s,%s,%s,%s)",
                (nota_id, aluno, turma, concluido, aval_id))
    cur.execute("INSERT INTO HistoricoEscolar(id_aluno,id_turma,id_nota) "
                "VALUES(%s,%s,%s)",
                (aluno, turma, nota_id))
    aval_id += 1
    nota_id += 1

# ── CASO GARANTIDO DE REPROVAÇÃO → APROVAÇÃO ──────────────
t1 = next(t[0] for t in turmas if t[1] == 1 and t[2] == '1')
t2 = next(t[0] for t in turmas if t[1] == 1 and t[2] == '2')
insere_nota(1, t1, 1, 4)
insere_nota(1, t2, 1, 8)

# ── NOTAS ALEATÓRIAS PARA TODOS ──────────────────────────
for aid in range(1, TOTAL_ALUNOS + 1):
    for disc in range(1, TOTAL_DISCIPLINAS + 1):
        if aid == 1 and disc == 1:
            continue
        curso = ((aid - 1) % TOTAL_CURSOS) + 1
        sem1_tid = next(t[0] for t in turmas if t[1] == disc and t[2] == '1' and t[3] == curso)
        val = random.randint(0, 10)
        insere_nota(aid, sem1_tid, disc, val)

# ── FINALIZA INSERÇÕES ───────────────────────────────────
conn.commit()
cur.close()
conn.close()
print("Dados inseridos com sucesso!")
