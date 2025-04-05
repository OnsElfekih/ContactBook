from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "votre_clé_secrète"

def get_db_connection():
    conn = sqlite3.connect("carnet_contacts.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return redirect("/signup")

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
        email = request.form["email"]
        motdepasse = request.form["password"]

        conn = get_db_connection()
        utilisateur = conn.execute(
            "SELECT * FROM utilisateurs WHERE email = ? AND motdepasse = ?",
            (email, motdepasse)
        ).fetchone()
        conn.close()

        if utilisateur:
            session["utilisateur_id"] = utilisateur["idUtilisateur"]
            session["email"] = utilisateur["email"]
            return redirect("/dashboard")
        else:
            return "Email ou mot de passe incorrect."

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
