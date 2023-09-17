CREATE TABLE IF NOT EXISTS "Users" (
    id SERIAL PRIMARY KEY NOT NULL,
    UserName VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Coins INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS "Scores" (
    GameID SERIAL PRIMARY KEY NOT NULL,
    UserID INT NOT NULL REFERENCES "Users"(id),
    Date Date NOT NULL,
    Score INT NOT NULL
);

CREATE TABLE IF NOT EXISTS "Skins" (
    SkinID SERIAL PRIMARY KEY NOT NULL,
    SkinName VARCHAR(255) NOT NULL,
    SkinCost INT NOT NULL
);

INSERT INTO "Skins" ("skinname", "skincost") VALUES ('Snake1', 21);
INSERT INTO "Skins" ("skinname", "skincost") VALUES ('Rock1', 69);
INSERT INTO "Skins" ("skinname", "skincost") VALUES ('Rock2', 420);

CREATE TABLE IF NOT EXISTS "Ownership" (
    UserID INT NOT NULL PRIMARY KEY REFERENCES "Users"(id),
    SnakeSkin BOOLEAN NOT NULL DEFAULT FALSE,
    RockSkin1 BOOLEAN NOT NULL DEFAULT FALSE,
    RockSkin2 BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX ix_UserID ON "Users"(UserName);
CREATE INDEX ix_Password ON "Users"(Password);
CREATE INDEX ix_Score ON "Scores"(Score);