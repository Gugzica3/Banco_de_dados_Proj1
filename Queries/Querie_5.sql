SELECT
    p.nome AS professor,
    COALESCE(d.nome, 'nenhum') AS departamento,
    COALESCE(STRING_AGG(DISTINCT c.nome, ', '), 'nenhum') AS curso
FROM Professor pr
JOIN Pessoa p ON pr.cpf = p.cpf
LEFT JOIN Depto d ON pr.id_professor = d.chefe_depto
LEFT JOIN Curso c ON pr.id_professor = c.coordenador_curso
WHERE d.chefe_depto IS NOT NULL OR c.coordenador_curso IS NOT NULL
GROUP BY p.nome, d.nome
ORDER BY p.nome;
