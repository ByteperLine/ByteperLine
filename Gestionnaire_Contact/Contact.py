import json
import os
import sys

FILENAME = "list_contact/contact.json"
os.makedirs(os.path.dirname(FILENAME), exist_ok=True)
first_time = True

def search_contact():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as file:
            try:
                contacts = json.load(file)
            except json.JSONDecodeError:
                contacts = []
    else:
        contacts = []
    
    if not contacts:
        print("Aucun contact enregistré.")
        return

    while True:
        search = input("Entrez une lettre ou un mot-clé pour chercher un contact : ").strip().lower()

        results = []
        for contact in contacts:
            if (contact["Nom_de_famille"].lower().startswith(search) or
                contact["Prénom"].lower().startswith(search)):
                results.append(contact)

        if results:
            print(f"\nRésultats pour '{search}' :")
            for i, result in enumerate(results, 1):
                print(f"\nContact {i}:")
                for key, value in result.items():
                    print(f"  {key} : {value}")
        else:
            print("Aucun contact trouvé.")

        while True:
            again = input("\nRechercher un autre contact ? (O/N) ").strip().lower()
            if again == "n":
                break
            elif again == "o":
                start()
            else:
                print("Choix incorrect.")
                continue

def save_contact(contact):
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as file:
            try:
                contacts = json.load(file)
            except json.JSONDecodeError:
                contacts = []
    else:
        contacts = []

    contacts.append(contact)

    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4, ensure_ascii=False)

def add_contacts():
    first_number = ["01", "02", "03", "04", "05", "06", "07", "08", "09"]
    suffix_email = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com", "protonmail.com",
                    "orange.fr", "sfr.fr", "laposte.net", "live.com", "free.fr", "wanadoo.fr", "bouyguestelecom.fr",
                    "gmx.com", "mail.com"]
    new_contact = None
    while True:
        last_name = input("Nom de famille : ").strip()

        if last_name == "":
            print("Le nom de famille doit être défini.")
            continue

        break

    while True:
        first_name = input("Prénom : ").strip()

        if first_name == "":
            print("Le prénom doit être défini.")
            continue
        
        break

    while True:
        number = input("Numéro : ").strip()
        number = number.replace(" ", "")

        if not any(number.startswith(prefix) for prefix in first_number):
            print("Le numéro de téléphone est incorrect.")
            continue

        if not number.isdigit():
            print("Le numéro de téléphone est incorrect.")
            continue

        if len(number) != 10:
            print("Le numéro de téléphone est incorrect.")
            continue
        
        break

    while True:
        email = input("Email : ").strip()
        print()

        if not any(email.endswith(f"@{su}") for su in suffix_email) or email.startswith("@"):
            print("Email incorrect.")
            continue
        
        break
    
    new_contact = {
        "Nom_de_famille": last_name.capitalize(),
        "Prénom": first_name.capitalize(),
        "Numéro_de_tel": number,
        "Email": email
    }

    for key, value in new_contact.items():
        print(f"\t{key} : {value}")

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
                
                if key_to_modify == "Numéro_de_tel":
                    if not new_value.isdigit() or len(new_value) != 10 or not any(new_value.startswith(prefix) for prefix in first_number):
                        print("Numéro de téléphone incorrect.")
                        continue
                
                if key_to_modify == "Email":
                    if not any(new_value.endswith(f"@{su}") for su in suffix_email):
                        print("Email incorrect.")
                        continue
                
                new_contact[key_to_modify] = new_value.capitalize() if "Nom" in key_to_modify or "Prénom" in key_to_modify else new_value
                print(f"{key_to_modify} modifié.\n")

                for k, v in new_contact.items():
                    print(f"\t{k} : {v}")

                for i, key in enumerate(keys, 1):
                    print(f"\t{i}. {key} : {new_contact[key]}")

                while True:
                    cont_mod = input("Voulez-vous modifier un autre champ ? (O/N) ").lower()
                    if cont_mod == "o":
                        start()
                    elif cont_mod == "n":
                        break
                    else:
                        print("Choix incorrect.")
                
                continue
        else:
            print("Choix incorrect.")
            
def start():
    global first_time

    if first_time == True:
        print("Bienvenue sur le gestionnaire de contact.")
    print("1. Rechercher un contact\n2. Créer un contact\n3. Quitter")
    first_time = False

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

start()
