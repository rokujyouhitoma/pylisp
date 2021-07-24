import typing
from dataclasses import dataclass
from enum import Enum


@dataclass
class Err:
    reason: str


@dataclass
class Result:
    value: typing.Any
    err: Err


class Expression:
    def to_string(self) -> str:
        pass


@dataclass
class Bool(Expression):
    value: bool


@dataclass
class Symbol(Expression):
    value: str


@dataclass
class Number(Expression):
    value: int


@dataclass
class List(Expression):
    value: typing.List[Expression]


@dataclass
class Func(Expression):
    params: typing.List[Expression]
    body: Expression


@dataclass
class Lambda(Expression):
    params: typing.List[Expression]
    body: Expression


class Exp(Enum):
    Bool: Bool
    Symbol: Symbol
    Number: Number
    List: List
    Func: Func
    Lambda: Lambda


@dataclass
class Env:
    data: typing.Dict[str, Expression]
    outer: typing.Optional[Expression]


def default_env():
    pass


def Ok(value):
    return Result(value, None)


def tokenize(expr: str) -> typing.Sequence[str]:
    return [c for c in expr.replace("(", " ( ").replace(")", " ) ").split(" ") if c != ""]


def read_seq(tokens: typing.Sequence[str]) -> Result:
    res = []
    xs = tokens
    while xs:
        if len(tokens) == 0:
            return Result(None, Err("could not find closing `)`"))
        next_token, rest = xs[0], xs[1:]
        if next_token == ")":
            return Ok((List(res), rest))
        (exp, new_xs) = parse(xs).value
        res.append(exp)
        xs = new_xs


def parse_atom(token: str):
    if token == "true":
        return Bool(True)
    elif token == "false":
        return Bool(False)
    try:
        potential_float = int(token)
        return Number(potential_float)
    except ValueError:
        return Symbol(token)


def parse(tokens: typing.Sequence[str]) -> Result:
    if len(tokens) == 0:
        return Result(None, Err("could not get token"))
    token, rest = tokens[0], tokens[1:]
    if token == "(":
        return read_seq(rest)
    elif token == ")":
        return Result(None, Err("unexpected )"))
    else:
        return Result((parse_atom(token), rest), None)


def eval(exp: Exp, env: Env) -> Result:
    if isinstance(exp, Symbol):
        return exp
    elif isinstance(exp, Bool):
        return exp
    elif isinstance(exp, Number):
        return exp
    elif isinstance(exp, List):
        return exp


def parse_eval(expr: str, env: Env) -> Result:
    (parsed_exp, _) = parse(tokenize(expr)).value;
    evaled_exp = eval(parsed_exp, env);
    return Result(evaled_exp, None)


def read_expr() -> str:
    return input()


def main():
    env = default_env();
    # while True:
    #     print("lisp > ", end="")
    #     expr = read_expr()
    #     result = parse_eval(expr, env).value
    #     print(result)
    result = parse_eval("(1 2)", env).value
    print(result)


if __name__ == "__main__":
    main()
