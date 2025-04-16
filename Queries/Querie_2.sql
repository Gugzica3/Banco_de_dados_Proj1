SELECT 
    tcc.titulo,
    p_orientador.nome AS orientador,
    CONCAT_WS(', ',
              pa1.nome,
              pa2.nome,
              pa3.nome,
              pa4.nome,
              pa5.nome) AS alunos
FROM TCC tcc
JOIN Professor pr ON tcc.orientador = pr.id_professor
JOIN Pessoa p_orientador ON pr.cpf = p_orientador.cpf
JOIN Grupo_TCC gt ON tcc.id_grupo = gt.id_grupo
LEFT JOIN Aluno a1 ON gt.aluno1 = a1.id_aluno
LEFT JOIN Pessoa pa1 ON a1.cpf = pa1.cpf
LEFT JOIN Aluno a2 ON gt.aluno2 = a2.id_aluno
LEFT JOIN Pessoa pa2 ON a2.cpf = pa2.cpf
LEFT JOIN Aluno a3 ON gt.aluno3 = a3.id_aluno
LEFT JOIN Pessoa pa3 ON a3.cpf = pa3.cpf
LEFT JOIN Aluno a4 ON gt.aluno4 = a4.id_aluno
LEFT JOIN Pessoa pa4 ON a4.cpf = pa4.cpf
LEFT JOIN Aluno a5 ON gt.aluno5 = a5.id_aluno
LEFT JOIN Pessoa pa5 ON a5.cpf = pa5.cpf
ORDER BY tcc.titulo;
