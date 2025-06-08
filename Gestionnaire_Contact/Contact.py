import json
import os
import sys

# Chemin du fichier JSON contenant les contacts
FILENAME = "list_contact/contact.json"
# Création du dossier s’il n’existe pas
os.makedirs(os.path.dirname(FILENAME), exist_ok=True)

# Indicateur pour la première utilisation
first_time = True

# Fonction pour rechercher un contact dans le fichier JSON
def search_contact():
    # Lecture des contacts existants
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as file:
            try:
                contacts = json.load(file)
            except json.JSONDecodeError:
                contacts = []
    else:
        contacts = []

    # Si aucun contact n’est enregistré
    if not contacts:
        print("Aucun contact enregistré.")
        return

    # Boucle de recherche
    while True:
        search = input("Entrez une lettre ou un mot-clé pour chercher un contact : ").strip().lower()

        # Recherche des contacts correspondant au critère
        results = []
        for contact in contacts:
            if (contact["Nom_de_famille"].lower().startswith(search) or
                contact["Prénom"].lower().startswith(search)):
                results.append(contact)

        # Affichage des résultats
        if results:
            print(f"\nRésultats pour '{search}' :")
            for i, result in enumerate(results, 1):
                print(f"\nContact {i}:")
                for key, value in result.items():
                    print(f"  {key} : {value}")
        else:
            print("Aucun contact trouvé.")

        # Recommencer ou quitter la recherche
        while True:
            again = input("\nRechercher un autre contact ? (O/N) ").strip().lower()
            if again == "n":
                start()
            elif again == "o":
                break
            else:
                print("Choix incorrect.")
                continue
        continue

# Fonction pour sauvegarder un contact dans le fichier JSON
def save_contact(contact):
    # Lecture des contacts existants
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as file:
            try:
                contacts = json.load(file)
            except json.JSONDecodeError:
                contacts = []
    else:
        contacts = []

    # Ajout du nouveau contact
    contacts.append(contact)

    # Écriture dans le fichier JSON
    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4, ensure_ascii=False)

# Fonction pour ajouter un contact
def add_contacts():
    # Listes pour la validation des numéros et des emails
    first_number = ["01", "02", "03", "04", "05", "06", "07", "08", "09"]
    suffix_email = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com", "protonmail.com",
                    "orange.fr", "sfr.fr", "laposte.net", "live.com", "free.fr", "wanadoo.fr", "bouyguestelecom.fr",
                    "gmx.com", "mail.com"]

    new_contact = None

    # Saisie du nom
    while True:
        last_name = input("Nom de famille : ").strip()
        if last_name == "":
            print("Le nom de famille doit être défini.")
            continue
        break

    # Saisie du prénom
    while True:
        first_name = input("Prénom : ").strip()
        if first_name == "":
            print("Le prénom doit être défini.")
            continue
        break

    # Saisie et vérification du numéro
    while True:
        number = input("Numéro : ").strip().replace(" ", "")
        if not any(number.startswith(prefix) for prefix in first_number):
            print("Le numéro de téléphone est incorrect.")
            continue
        if not number.isdigit() or len(number) != 10:
            print("Le numéro de téléphone est incorrect.")
            continue
        break

    # Saisie et vérification de l'email
    while True:
        email = input("Email : ").strip()
        print()
        if not any(email.endswith(f"@{su}") for su in suffix_email) or email.startswith("@"):
            print("Email incorrect.")
            continue
        break

    # Création du contact
    new_contact = {
        "Nom_de_famille": last_name.capitalize(),
        "Prénom": first_name.capitalize(),
        "Numéro_de_tel": number,
        "Email": email
    }

    # Affichage du contact avant confirmation
    for key, value in new_contact.items():
        print(f"\t{key} : {value}")

    # Confirmation ou modification
    while True:
        choice = input("Est-ce bien cela ? (O,N) ").lower()

        if choice == "o":
            print("Contact enregistré.")
            save_contact(new_contact)
            start()
        elif choice == "n":
            print("Que voulez-vous modifier ?")
            keys = list(new_contact.keys())
            for i, key in enumerate(keys, 1):
                print(f"\t{i}. {key} : {new_contact[key]}")

            # Choix du champ à modifier
            while True:
                try:
                    mod_choice = int(input("Numéro du champ à modifier : "))
                except ValueError:
                    print("Le choix doit être un nombre.")
                    continue

                if mod_choice < 1 or mod_choice > len(keys):
                    print("Choix incorrect.")
                    continue

                key_to_modify = keys[mod_choice - 1]
                new_value = input(f"Nouvelle valeur pour {key_to_modify} : ").strip()

                # Validation spécifique si le champ est un numéro ou un email
                if key_to_modify == "Numéro_de_tel":
                    if not new_value.isdigit() or len(new_value) != 10 or not any(new_value.startswith(prefix) for prefix in first_number):
                        print("Numéro de téléphone incorrect.")
                        continue

                if key_to_modify == "Email":
                    if not any(new_value.endswith(f"@{su}") for su in suffix_email):
                        print("Email incorrect.")
                        continue

                # Mise à jour du champ
                new_contact[key_to_modify] = new_value.capitalize() if "Nom" in key_to_modify or "Prénom" in key_to_modify else new_value
                print(f"{key_to_modify} modifié.\n")

                # Affichage des nouvelles valeurs
                for k, v in new_contact.items():
                    print(f"\t{k} : {v}")

                for i, key in enumerate(keys, 1):
                    print(f"\t{i}. {key} : {new_contact[key]}")

                # Demande de modification supplémentaire
                while True:
                    cont_mod = input("Voulez-vous modifier un autre champ ? (O/N) ").lower()
                    if cont_mod == "o":
                        start()
                    elif cont_mod == "n":
                        break
                    else:
                        print("Choix incorrect.")
                        continue

                continue
        else:
            print("Choix incorrect.")

# Fonction principale de démarrage
def start():
    global first_time

    if first_time:
        print("Bienvenue sur le gestionnaire de contact.")
    print("1. Rechercher un contact\n2. Créer un contact\n3. Quitter")
    first_time = False

    # Choix utilisateur
    while True:
        try:
            choice = int(input("Que voulez-vous faire ? "))
        except ValueError:
            print("Choix incorrect.")
            continue
        break

    if choice == 1:
        search_contact()
    elif choice == 2:
        add_contacts()
    elif choice == 3:
        print("Aurevoir !")
        sys.exit()
    else:
        print("Choix incorrect.")

# Lancement du programme
start()
