CREATE TABLE boards (
    id SERIAL PRIMARY KEY,
    name text,
    description text,
    is_public boolean
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username text,
    usergroup integer -- 0 = normal user, 1 = administrator
    -- todo: add passwords
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    board_id integer references boards,
    title text,
    author_id integer references users
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    thread_id integer references threads,
    content text,
    author_id integer references users,
    sent_at timestamp without time zone
);

-- Allows specific user-ids to access private boards
CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    board_id integer references boards,
    user_id integer references users
);

 -- Default boards, users and threads for previewing

INSERT INTO boards (name, description, is_public) values ('Yleinen', 'Yleistä keskustelua', true);
INSERT INTO boards (name, description, is_public) values ('Ohjelmointi', 'Kaikki koodauksesta', true);
INSERT INTO boards (name, description, is_public) values ('Offtopic', 'Muu keskustelu', true);
INSERT INTO boards (name, description, is_public) values ('Salainen alue', 'Shh!', false);

INSERT INTO users (username, usergroup) values ('Admin', 1);
INSERT INTO users (username, usergroup) values ('Käyttäjä 2', 0);

INSERT INTO threads (board_id, title, author_id) values (1, 'Ensimmäinen ketju!', 1);
INSERT INTO threads (board_id, title, author_id) values (1, 'Toinen ketju', 1);

INSERT INTO messages (thread_id, content, author_id, sent_at) values (1, 'Hello world!', 1, '2024-04-05 20:23:54');
INSERT INTO messages (thread_id, content, author_id, sent_at) values (1, 'moi', 2, '2024-04-05 20:24:59');
INSERT INTO messages (thread_id, content, author_id, sent_at) values (1, 'moi', 1, '2024-04-06 19:53:27');
INSERT INTO messages (thread_id, content, author_id, sent_at) values (2, 'Toisen ketjun testausta', 1, '2024-04-05 20:27:12');
