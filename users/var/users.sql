PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS Registrations;
CREATE TABLE Registrations (
    UserId INT NOT NULL,
    Username VARCHAR(30) NOT NULL UNIQUE,
    UserPassword VARCHAR(30) NOT NULL,
    BearerToken VARCHAR(255),
    PRIMARY KEY (UserId)
);
DROP TABLE IF EXISTS Roles;
CREATE TABLE Roles (
    RoleId INT NOT NULL,
    RoleName VARCHAR(30) NOT NULL,
    PRIMARY KEY (RoleId)
);
INSERT INTO Roles VALUES 
(1, 'Student'),
(2, 'Instructor'),
(3, 'Registrar');
DROP TABLE IF EXISTS UserRoles;
CREATE TABLE UserRoles (
    Id INT NOT NULL,
    RoleId INT NOT NULL REFERENCES Roles(RoleId),
    UserId INT NOT NULL REFERENCES Registrations(UserId),
    PRIMARY KEY (Id)
);
COMMIT;
