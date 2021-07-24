import dataclasses
import typing

from sly import Lexer, Parser  # type: ignore


@dataclasses.dataclass
class Node:
    type: str
    body: typing.List["Node"]


class SampleLexer(Lexer):  # type: ignore
    """
    Grammar.
    statement: value
             | DLBRACKET variable DRBRACKET
    value    : STRING
             | NUMBER
    variable : STRING
    """

    ignore = "\t"

    tokens = {STRING, NUMBER, DLBRACKET, DRBRACKET}  # type: ignore # noqa: F821

    NUMBER = r"\d+"
    STRING = r"[a-zA-Z0-9_! ]+"

    DLBRACKET = r"{{"
    DRBRACKET = r"}}"

    @_(r"\n+")  # type: ignore # noqa: F821
    def newline(self, t) -> None:  # type: ignore
        self.lineno += t.value.count("\n")


class SampleParser(Parser):  # type: ignore
    tokens = SampleLexer.tokens

    @_("value")  # type: ignore # noqa: F821
    def statement(self, p):  # noqa: F811
        return p.value

    @_("DLBRACKET variable DRBRACKET")  # type: ignore # noqa: F821
    def statement(self, p):  # noqa: F811
        return p.variable

    @_("STRING")  # type: ignore # noqa: F821
    def value(self, p) -> Node:
        return Node(type="STRING", body=p.STRING)

    @_("NUMBER")  # type: ignore # noqa: F821
    def value(self, p) -> Node:  # noqa: F811
        return Node(type="NUMBER", body=int(p.NUMBER))

    @_("STRING")  # type: ignore # noqa: F821
    def variable(self, p) -> Node:  # type: ignore
        return Node(type="VARIABLE", body=p.STRING.strip())
