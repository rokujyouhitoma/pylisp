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
    return Env({}, None)


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


def env_get(k: str, env: Env):
    exp = env.data.get(k.value)
    if exp:
        return exp
    else:
        outer_env = env.outer
        if outer_env:
            return env_get(k, outer_env)
        else:
            return None


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


def eval_if_args(arg_forms: typing.Sequence[Expression], env: Env):
    pass


def eval_def_args(arg_forms: typing.Sequence[Expression], env: Env):
    if len(arg_forms) == 0:
        return Result(None, Err("expected first form"))
    first_form = arg_forms[0]
    if isinstance(first_form, Symbol):
        first_str = Ok(first_form)
    else:
        return Err("expected first form to be a symbol")
    if len(arg_forms) > 1:
        second_form = arg_forms[1]
    else:
        return Err("expected second form")
    if len(arg_forms) > 3:
        return Err("def can only have two forms")
    second_eval = eval(second_form, env)
    env.data[first_str.value.value] = second_eval;
    return Ok(first_form)


def eval_lamba_args(arg_forms: typing.Sequence[Expression], env: Env):
    pass


def eval_built_in_form(exp: Expression, arg_forms: typing.Sequence[Expression], env: Env) -> typing.Optional[Result]:
    if isinstance(exp, Symbol):
        if exp.value == "if":
            return eval_if_args(arg_forms, env)
        elif exp.value == "def":
            return eval_def_args(arg_forms, env)
        elif exp.value == "fn":
            return eval_lambda_args(arg_forms, env)
        else:
            return None
    else:
        return None


def eval(exp: Expression, env: Env) -> Result:
    if isinstance(exp, Symbol):
        return env_get(exp, env)
    elif isinstance(exp, Bool):
        return exp
    elif isinstance(exp, Number):
        return exp
    elif isinstance(exp, List):
        if len(exp.value) == 0:
            return Result(None, Err("expected a non-empty list"))
        first_form = exp.value[0]
        arg_forms = exp.value[1:]
        res = eval_built_in_form(first_form, arg_forms, env)
        if res:
            return res
        else:
            first_eval = eval(first_form, env)
            if isinstance(first_eval, Func):
                def f(v):
                    return v
                return f(eval_forms(arg_forms, env))
            else:
                return Err("first form must be a function")


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
    #result = parse_eval("(1 2)", env).value
    result = parse_eval("(def f 1)", env).value
    result = parse_eval("f", env).value
    print(result)
    print(env)


if __name__ == "__main__":
    main()
