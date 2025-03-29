# Description: Game class
# Import modules
"""Classe Game qui fait tourner le jeu avec play(), setup() et process_command()"""

from room import Room
from player import Player
from command import Command
from actions import Actions
from items import Item
from character import Character


class Game:
    """Definition de la classe Game"""
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.pnj = []

    # pylint: disable=too-many-locals, too-many-statements
    # Setup the game
    def setup(self):
        """Setup permet de parametrer les salles, les pnj et les items"""
        # Setup commands

        help_1 = Command("help", " : Afficher cette aide", Actions.help, 0)
        self.commands["help"] = help_1
        quit_1 = Command("quit", " : Quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit_1
        go = Command("go", " <direction> : Se déplacer dans une direction cardinale (N, E, S, O) "
        "ou aller de haut en bas (U, D)", Actions.go, 1)
        self.commands["go"] = go
        back = Command("back", " : Revenir en arrière", Actions.back, 0)
        self.commands["back"] = back
        check = Command("check", " : Afficher l'inventaire du joueur", Actions.check, 0)
        self.commands["check"] = check
        look = Command("look" , " : Regarder autour de soi", Actions.look, 0)
        self.commands["look"] = look
        take = Command("take", " : Prendre un objet", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " : Déposer un objet", Actions.drop, 1)
        self.commands["drop"] = drop
        talk = Command("talk", " : Parler à un PNJ", Actions.talk, 1)
        self.commands["talk"] = talk
        enter = Command("enter", " : Ouvre la page de navigation de l'ordinateur", Actions.enter, 1)
        self.commands["enter"] = enter
    # Ajout des commandes au dictionnaire

        # Setup rooms

        hall=Room("le hall d'acceuil de la tour",
        "Vous avez les mains moites, il ne faut surtout pas se faire repérer.", False)
        self.rooms.append(hall)
        ascenseur=Room("l'ascenseur",
        "Vous êtes seul, silencieux. Direction le 52ème étage.", False)
        self.rooms.append(ascenseur)
        couloir1 = Room("un long couloir interminable", "", False)
        self.rooms.append(couloir1)
        couloir2 = Room("même couloir qui se prolonge", "", False)
        self.rooms.append(couloir2)


        bureau1 = Room("le bureau de comptabilité",
        "L'argent de l'entreprise est géré ici.", False)
        self.rooms.append(bureau1)
        bureau2 = Room("le bureau de gestion du personnel.",
        "Les RH travaillent ici.", False)
        self.rooms.append(bureau2)
        bureau3 = Room("le bureau de trading",
        "L'ambiance est électrique. Les traders crient de partout"
        " et se battent entre eux.", True)
        self.rooms.append(bureau3)
        bureau4 = Room("le bureau des managers",
        "Les managers discutent de la nouvelle tendance à la mode, le management Lean.", False)
        self.rooms.append(bureau4)


        bureau5 = Room("le placard à balais", "La pièce est sombre et humide", False)
        self.rooms.append(bureau5)
        bureau6 = Room("le bureau du patron",
        "Tout est bien ordonné à sa place. Faites vite, il pourrait revenir à tout instant.", True)
        self.rooms.append(bureau6)


        # Create exits for rooms

        hall.exits = {"N" : ascenseur}

        ascenseur.exits = {"N" : couloir1}


        couloir1.exits = {"N" : couloir2, "E" : bureau1, "S" : ascenseur, "O" : bureau2}
        bureau1.exits = {"N" : bureau3, "E" : None, "S" : None, "O" : couloir1, "D": bureau5}
        bureau2.exits = {"N" : bureau4, "E" : couloir1, "O" : None, "S" : None, "U" : bureau6}
        bureau3.exits = {"N" : None, "U" : None, "S" : bureau1, "O" : couloir2, "D" : bureau5}
        bureau4.exits = {"U" : bureau6, "E" : couloir2, "S" : bureau2, "O" : None, "N" : None}
        bureau5.exits = {"U" : bureau1, "E" : None, "S" : None, "O" : None, "N" : None}
        bureau6.exits = {"U" : None, "E" : None, "S" : None, "O" : None, "N" : None, "D" : bureau2}
        couloir2.exits = {"N" : None, "E" : bureau3, "S" : couloir1, "O" : bureau4}

        bureau3.code = "2549"


       # Objets
        bureau3.inventory.add(Item("Clé",
        "Une clé qui scintille et qui attire votre attention", 0.2))
        bureau1.inventory.add(Item("Ordinateur",
        "Il est déverouillé, étrange. Le fichier de comptabilité de cette année est affiché."
        " enter Ordinateur permet d'afficher la fenêtre", 23))
        bureau6.inventory.add(Item("Documents", "Les fameux fichiers qui"
        " prouvent l'assassinat de Ben Fisher", 0.6))
        bureau4.inventory.add(Item("Machine", "Du café bien chaud", 400))
        bureau5.inventory.add(Item("Balai", "Un simple balai",4))

        # PNJ dans les salles

        hall.character["Hôtesse"] = Character("Hôtesse",
        "Une femme au guichet d'acceuil", hall, ["Bienvenue chez BlackStone"])
        couloir1.character["Traders"] = Character("Traders",
        "Deux hommes bien habillés et l'air soucieux", couloir1,
        ["J'ai entendu dire qu'un journaliste voulait mettre son nez dans nos affaires.",
        "Le comptable a ecnore changé les codes"])
        bureau3.character["RH"] = Character("RH",
        "Une femme à l'air sérieux et sévère", bureau3,
        ["Il a fait perdre 5 milliards à l'entreprise, j'étais obligée de le virer."])
        couloir2.character["Comptable"] = Character("Comptable",
        "Un homme à l'air banal", couloir2, ["Je vais "
        "me chercher un café",
        "Je suis satisfait, l'entreprise a enregistré des performances record cette année", 
        "Ah les traders, le gain, ils n'ont que ce mot à la bouche"])
        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "), hall)
        self.player.current_room = hall


    def win(self):
        """ Scénario gagnant """
        for i in self.player.inventory:
            if i == "Documents" and self.player.current_room.name == "le bureau du patron":
                print("Vous avez récupéré les Documents."
                " Échappez-vous du bâtiment avant qu'il ne soit trop tard.")
            if self.player.current_room.name == "le hall d'acceuil de la tour" and i == "Documents":
                print("Vous avez mené votre infiltration avec succès."
                " Vous vous êtes échappé. Un taxi vient vous récupérer."
                " Le PDG de BlackStone démissionne quelques jours après" 
                "la publication de l'article. La justice a un prix.")
                self.finished = True

    def loose(self):
        """Scenario perdant"""
        for i in self.player.inventory:
            if i == "Documents" :
                if self.player.current_room.name == "le bureau de comptabilité":
                    print("Les caméras de surveillance vous voient avec les documents dans la main."
                    "La sécurité se jette sur vous. Vous avez perdu")
                    self.finished = True

    # Play the game
    def play(self):
        """fonction play qui fait tourner le jeu de manière itérative"""
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
            self.win()
            self.loose()



    # Process the command entered by the player
    def process_command(self, command_string) -> None:
        """Traduit les commandes clavier en objet python"""
        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]
        if not command_word :
            return
        # If the command is not recognized, print an error message
        if command_word == "go" :
            for room in self.rooms :
                for pnj in list(room.character.values()) :
                    pnj.move()
        if command_word not in self.commands:
            print(f"\nCommande '{command_word}' non reconnue."
            " Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it

        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)


    # Print the welcome message
    def print_welcome(self):
        """fonction d'affiche du message de début"""
        print(f"\nDISCLAIMER : Toute ressemblance avec des faits réels ou "
      "avec des personnes existantes ou ayant existé serait purement fortuite."
      f"\nÉlise Lucet : Bon {self.player.name}, on a absolument besoin des documents "
      "qui prouvent que Ben Fisher a été assassiné par BlackStone suite à son "
      "investigation sur les puits de pétrole au Groënland.")
        print("Entrez 'help' si vous avez besoin d'aide.")

        #
        print(self.player.current_room.get_long_description())


def main():
    """fonction main"""
    game = Game()  # Passer root à la classe Game
    game.play()  # Commencer le jeu

if __name__ == "__main__":
    main()
