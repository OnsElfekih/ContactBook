from flask import Flask, render_template, request, redirect, session
import sqlite3
from auth import authentifier, hash_motdepasse

app = Flask(__name__)
app.secret_key = "votre_clé_secrète"

def get_db_connection():
    conn = sqlite3.connect("carnet_contacts.db")
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

from flask import Flask, request, jsonify

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        motdepasse = data.get("password")

        resultat = authentifier(email, motdepasse)

        if isinstance(resultat, tuple) and resultat[0] == "Authentification réussie":
            session["utilisateur_id"] = resultat[1]
            session["email"] = email
            return jsonify({"success": True, "message": "Authentification réussie"})

        if resultat == "Email incorrect":
            return jsonify({ "error": "email_incorrect" })
        elif resultat == "Mot de passe incorrect":
            return jsonify({ "error": "mot_de_passe_incorrect" })
        else:
            return jsonify({ "error": "email_et_mot_de_passe_incorrects" })

    return render_template("login.html")



@app.route("/dashboard")
def dashboard():
    if "utilisateur_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html", email=session["email"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/liste")
def liste_utilisateurs():
    if "utilisateur_id" not in session:
        return redirect("/login")

    conn = get_db_connection()
    utilisateurs = conn.execute("SELECT idUtilisateur, email FROM utilisateurs").fetchall()
    conn.close()

    return render_template("liste.html", utilisateurs=utilisateurs)


if __name__ == "__main__":
    app.run(debug=True)
