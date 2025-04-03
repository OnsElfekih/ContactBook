import hashlib
import sqlite3

# Fonction de hachage du mot de passe
def hash_motdepasse(motdepasse):
    return hashlib.sha256(motdepasse.encode()).hexdigest()

# Fonction d'authentification
def authentifier(email, motdepasse):
    try:
        conn = sqlite3.connect("carnet_contacts.db")
        cursor = conn.cursor()
        cursor.execute("SELECT idUtilisateur, motdepasse FROM utilisateurs WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and user[1] == hash_motdepasse(motdepasse):
            print("Authentification réussie")
            return user[0]  # Retourne l'ID de l'utilisateur
        else:
            print("Échec de l'authentification")
            return None
    except sqlite3.Error as e:
        print(f"Erreur de base de données : {e}")
        return None

# Fonction d'ajout de contact
def ajouter_contact(nom, telephone, email, adresse, type_contact, favori, utilisateur_id):
    conn = sqlite3.connect("carnet_contacts.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contacts (nom, telephone, email, adresse, type, favori, utilisateur_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nom, telephone, email, adresse, type_contact, favori, utilisateur_id))
    conn.commit()
    conn.close()

# Fonction de liste des contacts
def lister_contacts(utilisateur_id):
    conn = sqlite3.connect("carnet_contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE utilisateur_id = ?", (utilisateur_id,))
    contacts = cursor.fetchall()
    conn.close()
    return contacts

# Fonction d'ajout de tâche
def ajouter_tache(contact_id, titre, description, date_limite, statut):
    conn = sqlite3.connect("carnet_contacts.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO taches (contact_id, titre, description, date_limite, statut)
        VALUES (?, ?, ?, ?, ?)
    """, (contact_id, titre, description, date_limite, statut))
    conn.commit()
    conn.close()

# Fonction de liste des tâches
def lister_taches(contact_id):
    conn = sqlite3.connect("carnet_contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM taches WHERE contact_id = ?", (contact_id,))
    taches = cursor.fetchall()
    conn.close()
    return taches

# Tester l'ajout d'un utilisateur, contact et tâche
def test_application():
    # Inscription utilisateur
    email = "test@email.com"
    motdepasse = "password123"
    motdepasse_hache = hash_motdepasse(motdepasse)

    # Ajouter un utilisateur à la base de données
    conn = sqlite3.connect("carnet_contacts.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO utilisateurs (email, motdepasse) VALUES (?, ?)", (email, motdepasse_hache))
    conn.commit()
    conn.close()

    # Authentification
    user_id = authentifier(email, motdepasse)
    if user_id:
        print(f"Utilisateur {email} authentifié avec succès. ID utilisateur: {user_id}")
        
        # Ajouter un contact
        ajouter_contact("Jean Dupont", "0601020304", "jean@email.com", "10 rue des Lilas", "personnel", 1, user_id)
        
        # Lister les contacts
        contacts = lister_contacts(user_id)
        print("Liste des contacts:")
        for contact in contacts:
            print(contact)
        
        # Ajouter une tâche
        ajouter_tache(1, "Rappeler Jean", "Confirmer RDV", "2025-04-10", "À faire")
        
        # Lister les tâches
        taches = lister_taches(1)  # Utilise un contact_id valide (ici 1 pour cet exemple)
        print("Liste des tâches:")
        for tache in taches:
            print(tache)
    else:
        print("Échec de l'authentification")

# Lancer le test
test_application()
