import random
from faker import Faker
import psycopg2

def main():
    USER     = "postgres.qapvlmvkhuatubqlewrs"
    PASSWORD = "aaaaaaaaaa789798798ghjgkjhg"
    HOST     = "aws-0-sa-east-1.pooler.supabase.com"
    PORT     = "6543"
    DBNAME   = "postgres"
    SSLMODE  = "require"  

    print(f"Conectando {USER}@{HOST}:{PORT}/{DBNAME} …")
    conn = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME,
        sslmode=SSLMODE
    )
    cur = conn.cursor()
    print("Conexão estabelecida!")
    fake = Faker('pt_BR')
    random.seed(42)

    
    TOTAL_PROFESSORES = 20
    TOTAL_ALUNOS      = 60
    TOTAL_DEPTOS      = 4
    TOTAL_CURSOS      = 4
    TOTAL_DISCIPLINAS = 4
    ALUNOS_POR_GRUPO  = 5

    DEPTOS_FIXOS      = ["Matematica", "Computador", "Engenharia", "Fisica"]
    CURSOS_FIXOS      = ["Ciencia da Computacao", "Ciencia de Dados",
                         "Inteligencia Artificial", "Engenharia de Reproducao"]
    DISCIPLINAS_FIXAS = ["Calculo", "Filosofia", "Banco de Dados", "Python"]

    # ── GERA CPFs ────────────────────────────────────────────────
    pessoas_cpfs     = [fake.unique.cpf() for _ in range(TOTAL_PROFESSORES + TOTAL_ALUNOS)]
    professores_cpfs = pessoas_cpfs[:TOTAL_PROFESSORES]
    alunos_cpfs      = pessoas_cpfs[TOTAL_PROFESSORES:]

    # 1) Pessoa
    for cpf in pessoas_cpfs:
        cur.execute(
            "INSERT INTO Pessoa (cpf, nome) VALUES (%s, %s)",
            (cpf, fake.name())
        )

    # 2) Depto
    for i, nome in enumerate(DEPTOS_FIXOS, start=1):
        cur.execute(
            "INSERT INTO Depto (id_depto, nome, chefe_depto) VALUES (%s, %s, NULL)",
            (i, nome)
        )

    # 3) Professor
    for pid, cpf in enumerate(professores_cpfs, start=1):
        id_depto = ((pid - 1) % TOTAL_DEPTOS) + 1
        cur.execute(
            "INSERT INTO Professor (id_professor, cpf, id_depto) VALUES (%s, %s, %s)",
            (pid, cpf, id_depto)
        )

    # 4) Chefes de depto
    for i in range(1, TOTAL_DEPTOS + 1):
        cur.execute(
            "UPDATE Depto SET chefe_depto = %s WHERE id_depto = %s",
            (i, i)
        )

    # 5) Curso
    for cid, nome in enumerate(CURSOS_FIXOS, start=1):
        id_depto = ((cid - 1) % TOTAL_DEPTOS) + 1
        cur.execute(
            "INSERT INTO Curso (id_curso, nome, id_depto, coordenador_curso) VALUES (%s, %s, %s, %s)",
            (cid, nome, id_depto, cid)
        )

    # 6) Disciplina
    for did, nome in enumerate(DISCIPLINAS_FIXAS, start=1):
        id_depto = ((did - 1) % TOTAL_DEPTOS) + 1
        cur.execute(
            "INSERT INTO Disciplina (id_disciplina, nome, id_depto, coordenador_disciplina) VALUES (%s, %s, %s, %s)",
            (did, nome, id_depto, did)
        )

    # 7) Turma (1º e 2º semestre para cada curso+disciplina)
    turmas = []
    tid = 1
    for curso in range(1, TOTAL_CURSOS + 1):
        for disc in range(1, TOTAL_DISCIPLINAS + 1):
            for semestre in ['1', '2']:
                periodo = random.randint(1, 8)
                cur.execute(
                    "INSERT INTO Turma (id_turma, periodo, ano, semestre_ano, id_disciplina, id_curso) "
                    "VALUES (%s, %s, 2023, %s, %s, %s)",
                    (tid, periodo, semestre, disc, curso)
                )
                turmas.append((tid, disc, semestre, curso))
                tid += 1

    # 8) Aluno (cada um na turma do 1º semestre da disciplina 1 do seu curso)
    for aid, cpf in enumerate(alunos_cpfs, start=1):
        curso = ((aid - 1) % TOTAL_CURSOS) + 1
        turma_sem1 = next(t[0] for t in turmas if t[1] == 1 and t[2] == '1' and t[3] == curso)
        cur.execute(
            "INSERT INTO Aluno (id_aluno, cpf, id_curso, id_turma) VALUES (%s, %s, %s, %s)",
            (aid, cpf, curso, turma_sem1)
        )

    # 9) Grupo_TCC e TCC
    grupos = TOTAL_ALUNOS // ALUNOS_POR_GRUPO
    for gid in range(1, grupos + 1):
        membros = [((gid - 1) * ALUNOS_POR_GRUPO) + j + 1 for j in range(ALUNOS_POR_GRUPO)]
        cur.execute(
            "INSERT INTO Grupo_TCC (id_grupo, aluno1, aluno2, aluno3, aluno4, aluno5) VALUES (%s, %s, %s, %s, %s, %s)",
            (gid, *membros)
        )
        orient = random.randint(1, TOTAL_PROFESSORES)
        titulo = fake.sentence(nb_words=5)
        cur.execute(
            "INSERT INTO TCC (orientador, titulo, id_grupo) VALUES (%s, %s, %s)",
            (orient, titulo, gid)
        )

    # 10) Aula
    for t in turmas:
        tid = t[0]
        prof_id = ((tid - 1) % TOTAL_PROFESSORES) + 1
        cur.execute(
            "INSERT INTO Aula (id_aula, id_turma, professor_aula) VALUES (%s, %s, %s)",
            (tid, tid, prof_id)
        )

    # 11) Avaliacao / Nota / HistoricoEscolar
    avaliacao_id = 1
    nota_id      = 1

    def insere_nota(aluno, turma_id, disc, val):
        nonlocal avaliacao_id, nota_id
        cur.execute(
            "INSERT INTO Avaliacao (id_avaliacao, nota, id_disciplina) VALUES (%s, %s, %s)",
            (avaliacao_id, val, disc)
        )
        concluido = val >= 6
        cur.execute(
            "INSERT INTO Nota (id_nota, id_aluno, id_turma, concluido, id_avaliacao) VALUES (%s, %s, %s, %s, %s)",
            (nota_id, aluno, turma_id, concluido, avaliacao_id)
        )
        cur.execute(
            "INSERT INTO HistoricoEscolar (id_aluno, id_turma, id_nota) VALUES (%s, %s, %s)",
            (aluno, turma_id, nota_id)
        )
        avaliacao_id += 1
        nota_id      += 1

    # Garante reprovação (4) e aprovação (8) para o aluno 1 na disciplina 1
    sem1 = next(t[0] for t in turmas if t[1] == 1 and t[2] == '1')
    sem2 = next(t[0] for t in turmas if t[1] == 1 and t[2] == '2')
    insere_nota(1, sem1, 1, 4)
    insere_nota(1, sem2, 1, 8)

    # Demais alunos: nota aleatória no sem1 da disciplina 1
    for aid in range(2, TOTAL_ALUNOS + 1):
        curso = ((aid - 1) % TOTAL_CURSOS) + 1
        turma_sem1 = next(t[0] for t in turmas if t[1] == 1 and t[2] == '1' and t[3] == curso)
        val = random.choices(range(0, 11), weights=[1]*2 + [2]*9, k=1)[0]
        insere_nota(aid, turma_sem1, 1, val)

    # Finaliza inserções
    conn.commit()
    cur.close()
    conn.close()
    print("Dados gerados e inseridos com sucesso!")

if __name__ == "__main__":
    main()
