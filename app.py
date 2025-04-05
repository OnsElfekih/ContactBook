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

    # Récupérer les contacts de l'utilisateur
    contacts = conn.execute(
        "SELECT * FROM contacts WHERE idUtilisateur = ?",
        (utilisateur_id,)
    ).fetchall()

    # Récupérer les tâches de l'utilisateur
    taches = conn.execute(
        "SELECT * FROM taches WHERE idUtilisateur = ?",
        (utilisateur_id,)
    ).fetchall()

    # Comptage des contacts et tâches
    nb_personnels = conn.execute(
        "SELECT COUNT(*) FROM contacts WHERE idUtilisateur = ? AND type = 'personnel'",
        (utilisateur_id,)
    ).fetchone()[0]

    nb_professionnels = conn.execute(
        "SELECT COUNT(*) FROM contacts WHERE idUtilisateur = ? AND type = 'professionnelle'",
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

    # Renvoi de la liste des utilisateurs au template
    return render_template("index.html", users=utilisateurs)


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
        contacts=contacts,
        nb_contacts_personnels=nb_personnels,
        nb_contacts_professionnels=nb_professionnels,
        nb_contacts_total=nb_personnels + nb_professionnels
    )

@app.route("/taches")
def taches():
    if "utilisateur_id" not in session:
        return redirect("/login")

    utilisateur_id = session["utilisateur_id"]
    conn = get_db_connection()

    taches = conn.execute(
        "SELECT * FROM taches WHERE idUtilisateur = ?",
        (utilisateur_id,)
    ).fetchall()

    nb_a_faire = conn.execute(
        "SELECT COUNT(*) FROM taches WHERE idUtilisateur = ? AND statut = 'à faire'",
        (utilisateur_id,)
    ).fetchone()[0]

    nb_en_cours = conn.execute(
        "SELECT COUNT(*) FROM taches WHERE idUtilisateur = ? AND statut = 'en cours'",
        (utilisateur_id,)
    ).fetchone()[0]

    nb_termine = conn.execute(
        "SELECT COUNT(*) FROM taches WHERE idUtilisateur = ? AND statut = 'terminé'",
        (utilisateur_id,)
    ).fetchone()[0]

    conn.close()

    return render_template(
        "taches.html",
        taches=taches,
        nb_taches_a_faire=nb_a_faire,
        nb_taches_en_cours=nb_en_cours,
        nb_taches_termine=nb_termine,
        nb_taches_total=nb_a_faire + nb_en_cours + nb_termine
    )

if __name__ == "__main__":
    app.run(debug=True)
