CREATE TABLE role (
    role_id INT,
    role_name VARCHAR(100),
    description VARCHAR(100),
    PRIMARY KEY (role_id)
);

CREATE TABLE roles_users (
    user_id INT,
    role_id INT,
    PRIMARY KEY (user_id)
);

CREATE TABLE user (
    user_id INT,
    email VARCHAR(100),
    username VARCHAR(100),
    password VARCHAR(100),
    active BOOLEAN,
    PRIMARY KEY (user_id),
    UNIQUE (email)
);

CREATE TABLE matches (
    match_id INT(100),
    match_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    team_a VARCHAR(50),
    team_b VARCHAR(50),
    competition VARCHAR(100),
    match_status TINYINT,
    PRIMARY KEY (match_id)
);

CREATE TABLE events (
    event_id INT,
    match_id INT,
    description VARCHAR(255),
    question_text VARCHAR(255),
    PRIMARY KEY (event_id),
    FOREIGN KEY (match_id)
        REFERENCES matches (match_id)
);


CREATE TABLE votes (
    vote_id INT,
    user_id INT,
    vote BOOL,
    event_id INT,
    PRIMARY KEY (user_id , event_id),
    FOREIGN KEY (user_id)
        REFERENCES user (user_id),
    FOREIGN KEY (event_id)
        REFERENCES events (event_id)
);

CREATE TABLE media (
    media_id INT,
    event_id INT,
    media_type TINYINT,
    media_url VARCHAR(255),
    PRIMARY KEY (media_id),
    FOREIGN KEY (event_id)
        REFERENCES events (event_id)
);