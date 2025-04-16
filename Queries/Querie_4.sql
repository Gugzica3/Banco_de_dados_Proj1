SELECT
    d.id_disciplina AS "Código da Disciplina",
    d.nome AS "Nome da Disciplina",
    STRING_AGG(DISTINCT p_prof.nome, ', ') AS "Professores que Lecionaram"
FROM HistoricoEscolar he
JOIN Turma t ON he.id_turma = t.id_turma
JOIN Disciplina d ON t.id_disciplina = d.id_disciplina
JOIN Aula a ON a.id_turma = t.id_turma
JOIN Professor pr ON a.professor_aula = pr.id_professor
JOIN Pessoa p_prof ON pr.cpf = p_prof.cpf
WHERE he.id_aluno = 1
GROUP BY d.id_disciplina, d.nome
ORDER BY d.id_disciplina;
