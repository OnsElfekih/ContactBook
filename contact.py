import sqlite3

def ajouter_contact(nom, telephone, email, adresse, motdepasse, type_contact, favori, utilisateur_id):
    conn = sqlite3.connect("carnet_contactsN.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contacts (nom, telephone, email, adresse, motdepasse, type, favori, utilisateur_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (nom, telephone, email, adresse, motdepasse, type_contact, favori, utilisateur_id))
    conn.commit()
    conn.close()

def modifier_contact(id_contact, nom, telephone, email, adresse, motdepasse, type_contact, favori):
    conn = sqlite3.connect("carnet_contactsN.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE contacts SET nom=?, telephone=?, email=?, adresse=?, motdepasse=?, type=?, favori=?
        WHERE idContact=?
    """, (nom, telephone, email, adresse, motdepasse, type_contact, favori, id_contact))
    conn.commit()
    conn.close()

def supprimer_contact(id_contact):
    conn = sqlite3.connect("carnet_contactsN.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE idContact=?", (id_contact,))
    conn.commit()
    conn.close()

def lister_contacts(utilisateur_id):
    conn = sqlite3.connect("carnet_contactsN.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE utilisateur_id=?", (utilisateur_id,))
    contacts = cursor.fetchall()
    conn.close()
    return contacts

def rechercher_contact(terme, utilisateur_id):
    conn = sqlite3.connect("carnet_contactsN.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM contacts WHERE utilisateur_id=? AND 
        (nom LIKE ? OR telephone LIKE ? OR email LIKE ? OR adresse LIKE ?)
    """, (utilisateur_id, f"%{terme}%", f"%{terme}%", f"%{terme}%", f"%{terme}%"))
    contacts = cursor.fetchall()
    conn.close()
    return contacts
