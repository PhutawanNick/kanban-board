CREATE TABLE "Users" (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE "Boards" (
    board_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_by_user_id INTEGER NOT NULL,
    FOREIGN KEY (created_by_user_id) REFERENCES "Users"(user_id) ON DELETE CASCADE
);

CREATE TABLE "BoardMembers" (
    board_member_id SERIAL PRIMARY KEY,
    board_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (board_id) REFERENCES "Boards"(board_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES "Users"(user_id) ON DELETE CASCADE
);

CREATE TABLE "Columns" (
    column_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    board_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (board_id) REFERENCES "Boards"(board_id) ON DELETE CASCADE
);

CREATE TABLE "Tasks" (
    task_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    position INTEGER NOT NULL,
    column_id INTEGER NOT NULL,
    description TEXT,
    FOREIGN KEY (column_id) REFERENCES "Columns"(column_id) ON DELETE CASCADE
);

CREATE TABLE "TaskMembers" (
    task_member_id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (task_id) REFERENCES "Tasks"(task_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES "Users"(user_id) ON DELETE CASCADE
);
