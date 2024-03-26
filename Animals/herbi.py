from .animal import Animal


class Herbivore(Animal):
    def __init__(
        self,
        pos: tuple,
        genoms: dict,
        population: dict,
        map: list,
        key: int,
        sprite: str,
        group,
    ) -> None:
        """Initializes a Herbivore object with specific characteristics.

        Args:
            pos (tuple): The position of the Herbivore.
            genoms (dict): Dictionary of genetic information.
            population (dict): Dictionary of population data.
            map (list): The map configuration.
            key (int): Key value for the Herbivore.
            sprite (str): The sprite representing the Herbivore.
            group: The group the Herbivore belongs to.
        """
        super().__init__(pos, genoms, population, map, key, sprite, group)

        self.hunted = False
        self.hunter = None

    def __cleanup_on_death__(self) -> None:
        """Cleans up on death by resetting variables for the Herbivore and its hunter."""
        super().__cleanup_on_death__()
        if self.hunted:
            self.hunter.food_found = False
            self.hunter.food_point = None
            self.hunter.prey = None
            self.hunter.queued_movements = []
            self.hunter.path_length = None

    def alive(self) -> bool or list:  # type: ignore
        """Checks if the Herbivore is alive, handles interactions with its hunter, and cleans up on death.

        Returns:
            bool or list: True if alive, False if dead.
        """
        if self.hunted:
            self.hunter.queued_movements.append(self.__convert_pos__(self.pos))
            self.hunter.food_point = self.__convert_pos__(self.pos)
            if self.hunter.pos == self.pos:
                self.hunter.hunger -= 350 * (20 - self.hunter.hunger_rate)
                self.__cleanup_on_death__()
                return False

        if value := super().alive():
            return value
        self.__cleanup_on_death__()
        return False

    def __find_food__(self) -> None:
        """Finds food (berries) for the Herbivore."""
        self.__find_berry__()
