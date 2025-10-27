## Braille
from build123d import Align, BasePartObject, BuildPart, BuildSketch, Locations, Mode, Part, Pos, Rectangle, ShapeList, Sphere, extrude


class BrailleLetter(BasePartObject):
    actual_map = {
        'a' : 0b000100,
        'b' : 0b000110,
        'c' : 0b100100,
        'd' : 0b110100,
        'e' : 0b010100,
        'f' : 0b100110,
        'g' : 0b110110,
        'h' : 0b010110,
        'i' : 0b100010,
        'j' : 0b110010,
        'k' : 0b000101,
        'l' : 0b000111,
        'm' : 0b100101,
        'n' : 0b110101,
        'o' : 0b010101,
        'p' : 0b100111,
        'q' : 0b110111,
        'r' : 0b010111,
        's' : 0b100011,
        't' : 0b110011,
        'u' : 0b001101,
        'v' : 0b001111,
        'w' : 0b111010,
        'x' : 0b101101,
        'y' : 0b111101,
        'z' : 0b011101,
    }
    def __init__(self, size, mask : str, rotation=(0,0,0), align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.ADD):
        letter_map = f"{self.actual_map[mask.lower()[0]]:06b}"
        gl = Locations(list(map(
            lambda x: x[1],
            filter(
                lambda x: x[0], zip(list(map(lambda x: int(x), letter_map)), [
                    (size / 2, size),
                    (size / 2, 0),
                    (size / 2, -size),
                    (-size / 2, size),
                    (-size / 2, 0),
                    (-size / 2, -size)
                ])
                )
           )        
        ))
        
        with BuildPart() as backing:
            with BuildSketch():
                Rectangle(2 * size, 3 * size)
            extrude(amount = -1)
            if len(list(gl)):
                with gl:
                    Sphere(size / 4)
        if backing.part is None:
            raise Exception("Failed to create BrailleLetter")
        super().__init__(backing.part, rotation, align, mode)

class BrailleWord(BasePartObject):
    def __init__(self, size, word: str, rotation=(0,0,0), align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.ADD):
        tile = (Part() + ShapeList([Pos(i * size * 2, 0) * BrailleLetter(size, letter) for i, letter in enumerate(word)])).solid()
        if tile is None:
            raise Exception("Failed to create BrailleWord")
        super().__init__(tile, rotation, align, mode)
        self.name = word + " in Braille"