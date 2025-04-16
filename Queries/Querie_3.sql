SELECT DISTINCT
    d.id_disciplina,
    d.nome AS disciplina
FROM Turma      t
JOIN Disciplina d ON d.id_disciplina = t.id_disciplina
WHERE t.id_curso = 1              
ORDER BY d.id_disciplina;

--Pode selecionar o curso trocando o numero

