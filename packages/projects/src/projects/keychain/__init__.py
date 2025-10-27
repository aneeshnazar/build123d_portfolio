from build123d import Align, BasePartObject, BuildLine, BuildPart, BuildSketch, Circle, Locations, Mode, Polyline, Text, ThreePointArc, extrude, make_face


class TextKeychain(BasePartObject):
    def __init__(
        self,
        text : str,
        size : float,
        margin : float = 2,
        thickness : float = 1.2,
        hole_radius : float = 1.5,
        text_rotation : float = 0,
        rotation = (0,0,0),
        align = (Align.CENTER, Align.CENTER, Align.MIN),
        mode = Mode.ADD
    ):
        with BuildPart() as keychain:
            with BuildSketch() as text_tag:
                Text(text, size, rotation=text_rotation)
            extrude(amount=thickness)
            with BuildSketch() as keychain_profile:
                bb = text_tag.sketch.bounding_box()
                mx, mn, center = bb.max + (margin, margin), bb.min - (margin, margin), bb.center()
                outer_radius = (mn.Y - center.Y)
                with BuildLine():
                    Polyline(
                        (mn.X, mx.Y),
                        (mx.X, mx.Y),
                        (mx.X, mn.Y),
                        (mn.X, mn.Y)
                    )
                    ThreePointArc(
                        (mn.X, mx.Y),
                        (mn.X + outer_radius, center.Y),
                        (mn.X, mn.Y)
                    )
                make_face()
                with Locations((mn.X + outer_radius / 2, center.Y)):
                    Circle(hole_radius, mode=Mode.SUBTRACT)
            extrude(amount=-thickness)
        if keychain.part is None:
            raise Exception("Failed to create keychain")
        super().__init__(keychain.part, rotation, align, mode)
        self.name = f"TextKeychain-{text}"
        self.label = self.name