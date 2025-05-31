
-- PARA criar a tabela Livros com: ID, Titulo, Autor, Ano, Genero e Disponivel 
CREATE table Livros (

-- A Primary Key é usada quando queremos garantir que cada registro seja unico
id int PRIMARY KEY,

Titulo varchar (100),
Autor varchar (100),
Ano int,
Genero varchar (100),
Disponivel BOOLEAN
)

-- Para Adicionar o conteudo da tabela
Insert into livros (id, titulo, autor, ano, genero, disponivel) values (1, 'Harry Potter', 'J.K Roling', 2001, 'Drama', True);
Insert into livros (id, titulo, autor, ano, genero, disponivel) values (2, 'Clean Code', 'Robert C. Martin', 2009, 'T.I', True);
Insert into livros (id, titulo, autor, ano, genero, disponivel) values (3, 'YOU', 'Caroline Kepnes', 2018, 'Suspense', True);
Insert into livros (id, titulo, autor, ano, genero, disponivel) values (4, 'SQL', 'Alice Zhao', 2023, 'T.I', True);
Insert into livros (id, titulo, autor, ano, genero, disponivel) values (5, 'Python', 'Luciano Ramalho', 1939, 'T.I', True);


-- Para selecionar todas as colunas ta tabelas
select * from livros;

-- UPDATE: para atualizar o conteudo de uma tabela
Update livros set disponivel=FALSE where id=2

-- Para selecionar os livros em ordem crescente de ano
select * from livros ORDER by ano asc;

-- DELETE: para deletar um conteudo da tabela que atenda a condição
DELETE from livros where ano < 1940

-- Para deletar a Atabela livros
Drop TABLE livros;

-- Recria a tabela livros
CREATE table Livros (
id int PRIMARY KEY,
Titulo varchar (100),
Autor varchar (100),
Ano int,
Genero varchar (100),
Disponivel BOOLEAN
)