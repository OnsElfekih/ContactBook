import hashlib
import sqlite3

def hash_motdepasse(motdepasse):
    """Hache le mot de passe avec SHA-256."""
    return hashlib.sha256(motdepasse.encode()).hexdigest()

def authentifier(email, motdepasse):
    """Vérifie l'authentification de l'utilisateur."""
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
            print("Échec de l'authentification : email ou mot de passe incorrect.")
            return None
    except sqlite3.Error as e:
        print(f"Erreur de base de données : {e}")
        return None
