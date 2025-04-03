import sqlite3

conn = sqlite3.connect("carnet_contacts.db")
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
    motdepasse TEXT,
    type TEXT CHECK(type IN ('professionnelle', 'personnel')),
    favori BOOLEAN DEFAULT 0,
    utilisateur_id INTEGER,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS taches (
    idTache INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_id INTEGER,
    titre TEXT NOT NULL,
    description TEXT,
    date_limite DATE,
    statut TEXT CHECK(statut IN ('À faire', 'En cours', 'Terminé')),
    FOREIGN KEY (contact_id) REFERENCES contacts(id)
)
""")

conn.commit()
conn.close()
