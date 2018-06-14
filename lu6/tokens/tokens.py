from enum import Enum


class TokenInfo(object):
    def __init__(self, name, image):
        self.name = name
        self.image = image

    def has_image(self, string):
        return string is not None and self.image is not None and \
               len(self.image) == len(string) and \
               self.image == string

    def __eq__(self, token):
        return self.name == token.name

    def __repr__(self):
        return self.image


class Token(object):
    def __init__(self, type, image, line):
        self._type = type
        self._image = image
        self._line = line

    @property
    def image(self):
        return self._image

    @property
    def type(self):
        return self._type

    def has_type(self, tType):
        return self._type == tType

    def has_type_one_of(self, tTypes):
        for tType in tTypes:
            if self.has_type(tType):
                return True
        return False

    def __repr__(self):
        return "Token {type}: {image}".format(type=self._type.name, image=self._image)

    def __str__(self):
        return self.__repr__()

    def __iadd__(self, other):
        self._image += other.image
        return self

    def __add__(self, other):
        self._image += other.image
        return self


class TokenEnum(Enum):
    @classmethod
    def has(cls, item):
        for tName in cls.__members__:
            token = cls.__members__[tName].value
            if token.has_image(item):
                return True

        return False


# Special tokens
class SpecialTokens(TokenEnum):
    # EOF token
    EOFToken = TokenInfo("EOF", None)

    # Single-character tokens
    DotToken = TokenInfo("DOT", ".")
    ColonToken = TokenInfo("COLON", ":")
    SemiColonToken = TokenInfo("SEMICOLON", ";")
    CommaToken = TokenInfo("COMMA", ",")
    StarToken = TokenInfo("STAR", "*")
    SlashToken = TokenInfo("SLASH", "/")
    RemToken = TokenInfo("REM", "%")
    PlusToken = TokenInfo("PLUS", "+")
    MinusToken = TokenInfo("MINUS","-")
    AmpersandToken = TokenInfo("AMPERSAND", "&")
    AssignToken = TokenInfo("ASSIGN", "=")
    MultiplyAssignToken = TokenInfo("MULTIPLY-ASSIGN", "*=")
    PlusAssignToken = TokenInfo("PLUS-ASSIGN", "+=")
    MinusAssignToken = TokenInfo("MINUS-ASSIGN", "-=")
    DivisionAssignToken = TokenInfo("DIVISION-ASSIGN", "/=")
    RemainderAssignToken = TokenInfo("REM-ASSIGN", "%=")

    LParenToken = TokenInfo("LPAREN", "(")
    RParenToken = TokenInfo("RPAREN", ")")
    LCurlyToken = TokenInfo("LCURLY", "{")
    RCurlyToken = TokenInfo("RCURLY", "}")

    StrictGreaterToken = TokenInfo("STRICT_GREATER", ">")
    StrictLessToken = TokenInfo("STRICT_LESS", "<")

    # Double-character tokens
    DoubleColonToken = TokenInfo("DOUBLE_COLON", "::")
    ArrowToken = TokenInfo("ARROW", "->")
    EqualsToken = TokenInfo("EQUALS", "==")
    NotEqualToken = TokenInfo("NOT_EQUALS", "!=")
    OrToken = TokenInfo("OR", "||")
    AndToken = TokenInfo("AND", "&&")
    GreaterToken = TokenInfo("GREATER", ">=")
    LessToken = TokenInfo("LESS", "<=")

    # Triple-character tokens
    # TripleQuotesTokens = TokenInfo("TRIPLE_QUOTES", "\"\"\"")


# Reserved words
class ReservedWordsTokens(TokenEnum):
    # Template engine reserved tokens
    AttributeToken = TokenInfo("RES_ATTRIBUTE", "@attribute")
    ClassToken = TokenInfo("RES_CLASS", "@class")
    ConstructorToken = TokenInfo("RES_CONSTRUCTOR", "@constructor")
    CategoryToken = TokenInfo("RES_CATEGORY", "@category")
    ExtendsToken = TokenInfo("RES_EXTENDS", "@extends")
    FunctionToken = TokenInfo("RES_FUNCTION", "@function")
    IncludeToken = TokenInfo("RES_INCLUDE", "@include")
    MethodToken = TokenInfo("RES_METHOD", "@method")
    PrintToken = TokenInfo("RES_PRINT", "@print")
    PrintlnToken = TokenInfo("RES_PRINTLN", "@println")
    InstructionToken = TokenInfo("RES_INSTRUCTION", "@instruction")
    IfToken = TokenInfo("RES_IF", "@if")
    ElseToken = TokenInfo("RES_ELSE", "@else")
    WhileToken = TokenInfo("RES_WHILE", "@while")

    # C++ ISO useful reserved tokens
    PrivateToken = TokenInfo("RES_PRIVATE_MODIFIER", "private")
    PublicToken = TokenInfo("RES_PUBLIC_MODIFIER", "public")
    ProtectedToken = TokenInfo("RES_PROTECTED_MODIFIER", "protected")
    StaticToken = TokenInfo("RES_STATIC_MODIFIER", "static")
    ConstToken = TokenInfo("RES_CONST_MODIFIER", "const")

    # C++ Special values
    TrueToken = TokenInfo("RES_TRUE", "true")
    FalseToken = TokenInfo("RES_FALSE", "false")

    # Empty token, used for identifying scanner errors
    NullToken = TokenInfo("RES_NULL", "")


