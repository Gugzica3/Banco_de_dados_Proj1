SELECT
    t.id_grupo,
    t.titulo,
    p_orient.nome                        AS professor_orientador,
    p_aluno.nome                         AS aluno_integrante
FROM TCC                t
JOIN Professor      prof ON prof.id_professor = t.orientador
JOIN Pessoa      p_orient ON p_orient.cpf     = prof.cpf
JOIN Grupo_TCC           g ON g.id_grupo     = t.id_grupo
LEFT JOIN LATERAL (
        VALUES (g.aluno1), (g.aluno2), (g.aluno3), (g.aluno4), (g.aluno5)
    ) AS g_unpivot(id_aluno)            ON TRUE
JOIN Aluno               a ON a.id_aluno     = g_unpivot.id_aluno
JOIN Pessoa          p_aluno ON p_aluno.cpf  = a.cpf
WHERE t.orientador = 6
ORDER BY t.id_grupo, p_aluno.nome;
