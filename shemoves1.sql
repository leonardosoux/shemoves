CREATE DATABASE shemoves1;

USE shemoves1;

CREATE TABLE post (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    image VARCHAR(255),
    likes INT DEFAULT 0
);

CREATE TABLE comment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    post_id INT NOT NULL,
    FOREIGN KEY (post_id) REFERENCES post(id) ON DELETE CASCADE
);

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthdate DATE NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE professional (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthdate DATE NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    cref VARCHAR(12) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

--alteração na tabela post para vincular um post ao usuário 
ALTER TABLE post
ADD COLUMN user_id INT NOT NULL,
ADD CONSTRAINT fk_post_user
FOREIGN KEY (user_id) REFERENCES user(id)
ON DELETE CASCADE;

--alteração na tabela comentário para vincular ao usuário correto
ALTER TABLE comment
ADD COLUMN user_id INT NOT NULL,
ADD CONSTRAINT fk_comment_user FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE;

