CREATE TABLE user(
id integer PRIMARY KEY NOT NULL,
name char(20) NOT NULL
);

CREATE TABLE task(
    id integer PRIMARY KEY NOT NULL,
    name char(20) NOT NULL,
    description TEXT NOT NULL,
    id_u integer NOT NULL,
    
    CONSTRAINT user_fk FOREIGN KEY (id_u) REFERENCES user(id)
    );