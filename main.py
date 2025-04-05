from contact import lister_contacts
from tache import lister_taches
from auth import authentifier
import sqlite3

def lister_utilisateurs():
    try:
        conn = sqlite3.connect("carnet_contactsN.db")
        cursor = conn.cursor()
        cursor.execute("SELECT idUtilisateur, email FROM utilisateurs")
        utilisateurs = cursor.fetchall()
        conn.close()
        return utilisateurs
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération des utilisateurs : {e}")
        return []

def afficher_toutes_les_donnees():
    utilisateurs = lister_utilisateurs()
    for utilisateur in utilisateurs:
        id_user = utilisateur[0]
        email = utilisateur[1]
        print(f"Utilisateur ID: {id_user} | Email: {email}")

        contacts = lister_contacts(id_user)
        if not contacts:
            print("  Aucun contact trouvé")
        else:
            for contact in contacts:
                print(f"  Contact ID: {contact[0]} | Nom: {contact[1]} | Tel: {contact[2]}")
                
                taches = lister_taches(contact[0])
                if not taches:
                    print("    Aucune tâche")
                else:
                    for tache in taches:
                        print(f"    Tâche ID: {tache[0]} | Titre: {tache[2]} | Statut: {tache[5]}")

# Exécution
if __name__ == "__main__":
    afficher_toutes_les_donnees()
