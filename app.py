from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "votre_clé_secrète"
def get_db_connection():
    conn = sqlite3.connect("carnet_contactsN.db")
    conn.row_factory = sqlite3.Row
    return conn 
@app.route("/")
def home():
    return redirect("/login")
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        motdepasse = request.form["password"]
        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO utilisateurs (email, motdepasse) VALUES (?, ?)", (email, motdepasse))
            conn.commit()
            return redirect("/login")
        except:
            return "Erreur : cet email est déjà utilisé."
        finally:
            conn.close()
    return render_template("signup.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        motdepasse = data.get("password")
        conn = get_db_connection()
        utilisateur = conn.execute(
            "SELECT * FROM utilisateurs WHERE email = ? AND motdepasse = ?",
            (email, motdepasse)
        ).fetchone()
        conn.close()
        if utilisateur:
            session["utilisateur_id"] = utilisateur["idUtilisateur"]
            session["email"] = utilisateur["email"]
            return jsonify({"success": True, "message": "Authentification réussie"})
        else:
            return jsonify({"error": "Email ou mot de passe incorrect."})
    return render_template("login.html")
@app.route("/dashboard")
def dashboard():
    if "utilisateur_id" not in session:
        return redirect("/login")
    utilisateur_id = session["utilisateur_id"]
    conn = get_db_connection()
    contacts = conn.execute(
        "SELECT * FROM contacts WHERE idUtilisateur = ?",
        (utilisateur_id,)
    ).fetchall()
    taches = conn.execute(
        "SELECT * FROM taches WHERE idUtilisateur = ?",
        (utilisateur_id,)
    ).fetchall()
    nb_personnels = conn.execute(
        "SELECT COUNT(*) FROM contacts WHERE idUtilisateur = ? AND type = 'personnel'",
        (utilisateur_id,)
    ).fetchone()[0]
    nb_professionnels = conn.execute(
        "SELECT COUNT(*) FROM contacts WHERE idUtilisateur = ? AND type = 'professionnel'",
        (utilisateur_id,)
    ).fetchone()[0]
    nb_a_faire = conn.execute(
        "SELECT COUNT(*) FROM taches WHERE idUtilisateur = ? AND statut = 'À faire'",
        (utilisateur_id,)
    ).fetchone()[0]
    nb_en_cours = conn.execute(
        "SELECT COUNT(*) FROM taches WHERE idUtilisateur = ? AND statut = 'En cours'",
        (utilisateur_id,)
    ).fetchone()[0]
    nb_termine = conn.execute(
        "SELECT COUNT(*) FROM taches WHERE idUtilisateur = ? AND statut = 'Terminé'",
        (utilisateur_id,)
    ).fetchone()[0]
    conn.close()
    return render_template(
        "dashboard.html",
        email=session["email"],
        contacts=contacts,  # Liste des contacts
        taches=taches,  # Liste des tâches
        nb_contacts_personnels=nb_personnels,
        nb_contacts_professionnels=nb_professionnels,
        nb_contacts_total=nb_personnels + nb_professionnels,
        nb_taches_a_faire=nb_a_faire,
        nb_taches_en_cours=nb_en_cours,
        nb_taches_termine=nb_termine,
        nb_taches_total=nb_a_faire + nb_en_cours + nb_termine
    )
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
@app.route("/liste")
def liste_utilisateurs():
    conn = get_db_connection()
    utilisateurs = conn.execute("SELECT idUtilisateur, email,  motdepasse FROM utilisateurs").fetchall()
    conn.close()
    return render_template("index.html", users=utilisateurs)
@app.route("/listeTaches")
def liste_taches():
    if "utilisateur_id" not in session:
        return redirect("/login")
    utilisateur_id = session["utilisateur_id"]
    conn = get_db_connection()
    taches = conn.execute(
        "SELECT * FROM taches WHERE idUtilisateur = ?",
        (utilisateur_id,)
    ).fetchall()
    conn.close()
    return render_template("liste_taches.html", taches=taches)
@app.route("/contacts")
def contacts():
    if "utilisateur_id" not in session:
        return redirect("/login")
    utilisateur_id = session["utilisateur_id"]
    conn = get_db_connection()
    contacts = conn.execute(
        "SELECT * FROM contacts WHERE idUtilisateur = ?",
        (utilisateur_id,)
    ).fetchall()
    nb_personnels = conn.execute(
        "SELECT COUNT(*) FROM contacts WHERE idUtilisateur = ? AND type = 'personnel'",
        (utilisateur_id,)
    ).fetchone()[0]
    nb_professionnels = conn.execute(
        "SELECT COUNT(*) FROM contacts WHERE idUtilisateur = ? AND type = 'professionnel'",
        (utilisateur_id,)
    ).fetchone()[0]
    conn.close()
    return render_template(
        "contacts.html",
        email=session["email"],
        contacts=contacts,
        nb_contacts_personnels=nb_personnels,
        nb_contacts_professionnels=nb_professionnels,
        nb_contacts_total=nb_personnels + nb_professionnels
    )
@app.route("/taches", methods=["GET"])
def taches():
    if "utilisateur_id" not in session:
        return redirect("/login")
    conn = get_db_connection()
    cursor = conn.cursor()
    utilisateur_id = session["utilisateur_id"]
    cursor.execute("SELECT selectedday FROM taches WHERE idUtilisateur = ?", (utilisateur_id,))
    dates_taches = cursor.fetchall()
    selected_dates = [date[0] for date in dates_taches]
    conn.close()
    return render_template("taches.html", email=session["email"],selected_dates=selected_dates)
@app.route("/ajouter", methods=["POST"])
def ajouter_contact():
    if "utilisateur_id" not in session:
        return redirect("/login")
    utilisateur_id = session["utilisateur_id"]
    nom = request.form["nom"]
    email = request.form["email"]
    telephone = request.form["telephone"]
    adresse = request.form["adresse"]
    type_contact = request.form["type"]
    favori = request.form["favori"]
    if type_contact not in ["personnel", "professionnel"]:
        return "Erreur : Type de contact invalide."
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO contacts (nom, email, telephone, adresse, type, favori, idUtilisateur) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (nom, email, telephone, adresse, type_contact, favori, utilisateur_id)
    )
    conn.commit()
    conn.close()
    return redirect("/contacts")
