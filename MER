MerDiagram

    pessoa {
        VARCHAR cpf PK
        VARCHAR nome
    }

    professor {
        INT id_professor PK
        VARCHAR cpf FK
        INT id_depto FK
    }

    depto {
        INT id_depto PK
        VARCHAR nome
        INT chefe_depto FK
    }

    curso {
        INT id_curso PK
        VARCHAR nome
        INT id_depto FK
        INT coordenador_curso FK
    }

    disciplina {
        INT id_disciplina PK
        VARCHAR nome
        INT id_depto FK
        INT coordenador_disciplina FK
    }

    turma {
        INT id_turma PK
        INT periodo
        INT ano
        VARCHAR semestre_ano
        INT id_disciplina FK
        INT id_curso FK
    }

    aluno {
        INT id_aluno PK
        VARCHAR cpf FK
        INT id_curso FK
        INT id_turma FK
    }

    grupo_tcc {
        INT id_grupo PK
        INT aluno1 FK
        INT aluno2 FK
        INT aluno3 FK
        INT aluno4 FK
        INT aluno5 FK
    }

    tcc {
        INT orientador FK
        VARCHAR titulo
        INT id_grupo FK
    }

    aula {
        INT id_aula PK
        INT id_turma FK
        INT professor_aula FK
    }

    avaliacao {
        INT id_avaliacao PK
        INT nota
        INT id_disciplina FK
    }

    nota {
        INT id_nota PK
        INT id_aluno FK
        INT id_turma FK
        BOOLEAN concluido
        INT id_avaliacao FK
    }

    historicoescolar {
        INT id_historico PK
        INT id_aluno FK
        INT id_turma FK
        INT id_nota FK
    }

    %% RELACIONAMENTOS
    professor ||--o{ depto : "atua"
    professor ||--o{ curso : "coordena"
    professor ||--o{ disciplina : "coordena"
    professor ||--o{ aula : "leciona"
    professor ||--o{ tcc : "orienta"
    
    pessoa ||--|| professor : "é"
    pessoa ||--|| aluno : "é"
    
    depto ||--o{ curso : "contém"
    depto ||--o{ disciplina : "contém"
    depto ||--o{ professor : "aloca"
    
    curso ||--o{ aluno : "tem"
    curso ||--o{ turma : "organiza"
    
    disciplina ||--o{ turma : "ministrada em"
    disciplina ||--o{ avaliacao : "avaliada em"

    turma ||--o{ aula : "tem"
    turma ||--o{ aluno : "aloca"
    turma ||--o{ historicoescolar : "registra"
    
    aluno ||--o{ grupo_tcc : "participa"
    aluno ||--o{ nota : "recebe"
    aluno ||--o{ historicoescolar : "registra"

    grupo_tcc ||--|| tcc : "relaciona"
    avaliacao ||--o{ nota : "atribui"
    nota ||--o{ historicoescolar : "registra"
