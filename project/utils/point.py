import attr


@attr.s(slots=True, auto_attribs=True)
class Point:
    x: float = attr.ib()
    y: float = attr.ib()
