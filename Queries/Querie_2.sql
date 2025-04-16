SELECT
    t.id_grupo,
    t.titulo                                  AS titulo_tcc,
    orient.nome                               AS professor_orientador,
    aluno_pessoa.nome                         AS nome_aluno
FROM TCC t

JOIN Professor       pr    ON pr.id_professor = t.orientador
JOIN Pessoa          orient ON orient.cpf    = pr.cpf


JOIN Grupo_TCC       g     ON g.id_grupo      = t.id_grupo


CROSS JOIN LATERAL (
    VALUES
      (g.aluno1),
      (g.aluno2),
      (g.aluno3),
      (g.aluno4),
      (g.aluno5)
) AS membros(id_aluno)

JOIN Aluno           a     ON a.id_aluno      = membros.id_aluno
JOIN Pessoa          aluno_pessoa ON aluno_pessoa.cpf = a.cpf

ORDER BY
    t.id_grupo,
    aluno_pessoa.nome;
