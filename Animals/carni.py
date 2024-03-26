from .animal import Animal


class Carnivore(Animal):
    def __init__(
        self,
        pos: tuple,
        preys: dict,
        genoms: dict,
        population: dict,
        map: list,
        key: int,
        sprite: str,
        group,
    ) -> None:
        """Initializes a Carnivore object with specific characteristics.

        Args:
            pos (tuple): The position of the Carnivore.
            preys (dict): Dictionary of prey types.
            genoms (dict): Dictionary of genetic information.
            population (dict): Dictionary of population data.
            map (list): The map configuration.
            key (int): Key value for the Carnivore.
            sprite (str): The sprite representing the Carnivore.
            group: The group the Carnivore belongs to.

        """
        super().__init__(pos, genoms, population, map, key, sprite, group)

        self.huntable = preys
        self.prey = None
        self.prey_pos = None

    def alive(self) -> bool or list:  # type: ignore
        """Checks if the Carnivore is alive and handles cleanup on death.

        Returns:
            bool or list: True if alive, False if dead.

        """
        if value := super().alive():
            return value
        self.__cleanup_on_death__()
        return False

    def __find_food__(self) -> None:
        """Finds food for the Carnivore."""
        self.__find_prey__()
