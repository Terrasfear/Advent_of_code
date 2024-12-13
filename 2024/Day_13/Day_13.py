class ClawMachine:
    def __init__(self, description: list[str]):
        self.buttons: dict[str, tuple[int, int]] = self.decode_buttons(description[0:2])
        self.price: tuple[int, int] = self.decode_price(description[2])

        self.position: tuple[int, int] = (0, 0)  # (x,y)

    def decode_buttons(self, button_description_lines: list[str]) -> dict[str, tuple[int, int]]:
        buttons = dict()

        for button_description in button_description_lines:
            button_name, button_behaviour = button_description.removesuffix("\n").split(": ")
            button_name = button_name[-1]
            if button_name not in ["A", "B"]:
                raise Exception(f"wrong button type {button_name}")

            button_behaviour = button_behaviour.split(", ")
            button_behaviour = tuple([int(behaviour[2:]) for behaviour in button_behaviour])

            buttons[button_name] = button_behaviour

        return buttons

    def decode_price(self, price_description_line: str) -> tuple[int, int]:
        price_location = price_description_line.removesuffix("\n").split(": ")[1].split(", ")
        return tuple([int(coordinate[2:]) for coordinate in price_location])

    def button_pressed(self, button: str) -> bool:
        if button in self.buttons:
            self.position = tuple(map(sum, zip(self.position, self.buttons[button])))
            if self.position == self.price:
                return True
            else:
                return False
        else:
            raise Exception(f"unknown button {button}")

    def minimal_tokens(self):
        minimal_presses = self.minimal_presses()
        if minimal_presses == (-1, -1):
            return 0

        return 3 * minimal_presses[0] + minimal_presses[1]

    def minimal_presses(self) -> tuple[int, int]:
        determinant = self.buttons["A"][0] * self.buttons["B"][1] - self.buttons["A"][1] * self.buttons["B"][0]
        A_presses = self.buttons["B"][1] * self.price[0] - self.buttons["B"][0] * self.price[1]
        if A_presses % determinant != 0:
            return -1, -1

        B_presses = - self.buttons["A"][1] * self.price[0] + self.buttons["A"][0] * self.price[1]
        if B_presses % determinant != 0:
            return -1, -1

        return A_presses // determinant, B_presses // determinant


with open("Input", "r") as _file:
    _lines = _file.readlines()

tokens_used1 = 0
tokens_used2 = 0
while _lines:
    machine1 = ClawMachine(_lines[0:3])
    machine2 = ClawMachine(_lines[0:3])
    machine2.price = tuple(map(sum, zip(machine2.price, [10000000000000]*2)))
    _lines = _lines[4:]

    tokens_used1 += machine1.minimal_tokens()
    tokens_used2 += machine2.minimal_tokens()

print(f"Part 1: {tokens_used1}")
print(f"Part 2: {tokens_used2}")
