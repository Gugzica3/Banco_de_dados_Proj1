SELECT 
    p.nome AS aluno,
    d.nome AS disciplina,
    t_fail.ano AS ano_reprovacao,
    t_fail.semestre_ano AS semestre_reprovacao,
    av_fail.nota AS nota_reprovacao,
    t_pass.ano AS ano_aprovacao,
    t_pass.semestre_ano AS semestre_aprovacao,
    av_pass.nota AS nota_aprovacao
FROM HistoricoEscolar he_fail
JOIN Nota n_fail 
  ON he_fail.id_nota = n_fail.id_nota
JOIN Avaliacao av_fail 
  ON n_fail.id_avaliacao = av_fail.id_avaliacao
JOIN Turma t_fail 
  ON he_fail.id_turma = t_fail.id_turma
JOIN HistoricoEscolar he_pass 
  ON he_fail.id_aluno = he_pass.id_aluno
JOIN Nota n_pass 
  ON he_pass.id_nota = n_pass.id_nota
JOIN Avaliacao av_pass 
  ON n_pass.id_avaliacao = av_pass.id_avaliacao
JOIN Turma t_pass 
  ON he_pass.id_turma = t_pass.id_turma
JOIN Aluno a 
  ON he_fail.id_aluno = a.id_aluno
JOIN Pessoa p 
  ON a.cpf = p.cpf
JOIN Disciplina d 
  ON t_fail.id_disciplina = d.id_disciplina
WHERE he_fail.id_aluno = 1
  AND t_fail.id_disciplina = t_pass.id_disciplina
  AND av_fail.nota < 6
  AND av_pass.nota >= 6
  AND (t_pass.ano > t_fail.ano 
       OR (t_pass.ano = t_fail.ano 
           AND t_pass.semestre_ano > t_fail.semestre_ano))
ORDER BY t_fail.ano, t_fail.semestre_ano;
