"""
 Module actions: contient les fonctions pour exécuter les commandes du jeu.
"""

import tkinter as tk
from tkinter import PhotoImage


# Messages d'erreur pour les commandes avec paramètres incorrects.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:
    """
    Classe Actions contenant les commandes disponibles pour le jeu.
    """

    def __init__(self):
        pass

    @staticmethod
    def go(game, list_of_words, number_of_parameters):
        """
        Permet de déplacer le joueur dans une direction donnée.
        """
        joueur = game.player
        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        directions = {
            "NORD": "N", "nord": "N", "n": "N", "Nord": "N", "N" : "N",
            "EST": "E", "E": "E", "est": "E", "e": "E", "Est": "E",
            "SUD": "S", "S": "S", "sud": "S", "s": "S", "Sud": "S",
            "OUEST": "O", "O": "O", "ouest": "O", "o": "O", "Ouest": "O",
            "UP" : "U", "U" : "U", "up": "U", "u": "U", "Up": "U",
            "DOWN" : "D", "d" : "D", "Down" : "D", "D" : "D"
        }

        direction = directions.get(list_of_words[1], None)
        if direction :
            joueur.move(direction)
            return True
        print("Direction non valide.")
        return False

    @staticmethod
    def quit(game, list_of_words, number_of_parameters):
        """
        Permet de quitter le jeu.
        """
        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        joueur = game.player
        print(f"\nMerci {joueur.name} d'avoir joué. Au revoir.\n")
        game.finished = True
        return True

    @staticmethod
    def help(game, list_of_words, number_of_parameters):
        """
        Affiche la liste des commandes disponibles.
        """
        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print(f"\t- {command}")
        print()
        return True

    @staticmethod
    def back(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de revenir à la salle précédente.
        """
        joueur = game.player
        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        if not joueur.history:
            joueur.current_room = joueur.hall
            print(joueur.current_room.get_long_description())
            return False

        previous_room = joueur.history.pop()
        joueur.current_room = previous_room
        print(f"Vous êtes revenu dans : {previous_room.name}.")
        print(joueur.current_room.get_long_description())
        return True

    @staticmethod
    def check(game, list_of_words, number_of_parameters):
        """
        Affiche l'inventaire du joueur.
        """
        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        print(game.player.get_inventory())
        return True

    @staticmethod
    def look(game, list_of_words, number_of_parameters):
        """
        Affiche l'inventaire de la salle actuelle.
        """
        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        print(game.player.current_room.get_inventory())
        return True

    @staticmethod
    def take(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de prendre un objet dans la salle actuelle.
        """
        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        item_name = list_of_words[1]
        room_inventory = game.player.current_room.inventory
        a = 0
        objet_trouve = False

        for item in room_inventory:
            a += item.weight
            if item_name == item.name:
                objet_trouve = True
                if a < game.player.max_weight:
                    game.player.inventory[item.name] = item
                    room_inventory.remove(item)
                    print(f"Vous avez pris {item.name}.")
                    return True
                print("Objet trop lourd. Vous n'avez pas besoin de le transporter.")
                return False
        if not objet_trouve :
            print("Objet non trouvé.")
            return False
        return None

    @staticmethod
    def drop(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de lâcher un objet de son inventaire dans la salle actuelle.
        """
        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        item_name = list_of_words[1]
        player_inventory = game.player.inventory

        if item_name in player_inventory:
            item = player_inventory.pop(item_name)
            game.player.current_room.inventory.add(item)
            print(f"Vous avez lâché {item_name}.")
            return True

        print("Objet non trouvé dans votre inventaire.")
        return False

    @staticmethod
    def talk(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de parler à un PNJ dans la salle actuelle.
        """
        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False  # Il semble que cela soit fait pour gérer une erreur de syntaxe.

        npc_name = list_of_words[1]
        room_characters = game.player.current_room.character

        if npc_name in room_characters:
            message = room_characters[npc_name].get_msg()
            print(message)
            return True  # Le joueur a parlé avec le PNJ, renvoie True pour signifier le succès.

        print("Personnage non trouvé dans la salle.")
        return False  # Si le personnage n'est pas trouvé, retourne False pour l'échec.

    @staticmethod
    def enter(game, list_of_words, number_of_parameters):
        """Permet d'entrer sur l'ordinateur"""

        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False  # Il semble que cela soit fait pour gérer une erreur de syntaxe.
        b = game.player
        if b == 1 :
            print("erreur")
        a = list_of_words[1]
        if a == "Ordinateur" :
            # Crée la fenêtre principale
            root = tk.Tk()
            root.title("Relevés Bancaires 2021-2024")
            # Définir la taille de la fenêtre
            root.geometry("700x600")

# Charger l'image
            image_path = "bl.png"  # Remplace par le chemin de ton image
            image = PhotoImage(file=image_path)

# Redimensionner l'image pour s'ajuster à la taille de la fenêtre (600x400)
# Utilisation de la méthode zoom de PhotoImage pour ajuster l'image à la fenêtre
            resized_image = image.subsample(int(image.width() / 600), int(image.height() / 400))

# Créer un label pour afficher l'image redimensionnée
            label_image = tk.Label(root, image=resized_image)
            label_image.pack()

# Afficher les relevés bancaires
            text = """
            Relevés Bancaires:
            2021 : 453 millions $
            2022 : 729 millions $
            2023 : 1547 millions $
            2024 : 2549 millions $
            """

# Ajouter un label pour afficher les informations bancaires
            label_text = tk.Label(root, text=text, font=("Helvetica", 14), bg="lightgrey")
            label_text.pack()

# Lancer l'interface graphique
            root.mainloop()
            return True
        return False
