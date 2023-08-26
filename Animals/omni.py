from Animals.animal import Animal


class Omnivore(Animal):

    def __init__(self, pos: tuple, preys: dict, genoms: dict, population: dict, map: list, key: int, sprite: str, group) -> None:
        super().__init__(pos, genoms, population, map, key, sprite, group)

        self.huntable = preys
        self.prey = None
        self.prey_pos = None

    def alive(self) -> bool or list:
        value = super().alive()
        if not value:
            self.__cleanup_on_death__()
            return False
        else:
            return value

    def __find_food__(self) -> None:
        if self.hunger <= 50:
            self.__find_prey__()
        else:
            self.__find_berry__()