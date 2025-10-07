import math

from build123d import BasePartObject, BuildPart, VectorLike, Mode, validate_inputs, Solid, Face, Wire, Plane, ShapeList, Part

class HexBoreHole(BasePartObject):
    _applies_to = [BuildPart._tag]

    def __init__(
        self,
        radius: float,
        hex_radius: float,
        counter_bore_depth: float,
        depth: float | None = None,
        rotation: VectorLike = (0, 0, 0),
        mode: Mode = Mode.SUBTRACT
    ):
        context: BuildPart | None = BuildPart._get_context(self)
        validate_inputs(context, self)

        self.radius = radius
        self.hex_radius = hex_radius
        self.counter_bore_depth = counter_bore_depth
        if depth is not None:
            self.hole_depth = depth
        elif depth is None and context is not None:
            self.hole_depth = context.max_dimension
        else:
            raise ValueError("No depth provided")
        self.mode = mode

        pts = [(hex_radius * math.cos(x * math.pi / 3), hex_radius * math.sin(x * math.pi / 3), 0) for x in range(6)]

        fused = Solid.extrude(
            Face(Wire.make_polygon(pts)),
            (0, 0, -self.counter_bore_depth)
        ).fuse(
            Solid.make_cylinder(
                radius=self.radius,
                height=self.hole_depth,
                plane = -Plane((0, 0, -counter_bore_depth))
            )
        )
        if isinstance(fused, ShapeList):
            solid = Part(fused)
        else:
            solid = fused

        super().__init__(part = solid, rotation=rotation, mode=mode)