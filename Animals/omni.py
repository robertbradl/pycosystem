from .animal import Animal


class Omnivore(Animal):
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
        """Initializes an Omnivore object with specific characteristics.

        Args:
            pos (tuple): The position of the Omnivore.
            preys (dict): Dictionary of prey types.
            genoms (dict): Dictionary of genetic information.
            population (dict): Dictionary of population data.
            map (list): The map configuration.
            key (int): Key value for the Omnivore.
            sprite (str): The sprite representing the Omnivore.
            group: The group the Omnivore belongs to.
        """
        super().__init__(pos, genoms, population, map, key, sprite, group)

        self.huntable = preys
        self.prey = None
        self.prey_pos = None

    def alive(self) -> bool or list:  # type: ignore
        """Checks if the Omnivore is alive and handles cleanup on death.

        Returns:
            bool or list: True if alive, False if dead.
        """
        if value := super().alive():
            return value
        self.__cleanup_on_death__()
        return value

    def __find_food__(self) -> None:
        """Finds food based on hunger level, either prey or berries, for the Omnivore."""
        if self.hunger <= 50:
            self.__find_prey__()
        else:
            self.__find_berry__()
