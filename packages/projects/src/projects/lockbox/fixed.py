from build123d import Align, Axis, BasePartObject, Box, BuildPart, BuildSketch, GeomType, Kind, Locations, Mode, Plane, Rectangle, RectangleRounded, RotationLike, Select, chamfer, extrude, fillet, loft, offset


class Dividers(BasePartObject):
    def __init__(
        self,
        length,
        width,
        height,
        thickness,
        body_roundness,
        divider_mask: list[bool] = [False] * 5 + [True] + [False] * 6,
        rotation: RotationLike = (0,0,0),
        align : tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.MIN),
        mode : Mode = Mode.ADD
    ):
        num_compartments = len(divider_mask)
        divider_positions = [(x * length / num_compartments - length / 2, 0) for x in range(1, num_compartments) if divider_mask[x - 1]]
        with BuildPart() as dividers:
            with BuildSketch():
                RectangleRounded(length - thickness, width - thickness, body_roundness)
                RectangleRounded(length - 2 * thickness, width - 2 * thickness, body_roundness, mode=Mode.SUBTRACT)
                with Locations(*divider_positions):
                    Rectangle(thickness, width - thickness * 2)
            extrude(amount=height - thickness)
            fillet(dividers.edges(Select.LAST).filter_by(Axis.Z), thickness)
        super().__init__(dividers.part, rotation, align, mode) # type: ignore

class Body(BasePartObject):
    def __init__(
        self,
        length,
        width,
        height,
        thickness,
        body_roundness,
        divider_mask : list[bool] = [True] * 12,
        rotation : RotationLike = (0,0,0),
        align : tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.MIN),
        mode = Mode.ADD
    ):
        num_compartments = len(divider_mask)
        divider_positions = [(x * length / num_compartments - length / 2, 0) for x in range(1, num_compartments) if divider_mask[x - 1]]
        with BuildPart() as body:
            Box(length, width, height, align=(Align.CENTER, Align.CENTER, Align.MIN))
            offset(openings = body.faces().sort_by(Axis.Z).last, amount = -thickness, kind=Kind.INTERSECTION)
            fillet(body.edges().filter_by(Axis.Z), body_roundness)
            chamfer(body.faces().filter_by(Axis.Z).sort_by(Axis.Z).first.edges(), thickness)
            if len(divider_positions):
                with BuildPart(Plane.XY.offset(thickness)):
                    Dividers(length, width, height, thickness, body_roundness, divider_mask)
        super().__init__(body.part, rotation, align, mode) # type: ignore
        self.label = "Body"
        self.name = self.label

class Lid(BasePartObject):
    def __init__(
        self,
        length,
        width,
        height,
        lid_height,
        thickness,
        body_roundness,
        margin,
        divider_mask : list[bool] = [True] * 12,
        rotation : RotationLike = (0,0,0),
        align : tuple[Align, Align, Align] = (Align.CENTER, Align.CENTER, Align.MAX),
        mode : Mode = Mode.ADD
    ):
        with BuildPart() as lid:
            plane = lid.workplanes[0]
    
            with BuildSketch(plane.offset(lid_height + thickness)):
                RectangleRounded(length, width, body_roundness)
            with BuildSketch(plane):
                RectangleRounded(length, width, body_roundness)
            loft(ruled=True)
            chamfer(lid.faces().sort_by(Axis.Z).last.edges(), thickness)
            with BuildSketch(plane):
                RectangleRounded(length - 2 * thickness - margin, width - 2 * thickness - margin, body_roundness)
            extrude(amount = -lid_height)
            with BuildSketch(plane.offset(-lid_height)):
                RectangleRounded(length - 4 * thickness, width - 4 * thickness, body_roundness)
            extrude(amount = 2 * lid_height, mode=Mode.SUBTRACT)

            Dividers(length, width, height, thickness, body_roundness, divider_mask, align=(Align.CENTER, Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)
           
        super().__init__(lid.part, rotation, align, mode) # type: ignore
        self.label = "Lid"
        self.name = self.label