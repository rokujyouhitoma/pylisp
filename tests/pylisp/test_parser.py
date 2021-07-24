import pytest
from sly.lex import Token as Token_

from pylisp.parser import SampleLexer, SampleParser, Node


def Token(type, value, lineno, index):
    token = Token_()
    token.type = type
    token.value = value
    token.lineno = lineno
    token.index = index
    return token


class TestLexer:
    @pytest.mark.parametrize(
        "test_input,expected", [
            ("{{a}}", [
                Token(type='DLBRACKET', value='{{', lineno=1, index=0),
                Token(type='STRING', value='a', lineno=1, index=2),
                Token(type='DRBRACKET', value='}}', lineno=1, index=3)
            ]),
            ("a\n", [
                Token(type='STRING', value='a', lineno=1, index=0),
            ]),
            ("a\nb", [
                Token(type='STRING', value='a', lineno=1, index=0),
                Token(type='STRING', value='b', lineno=2, index=2),
            ]),
            ("Hello {{ name }}!", [
                Token(type='STRING', value='Hello ', lineno=1, index=0),
                Token(type='DLBRACKET', value='{{', lineno=1, index=6),
                Token(type='STRING', value=' name ', lineno=1, index=8),
                Token(type='DRBRACKET', value='}}', lineno=1, index=14),
                Token(type='STRING', value='!', lineno=1, index=16)
            ]),
        ]
    )
    def test_tokenize(self, test_input, expected):
        lexer = SampleLexer()
        tokens = [token for token in lexer.tokenize(test_input)]
        print(tokens)
        for v1, v2 in zip(tokens, expected):
            assert (v1.type, v1.value) == (v2.type, v2.value)
            assert (v1.lineno, v1.index) == (v2.lineno, v2.index)
        assert len(tokens) == len(expected)


class TestParser:
    @pytest.mark.parametrize(
        "test_input,expected", [
            ("a", Node(type='STRING', body='a')),
            ("1", Node(type='NUMBER', body=1)),
            ("xyz", Node(type='STRING', body='xyz')),
            ("{{a}}", Node(type='VARIABLE', body='a')),
            ("{{xyz}}", Node(type='VARIABLE', body='xyz')),
        ]
    )
    def test_parse(self, test_input, expected):
        lexer = SampleLexer()
        parser = SampleParser()
        node = parser.parse(lexer.tokenize(test_input))
        assert node == expected


def test_parser():
    query = "{{a}}"
    lexer = SampleLexer()
    parser = SampleParser()
    ast = parser.parse(lexer.tokenize(query))
    assert ast
