-- PESSOA
CREATE TABLE Pessoa (
    cpf VARCHAR(14) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- DEPARTAMENTO
CREATE TABLE Depto (
    id_depto SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- PROFESSOR
CREATE TABLE Professor (
    id_professor SERIAL PRIMARY KEY,
    cpf VARCHAR(14) NOT NULL,
    id_depto INT NOT NULL,
    FOREIGN KEY (cpf) REFERENCES Pessoa(cpf),
    FOREIGN KEY (id_depto) REFERENCES Depto(id_depto)
);

-- Adiciona chefe_depto depois que Professor já existir
ALTER TABLE Depto ADD COLUMN chefe_depto INT;
ALTER TABLE Depto ADD CONSTRAINT fk_chefe FOREIGN KEY (chefe_depto) REFERENCES Professor(id_professor);

-- CURSO
CREATE TABLE Curso (
    id_curso SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    id_depto INT NOT NULL,
    coordenador_curso INT,
    FOREIGN KEY (id_depto) REFERENCES Depto(id_depto),
    FOREIGN KEY (coordenador_curso) REFERENCES Professor(id_professor)
);

-- DISCIPLINA
CREATE TABLE Disciplina (
    id_disciplina SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    id_depto INT NOT NULL,
    coordenador_disciplina INT,
    FOREIGN KEY (id_depto) REFERENCES Depto(id_depto),
    FOREIGN KEY (coordenador_disciplina) REFERENCES Professor(id_professor)
);

-- TURMA
CREATE TABLE Turma (
    id_turma SERIAL PRIMARY KEY,
    periodo INT NOT NULL,
    ano INT NOT NULL,
    semestre_ano VARCHAR(10) NOT NULL,
    id_disciplina INT NOT NULL,
    id_curso INT NOT NULL,
    FOREIGN KEY (id_disciplina) REFERENCES Disciplina(id_disciplina),
    FOREIGN KEY (id_curso) REFERENCES Curso(id_curso)
);

-- ALUNO
CREATE TABLE Aluno (
    id_aluno SERIAL PRIMARY KEY,
    cpf VARCHAR(14) NOT NULL,
    id_curso INT NOT NULL,
    id_turma INT NOT NULL,
    FOREIGN KEY (cpf) REFERENCES Pessoa(cpf),
    FOREIGN KEY (id_curso) REFERENCES Curso(id_curso),
    FOREIGN KEY (id_turma) REFERENCES Turma(id_turma)
);

-- GRUPO TCC
CREATE TABLE Grupo_TCC (
    id_grupo SERIAL PRIMARY KEY,
    aluno1 INT,
    aluno2 INT,
    aluno3 INT,
    aluno4 INT,
    aluno5 INT,
    FOREIGN KEY (aluno1) REFERENCES Aluno(id_aluno),
    FOREIGN KEY (aluno2) REFERENCES Aluno(id_aluno),
    FOREIGN KEY (aluno3) REFERENCES Aluno(id_aluno),
    FOREIGN KEY (aluno4) REFERENCES Aluno(id_aluno),
    FOREIGN KEY (aluno5) REFERENCES Aluno(id_aluno)
);

-- TCC
CREATE TABLE TCC (
    orientador INT NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    id_grupo INT NOT NULL,
    FOREIGN KEY (orientador) REFERENCES Professor(id_professor),
    FOREIGN KEY (id_grupo) REFERENCES Grupo_TCC(id_grupo)
);

-- AULA
CREATE TABLE Aula (
    id_aula SERIAL PRIMARY KEY,
    id_turma INT NOT NULL,
    professor_aula INT NOT NULL,
    FOREIGN KEY (id_turma) REFERENCES Turma(id_turma),
    FOREIGN KEY (professor_aula) REFERENCES Professor(id_professor)
);

-- AVALIACAO
CREATE TABLE Avaliacao (
    id_avaliacao SERIAL PRIMARY KEY,
    nota INT NOT NULL,
    id_disciplina INT NOT NULL,
    FOREIGN KEY (id_disciplina) REFERENCES Disciplina(id_disciplina)
);

-- NOTA
CREATE TABLE Nota (
    id_nota SERIAL PRIMARY KEY,
    id_aluno INT NOT NULL,
    id_turma INT NOT NULL,
    concluido BOOLEAN NOT NULL,
    id_avaliacao INT NOT NULL,
    FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno),
    FOREIGN KEY (id_turma) REFERENCES Turma(id_turma),
    FOREIGN KEY (id_avaliacao) REFERENCES Avaliacao(id_avaliacao)
);

-- HISTÓRICO ESCOLAR
CREATE TABLE HistoricoEscolar (
    id_aluno INT NOT NULL,
    id_turma INT NOT NULL,
    id_nota INT NOT NULL,
    PRIMARY KEY (id_aluno, id_turma, id_nota),
    FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno),
    FOREIGN KEY (id_turma) REFERENCES Turma(id_turma),
    FOREIGN KEY (id_nota) REFERENCES Nota(id_nota)
);
