import sqlite3

def ajouter_tache(contact_id, titre, description, date_limite, statut):
    conn = sqlite3.connect("carnet_contactsN.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO taches (contact_id, titre, description, date_limite, statut)
        VALUES (?, ?, ?, ?, ?)
    """, (contact_id, titre, description, date_limite, statut))
    conn.commit()
    conn.close()

def modifier_tache(id_tache, contact_id, titre, description, date_limite, statut):
    conn = sqlite3.connect("carnet_contactsN.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE taches SET contact_id=?, titre=?, description=?, date_limite=?, statut=?
        WHERE idTache=?
    """, (contact_id, titre, description, date_limite, statut, id_tache))
    conn.commit()
    conn.close()

def supprimer_tache(id_tache):
    conn = sqlite3.connect("carnet_contactsN.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM taches WHERE idTache=?", (id_tache,))
    conn.commit()
    conn.close()

def lister_taches(contact_id):
    conn = sqlite3.connect("carnet_contactsN.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM taches WHERE contact_id=?", (contact_id,))
    taches = cursor.fetchall()
    conn.close()
    return taches

def rechercher_tache(terme, contact_id):
    conn = sqlite3.connect("carnet_contactsN.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM taches WHERE contact_id=? AND 
        (titre LIKE ? OR description LIKE ?)
    """, (contact_id, f"%{terme}%", f"%{terme}%"))
    taches = cursor.fetchall()
    conn.close()
    return taches
