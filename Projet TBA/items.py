# pylint: disable=too-few-public-methods

"""Classe Items qui définit les objets prenables par le joueur"""

class Item :
    """Les caracteristiques de la classe sont le nom, le poids et la description de l'objet"""

    def __init__(self, name, description, weight):
        self.name = name
        self. description = description
        self.weight = weight

    def __str__(self):
        return f"{self.name} : {self.description} ({self.weight} kg)"