class IdentifierTokens(TokenEnum):
    CodegenIdentifier = TokenInfo("CODEGEN_IDENTIFIER", "<IDENTIFIER>")
    VariableIdentifier = TokenInfo("VARIABLE_IDENTIFIER", "<$IDENTIFIER>")


class LiteralTokens(TokenEnum):
    EnhancedStringLiteral = TokenInfo("ENHANCED_STRING_LITERAL", "<ENHANCED_STRING_LITERAL>")
    StringLiteral = TokenInfo("STRING_LITERAL", "<STRING_LITERAL>")
    IntLiteral = TokenInfo("INT_LITERAL", "<INT_LITERAL>")


class WhitespaceTokens(TokenEnum):
    SpaceToken = TokenInfo("SPACE", " ")
    CRToken = TokenInfo("CR", "\r")
    LFToken = TokenInfo("LF", "\n")
    TabToken = TokenInfo("TAB", "\t")


StatementTokens = [
    ReservedWordsTokens.WhileToken,
    ReservedWordsTokens.IfToken
]

CodegenValidTokenList = [
    SpecialTokens.SemiColonToken,
    SpecialTokens.RParenToken,
    SpecialTokens.LParenToken,
    SpecialTokens.RCurlyToken,
    SpecialTokens.LCurlyToken,
    SpecialTokens.DotToken,
    SpecialTokens.DoubleColonToken,
    SpecialTokens.ColonToken,
    SpecialTokens.CommaToken,
    SpecialTokens.ArrowToken,
    SpecialTokens.StarToken,
    SpecialTokens.AmpersandToken,
    SpecialTokens.AssignToken,
    SpecialTokens.EqualsToken,

    LiteralTokens.StringLiteral,
    LiteralTokens.IntLiteral,

    WhitespaceTokens.SpaceToken,
    #WhitespaceTokens.LFToken,
    WhitespaceTokens.CRToken,
    WhitespaceTokens.TabToken,

    IdentifierTokens.CodegenIdentifier,
    IdentifierTokens.VariableIdentifier
]


def get_truth_token(line, image):
    if image == "true":
        return Token(ReservedWordsTokens.TrueToken.value, True, line)
    elif image == "false":
        return Token(ReservedWordsTokens.FalseToken.value, False, line)


def get_token(collection, image, line):
    for token in collection:
        if token.value.has_image(image):
            return Token(token.value, image, line)

    if image is None:
        return Token(SpecialTokens.EOFToken.value, image, line)

    return Token(ReservedWordsTokens.NullToken.value, "", line)


def get_special_token(line, image):
    return get_token(SpecialTokens, image, line)


def get_reserved_word_token(line, image):
    return get_token(ReservedWordsTokens, image, line)


def get_identifier_token(line, image):
    if image.startswith("$"):
        return Token(IdentifierTokens.VariableIdentifier.value, image, line)
    return Token(IdentifierTokens.CodegenIdentifier.value, image, line)


def get_eof_token(line):
    return Token(SpecialTokens.EOFToken.value, "", line)


def get_literal(line, image):
    if len(image) > 0 and image.isdigit():
        return Token(LiteralTokens.IntLiteral.value, image, line)
    return Token(LiteralTokens.StringLiteral.value, image, line)


def get_whitespace(line, image):
    if image == " ":
        return Token(WhitespaceTokens.SpaceToken.value, image, line)
    elif image == "\n":
        return Token(WhitespaceTokens.LFToken.value, image, line)
    elif image == "\r":
        return Token(WhitespaceTokens.CRToken.value, image, line)
    elif image == "\t":
        return Token(WhitespaceTokens.TabToken.value, image, line)
    return Token(ReservedWordsTokens.NullToken.value, image, line)
