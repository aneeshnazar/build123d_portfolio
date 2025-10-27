from itertools import product
from build123d import Align, Axis, BasePartObject, Box, BuildPart, Cylinder, Face, Locations, Mode, Vector, VectorLike, fillet


class TabletFeature(BasePartObject):
    align_values = [m for m in Align if m.value != None]
    
    @classmethod
    def get_relative_position(
        cls,
        face : Face,
        size : VectorLike,
        offset : tuple[float, float],
        align : tuple[Align, Align] = (Align.CENTER, Align.CENTER)
    ):
        size_vector = Vector(size)
        corrected_offset = tuple(
            map(
                lambda x : -x[0] if x[1] == Align.MAX else x[0],
                zip(offset, align)
            )
        )

        flat_face_dims = tuple(sorted(filter(lambda x: x > 0.00001, face.oriented_bounding_box().size)))
        bounds = tuple(
            map(
                lambda x: (-x, 0, x),
                map(
                    lambda x: (x[0] - x[1]) / 2,
                    zip(
                        flat_face_dims,
                        [size_vector.X, size_vector.Y]
                    )
                )
            )
        )
        
        align_map = dict(zip(list(product(cls.align_values, cls.align_values)), list(product(*bounds))))
        return tuple(
            map(
                lambda x: max(min(x[0] + x[1], x[2][2]), x[2][0]),
                zip(align_map[align], corrected_offset, bounds)
            )
        )

class Button(TabletFeature):
    def __init__(
        self,
        face : Face,
        size : VectorLike,
        offset : tuple[float, float],
        align : tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.MIN)
    ):
        size_vector = Vector(size)
        pos = self.get_relative_position(face, size, offset, align[:2])
        with BuildPart(face) as b:
            with Locations(pos):
                b1 = Box(size_vector.X, size_vector.Y, size_vector.Z, align=(Align.CENTER, Align.CENTER, align[2]))
                a = Axis(face.center(), face.normal_at(0.5,0.5))
                fillet(b1.edges().filter_by(a), min(size) / 3)
        super().__init__(part=b.solid(), rotation=(0,0,0), mode=Mode.ADD)

class Port(TabletFeature):
    def __init__(
        self,
        face : Face,
        size : VectorLike,
        offset : tuple[float, float],
        align : tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.MIN)
    ):
        size_vector = Vector(size)
        pos = self.get_relative_position(face, size, offset, align[:2])
        with BuildPart(face) as b:
            with Locations(pos):
                b1 = Box(size_vector.X, size_vector.Y, size_vector.Z, align=(Align.CENTER, Align.CENTER, align[2]))
                a = Axis(face.center(), face.normal_at(0.5,0.5))
                fillet(b1.edges().filter_by(a), min(size) / 3)
        super().__init__(part=b.solid(), rotation=(0,0,0), mode=Mode.SUBTRACT)

class CameraBump(TabletFeature):
    def __init__(
        self,
        face : Face,
        radius : float,
        thickness : float,
        offset : tuple[float, float],
        align : tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.MIN)
    ):
        pos = self.get_relative_position(face, [radius * 2, radius * 2], offset, align[:2])
        with BuildPart(face) as b:
            with Locations((pos[1], pos[0])):
                Cylinder(radius, thickness, align=(Align.CENTER, Align.CENTER, align[2]))
        super().__init__(part=b.solid(), rotation=(0,0,0), mode=Mode.ADD)