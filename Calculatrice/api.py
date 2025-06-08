from flask import Flask, request, jsonify, render_template

# Initialisation de l'application Flask
app = Flask(__name__)

# Route principale qui affiche le formulaire HTML
@app.route("/")
def form():
    return render_template("index.html")  # Assure-toi que ce fichier existe dans le dossier "templates"

# Route pour effectuer un calcul via une requête POST
@app.route("/calcul", methods=["POST"])
def calcul():
    # Récupère les données JSON envoyées par le client
    data = request.get_json()

    # Récupère les valeurs de 'a', 'b' et 'operation' dans les données
    a = data.get("a")
    b = data.get("b")
    operation = data.get('operation')

    # Vérifie que a et b sont bien présents
    if a is None or b is None:
        return jsonify({"Erreur": "aucun calcul n'est fait"}), 400

    # Tente de convertir a et b en float
    try:
        a = float(a)
        b = float(b)
    except (ValueError, TypeError):
        return jsonify({"Erreur": "a et b doivent être des nombres"}), 400

    # Effectue l'opération demandée
    if operation == "addition":
        c = a + b
    elif operation == "soustraction":
        c = a - b
    elif operation == "multiplication":
        c = a * b
    elif operation == "division":
        # Vérifie qu'on ne divise pas par 0
        if b == 0:
            return jsonify({"Erreur": "division par zéro"}), 400
        c = a / b
    else:
        return jsonify({"Erreur": "opération non reconnue"}), 400

    # Retourne le résultat sous forme de JSON
    return jsonify({"resultat": c})

# Point d'entrée du programme
if __name__ == "__main__":
    app.run(debug=True)  # Mode debug activé pour voir les erreurs dans le terminal
