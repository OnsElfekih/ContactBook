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
    nom TEXT NOT NULL,
    telephone TEXT NOT NULL,
    email TEXT,
    adresse TEXT,
    type TEXT CHECK(type IN ('professionnel', 'personnel')),
    favori BOOLEAN DEFAULT 0,
    idUtilisateur INTEGER,
    FOREIGN KEY (idUtilisateur) REFERENCES utilisateurs(idUtilisateur)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS taches (
    idTache INTEGER PRIMARY KEY AUTOINCREMENT,
    idUtilisateur INTEGER,
    titre TEXT NOT NULL,
    description TEXT,
    date_limite DATE,
    statut TEXT CHECK(statut IN ('À faire', 'En cours', 'Terminé')),
    idContact INTEGER,  -- Ajout de la bonne clé étrangère
    FOREIGN KEY (idUtilisateur) REFERENCES utilisateurs(idUtilisateur),
    FOREIGN KEY (idContact) REFERENCES contacts(idContact)  -- Correction de la clé étrangère
)
""")


conn.commit()
conn.close()
