from enum import Enum

class Type(Enum):
    COMMENT = 'comment'
    REF = 'ref'
    NAME = 'name'
    EQUAL = 'equal'
    SPLIT = 'split'
    BCKL = 'bckl'
    BCKR = 'bckr'
    SPACE = 'space'

__pattern_type_map__ = [
    (Type.COMMENT, '#[\S \t\v\f]*'),
    (Type.REF, '[a-zA-Z_]\w*\.[a-zA-Z_]\w*'),
    (Type.NAME, '[a-zA-Z_]\w*'),
    (Type.EQUAL, '='),
    (Type.SPLIT, ','),
    (Type.BCKL, '\('),
    (Type.BCKR, '\)'),
    (Type.SPACE, '\s+'),
]
__ignored_type_name__ = {
    Type.COMMENT,
    Type.SPACE,
}
