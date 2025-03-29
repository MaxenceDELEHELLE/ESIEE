"Definition de la classe Character"

import random
DEBUG = False



class Character:
    """Class representing a character in the game."""

    def __init__(self, name, description, current_room, msg):
        """Initialize a character with a name, description, current room, and messages."""
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msg = msg

    def __str__(self):
        return f"{self.name} : {self.description}"

    def move(self):
        """Move the character to a random adjacent room if possible."""
        exits = list(self.current_room.exits)
        if random.choice([True, False]):
            new_direction = random.choice(exits)
            next_room = self.current_room.exits[new_direction]

            if next_room is None:
                if DEBUG:
                    print(f"{self.name} est en face d'une porte donc ne bouge pas de salle")
                return False

            del self.current_room.character[self.name]
            self.current_room = next_room

            if DEBUG:
                print(f"{self.name} est dans {next_room.name}")

            self.current_room.character[self.name] = Character(
                self.name, self.description, self.current_room, self.msg
            )
            return True

        if DEBUG:
            print(f"{self.name} ne bouge pas")
        return False

    def get_msg(self):
        """Retrieve the next message in a cyclical manner."""
        if not self.msg:
            raise ValueError("La liste des messages ne peut pas être vide.")

        # Remove and return the first message, then re-add it to the end of the list
        message = self.msg.pop(0)
        self.msg.append(message)
        return message
