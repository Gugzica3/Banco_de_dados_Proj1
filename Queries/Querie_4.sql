SELECT
    t.ano || '-' || t.semestre_ano AS semestre,

    d.id_disciplina,
    d.nome,
    p.id_professor,
    pes.nome AS nom_prof

FROM HistoricoEscolar hs
JOIN Nota          n   ON n.id_nota       = hs.id_nota
JOIN Turma         t   ON t.id_turma      = hs.id_turma
JOIN Disciplina    d   ON d.id_disciplina = t.id_disciplina
JOIN Aula          a   ON a.id_turma      = t.id_turma
JOIN Professor     p   ON p.id_professor  = a.professor_aula
JOIN Pessoa      pes   ON pes.cpf         = p.cpf

WHERE hs.id_aluno = 10 
ORDER BY
    hs.id_aluno,
    d.id_disciplina,
    t.ano,
    t.semestre_ano;
