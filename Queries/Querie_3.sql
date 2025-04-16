-- CIENCIAS DA COMPUTACAO
SELECT DISTINCT
    c.nome AS curso,
    d.id_disciplina,
    d.nome AS disciplina
FROM Curso c
JOIN Turma t ON c.id_curso = t.id_curso
JOIN Disciplina d ON t.id_disciplina = d.id_disciplina
WHERE c.nome = 'Ciencias da Computacao'
ORDER BY d.nome;
-- CIENCIAS DE DADOS
SELECT DISTINCT
    c.nome AS curso,
    d.id_disciplina,
    d.nome AS disciplina
FROM Curso c
JOIN Turma t ON c.id_curso = t.id_curso
JOIN Disciplina d ON t.id_disciplina = d.id_disciplina
WHERE c.nome = 'Ciencias de dados'
ORDER BY d.nome;