@app.route("/supprimer_contact", methods=["POST"])
def supprimer_contact():
    if "utilisateur_id" not in session:
        return redirect("/login")
    id_contact = request.form["idContact"]
    utilisateur_id = session["utilisateur_id"]
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM contacts WHERE idContact = ? AND idUtilisateur = ?",
        (id_contact, utilisateur_id)
    )
    conn.commit()
    conn.close()
    return redirect("/contacts")
@app.route('/modifier', methods=['POST'])
def modifier_contact():
    idContact = request.form['idContact']
    nom = request.form['nom']
    email = request.form['email']
    telephone = request.form['telephone']
    adresse = request.form['adresse']
    type_contact = request.form['type']
    favori = request.form['favori']
    conn = get_db_connection()
    conn.execute("""
        UPDATE contacts 
        SET nom = ?, email = ?, telephone = ?, adresse = ?, type = ?, favori = ? 
        WHERE idContact = ?
    """, (nom, email, telephone, adresse, type_contact, favori, idContact))
    conn.commit()
    conn.close()
    return redirect('/contacts')
@app.route("/ajouter_tache", methods=["GET", "POST"])
def ajouter_tache():
    if "utilisateur_id" not in session:
        return redirect("/login")
    if request.method == "POST":
        titre = request.form["titre"]
        description = request.form["description"]
        deadline = request.form["deadline"]
        selectedday = request.form.get("selectedday")
        statut = request.form["statut"]
        utilisateur_id = session["utilisateur_id"]
        if statut not in ["À faire", "En cours", "Terminé"]:
            return "Erreur : Statut de tâche invalide."
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO taches (titre, description, deadline, statut, selectedday, idUtilisateur) VALUES (?, ?, ?, ?, ?, ?)",
            (titre, description, deadline, statut, selectedday, utilisateur_id)
        )
        conn.commit()
        conn.close()
        return redirect("/taches")
    return render_template("ajouter_tache.html")
