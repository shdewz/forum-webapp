CREATE TABLE boards (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    is_public BOOLEAN
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    is_admin BOOLEAN,
    password TEXT
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    board_id INTEGER REFERENCES boards,
    title TEXT,
    author_id INTEGER REFERENCES users
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    thread_id INTEGER REFERENCES threads,
    content TEXT,
    author_id INTEGER REFERENCES users,
    sent_at TIMESTAMP WITHOUT TIME ZONE
);

-- Allows specific user-ids to access private boards
CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    board_id INTEGER REFERENCES boards,
    user_id INTEGER REFERENCES users
);

 -- Default boards, users and threads for previewing

INSERT INTO boards (name, description, is_public) VALUES ('Yleinen', 'Yleistä keskustelua', true);
INSERT INTO boards (name, description, is_public) VALUES ('Ohjelmointi', 'Kaikki koodauksesta', true);
INSERT INTO boards (name, description, is_public) VALUES ('Offtopic', 'Muu keskustelu', true);
INSERT INTO boards (name, description, is_public) VALUES ('Salainen alue', 'Shh!', false);

INSERT INTO users (username, is_admin) VALUES ('Admin', TRUE);
INSERT INTO users (username, is_admin) VALUES ('Käyttäjä 2', FALSE);

INSERT INTO threads (board_id, title, author_id) VALUES (1, 'Ensimmäinen ketju!', 1);
INSERT INTO threads (board_id, title, author_id) VALUES (1, 'Toinen ketju', 1);

INSERT INTO messages (thread_id, content, author_id, sent_at) VALUES (1, 'Hello world!', 1, '2024-04-05 20:23:54');
INSERT INTO messages (thread_id, content, author_id, sent_at) VALUES (1, 'moi', 2, '2024-04-05 20:24:59');
INSERT INTO messages (thread_id, content, author_id, sent_at) VALUES (1, 'moi', 1, '2024-04-06 19:53:27');
INSERT INTO messages (thread_id, content, author_id, sent_at) VALUES (2, 'Toisen ketjun testausta', 1, '2024-04-05 20:27:12');
