WITH dados AS (
    SELECT
        he.id_aluno,
        pes.nome                 AS aluno,
        d.id_disciplina,
        d.nome                   AS disciplina,
        t.ano,
        t.semestre_ano::INT      AS semestre,
        a.nota,
        ROW_NUMBER() OVER (
            PARTITION BY he.id_aluno, d.id_disciplina
            ORDER BY a.id_avaliacao           
        ) AS tentativa_ord
    FROM HistoricoEscolar he
    JOIN Nota       n   ON n.id_nota       = he.id_nota
    JOIN Avaliacao  a   ON a.id_avaliacao  = n.id_avaliacao
    JOIN Turma      t   ON t.id_turma      = he.id_turma
    JOIN Disciplina d   ON d.id_disciplina = t.id_disciplina
    JOIN Aluno      al  ON al.id_aluno     = he.id_aluno
    JOIN Pessoa     pes ON pes.cpf         = al.cpf
),
aluno_caso AS (        
    SELECT DISTINCT
           d1.id_aluno,
           d1.id_disciplina
    FROM dados d1
    JOIN dados d2
      ON d2.id_aluno      = d1.id_aluno
     AND d2.id_disciplina = d1.id_disciplina
     AND d2.tentativa_ord > d1.tentativa_ord   
    WHERE d1.nota < 6                          
      AND d2.nota >= 6                         
)
SELECT d.*
FROM dados d
JOIN aluno_caso ac
  ON ac.id_aluno      = d.id_aluno
 AND ac.id_disciplina = d.id_disciplina
ORDER BY d.id_aluno, d.disciplina, d.tentativa_ord;
