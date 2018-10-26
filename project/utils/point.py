import attr


@attr.s(slots=True, auto_attribs=True)
class Point:
    x: float = attr.ib()
    y: float = attr.ib()

    def __iter__(self):
        return (getattr(self, f.name) for f in attr.fields(self.__class__))


@attr.s(slots=True, auto_attribs=True)
class Dimensions:
    width: int = attr.ib()
    height: int = attr.ib()

    def __iter__(self):
        return (getattr(self, f.name) for f in attr.fields(self.__class__))
