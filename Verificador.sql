-- São 8 verificadores que tem que ser testados 1 de cada vez
SELECT COUNT(*) AS professores_sem_pessoa
FROM Professor p
LEFT JOIN Pessoa pe ON p.cpf = pe.cpf
WHERE pe.cpf IS NULL;

SELECT COUNT(*) AS alunos_sem_pessoa
FROM Aluno a
LEFT JOIN Pessoa pe ON a.cpf = pe.cpf
WHERE pe.cpf IS NULL;

SELECT COUNT(*) AS intersecao_cpfs
FROM (
    SELECT cpf FROM Professor
    INTERSECT
    SELECT cpf FROM Aluno
) sub;

SELECT COUNT(*) AS grupos_incompletos
FROM Grupo_TCC
WHERE aluno1 IS NULL 
   OR aluno2 IS NULL 
   OR aluno3 IS NULL 
   OR aluno4 IS NULL 
   OR aluno5 IS NULL;

SELECT 
    (SELECT COUNT(*) FROM Pessoa) AS total_pessoas,
    (SELECT COUNT(*) FROM Professor) + (SELECT COUNT(*) FROM Aluno) AS total_funcao;

SELECT COUNT(*) AS turmas_inconsistentes
FROM Turma t
LEFT JOIN Disciplina d ON t.id_disciplina = d.id_disciplina
LEFT JOIN Curso c ON t.id_curso = c.id_curso
WHERE d.id_disciplina IS NULL 
   OR c.id_curso IS NULL;

SELECT COUNT(*) AS notas_sem_avaliacao
FROM Nota n
LEFT JOIN Avaliacao a ON n.id_avaliacao = a.id_avaliacao
WHERE a.id_avaliacao IS NULL;

SELECT COUNT(*) AS pessoas_sem_funcao
FROM Pessoa
WHERE cpf NOT IN (SELECT cpf FROM Professor)
  AND cpf NOT IN (SELECT cpf FROM Aluno);
