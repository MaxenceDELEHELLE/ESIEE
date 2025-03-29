# Define the Room class.
"""La classe Room est définie dans ce fichier"""

class Room:
    """
    A class to represent a room in a game.

    Attributes:
        name (str): The name of the room.
        description (str): A description of the room.
        inventory (set): The items in the room.
        exits (dict): The exits from the room.
        character (dict): The characters present in the room.
    """

    def __init__(self, name, description, locked):
        """
        Initialize the Room object with a name, description, and default attributes.
        
        Args:
            name (str): The name of the room.
            description (str): A description of the room.
        """
        self.name = name
        self.description = description
        self.inventory = set()
        self.exits = {}
        self.character = {}
        self.locked = locked
        self.code = ""

    def get_exit(self, direction):
        """
        Get the room in the specified direction, if it exists.
        
        Args:
            direction (str): The direction to check for an exit.
        
        Returns:
            Room or None: The room in the specified direction, or None if no exit exists.
        """
        return self.exits.get(direction)

    def get_exit_string(self):
        """
        Get a string describing the room's exits.
        
        Returns:
            str: A comma-separated string of exits.
        """
        return "Sorties: " + ", ".join(self.exits)

    def get_long_description(self):
        """
        Get a detailed description of the room, including its exits.
        
        Returns:
            str: A description of the room.
        """
        return f"\nVous êtes dans {self.name}. {self.description}\n\n{self.get_exit_string()}\n"

    def get_inventory(self):
        """
        Get a description of the room's inventory and characters.
        
        Returns:
            str: A description of the room's contents.
        """
        if not self.inventory and not self.character:
            return "La pièce est vide."

        inventory_description = ""
        if self.inventory:
            inventory_description += "La pièce contient :\n"
            inventory_description += ''.join(f"    - {str(item)}\n" for item in self.inventory)

        character_description = ""
        if self.character:
            character_description += ''.join(
                f"    - {str(character)}\n"
                for character in self.character.values()
            )


        return inventory_description + character_description
