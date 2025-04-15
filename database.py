import sqlite3

conn = sqlite3.connect("carnet_contactsN.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS utilisateurs (
    idUtilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    motdepasse TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    idContact INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL unique,
    telephone TEXT NOT NULL unique,
    email TEXT NOT NULL unique,
    adresse TEXT,
    type TEXT CHECK(type IN ('professionnel', 'personnel')),
    favori BOOLEAN DEFAULT 0,
    idUtilisateur INTEGER,
    FOREIGN KEY (idUtilisateur) REFERENCES utilisateurs(idUtilisateur)
)
""")

cursor.execute("""
CREATE TABLE taches (
    idTache INTEGER PRIMARY KEY AUTOINCREMENT,
    idUtilisateur INTEGER,
    titre TEXT,
    description TEXT,
    deadline DATE,
    statut TEXT,
    selectedday DATE,
    FOREIGN KEY (idUtilisateur) REFERENCES utilisateurs(idUtilisateur)
);

""")


conn.commit()
conn.close()