@app.route("/ttaches")
def api_taches():
    if "utilisateur_id" not in session:
        return jsonify([])
    utilisateur_id = session["utilisateur_id"]
    conn = get_db_connection()
    taches = conn.execute(
        "SELECT titre, selectedday FROM taches WHERE idUtilisateur = ?",
        (utilisateur_id,)
    ).fetchall()
    conn.close()
    events = [{"title": t["titre"], "start": t["selectedday"]} for t in taches]
    return jsonify(events)
@app.route("/supprimer_toutes_taches", methods=["POST"])
def supprimer_toutes_taches():
    if "utilisateur_id" not in session:
        return redirect("/login")
    utilisateur_id = session["utilisateur_id"]
    conn = get_db_connection()
    conn.execute("DELETE FROM taches WHERE idUtilisateur = ?", (utilisateur_id,))
    conn.commit()
    conn.close()
    return redirect("/taches")
@app.route("/tache/<string:selectedday>", methods=["GET"])
def get_tache(selectedday):
    if "utilisateur_id" not in session:
        return redirect("/login")
    
    utilisateur_id = session["utilisateur_id"]
    conn = get_db_connection()
    
    # Fetch the task based on the selected day
    task = conn.execute(
        "SELECT titre, description, deadline, statut FROM taches WHERE selectedday = ? AND idUtilisateur = ?",
        (selectedday, utilisateur_id)
    ).fetchone()
    
    conn.close()

    if task:
        return jsonify({
            "titre": task["titre"],
            "description": task["description"],
            "deadline": task["deadline"],
            "statut": task["statut"]
        })
    return jsonify({"error": "Task not found."}), 404

@app.route("/supprimer_tache", methods=["POST"])
def supprimer_tache():
    if "utilisateur_id" not in session:
        return redirect("/login")
    id_tache = request.form["idTache"]
    utilisateur_id = session["utilisateur_id"]
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM taches WHERE idTache = ? AND idUtilisateur = ?",
        (id_tache, utilisateur_id)
    )
    conn.commit()
    conn.close()
    return redirect("/listeTaches")
@app.route("/modifier_tache", methods=["GET", "POST"])
def modifier_tache():
    if "utilisateur_id" not in session:
        return redirect("/login")
    if request.method == "POST":
        id_tache = request.form["idTache"]
        titre = request.form["titre"]
        description = request.form["description"]
        deadline = request.form["deadline"]
        statut = request.form["statut"]
        selectedday = request.form.get("selectedday")
        utilisateur_id = session["utilisateur_id"]
        if statut not in ["À faire", "En cours", "Terminé"]:
            return "Erreur : Statut de tâche invalide."
        conn = get_db_connection()
        conn.execute("""
            UPDATE taches
            SET titre = ?, description = ?, deadline = ?, statut = ?, selectedday = ?
            WHERE idTache = ? AND idUtilisateur = ?
        """, (titre, description, deadline, statut, selectedday, id_tache, utilisateur_id))
        conn.commit()
        conn.close()
        return redirect("/taches")
    id_tache = request.args.get("idTache")
    conn = get_db_connection()
    tache = conn.execute(
        "SELECT * FROM taches WHERE idTache = ? AND idUtilisateur = ?",
        (id_tache, session["utilisateur_id"])
    ).fetchone()
    conn.close()
    if tache:
        return render_template("taches.html", tache=tache)
    return "Tâche non trouvée."


if __name__ == "__main__":
    app.run(debug=True)
