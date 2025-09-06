from enum import Enum

POSITIONS = [
        "Ast - ALS (J)",
        "Ast - ALS (S)",
        "Ast - BKS (J)",
        "Ast - BKS (S)",
        "Ast - KMG (J)",
        "Ast - KMG (S)",
        "Ast - SMG (J)",
        "Ast - SMG (S)",
        "AstDev",
        "DBA Staff",
        "Head - KMG",
        "NA Officer - ALS",
        "NA Officer - KMG",
        "NA Staff - ALS",
        "NA Staff - KMG",
        "OP Officer",
        "Prt - ALS (J)",
        "Prt - ALS (S)",
        "Prt - BKS (J)",
        "Prt - BKS (S)",
        "ResMan Officer - ALS",
        "RnD Staff",
        "Subco - ALS",
        "Subco - KMG",
        "SubDev"
    ]

class Position(Enum):
    AST = "ast"
    ASTDEV = "astdev"
    ALL_NA = "all-na"
    KMG_NA = "kmg-na"
    ALS_NA = "als-na"
    RND = "rnd"
    DBA = "dba"
    SUBDEV = "subdev"
    OP = "op"
    PART = "part"
    SUBCO = "subco"
    RESMAN = "resman"
    HEAD = "head"

POSITION_MAPS = {
    Position.AST: [
        "Ast - ALS (J)",
        "Ast - ALS (S)",
        "Ast - BKS (J)",
        "Ast - BKS (S)",
        "Ast - KMG (J)",
        "Ast - KMG (S)",
        "Ast - SMG (J)",
        "Ast - SMG (S)"
    ],
    Position.ASTDEV: ["AstDev"],
    Position.ALL_NA: [
        "NA Officer - ALS",
        "NA Officer - KMG",
        "NA Staff - ALS",
        "NA Staff - KMG"
    ],
    Position.KMG_NA: [
        "NA Officer - KMG",
        "NA Staff - KMG"
    ],
    Position.ALS_NA: [
        "NA Officer - ALS",
        "NA Staff - ALS"
    ],
    Position.RND: [
        "RnD Staff",
        "RnD Officer"
    ],
    Position.DBA: [
        "DBA Staff",
        "DBA Officer"
    ],
    Position.SUBDEV: ["SubDev"],
    Position.OP: ["OP Officer"],
    Position.PART: [
        "Prt - ALS (J)",
        "Prt - ALS (S)",
        "Prt - BKS (J)",
        "Prt - BKS (S)"
    ],
    Position.SUBCO: [
        "Subco - ALS",
        "Subco - KMG"
    ],
    Position.RESMAN: ["ResMan Officer - ALS"],
    Position.HEAD: ["Head - KMG"]
}

DAY_MAPS = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday"
}

SHIFT_MAPS = {
    "M": "Night",
    "P": "Morning",
    "N": "Normal"
}

SHIFT_HOURS = {
    "P": {"start": 7, "end": 15, "label": "07:00 - 15:00"},
    "M": {"start": 11, "end": 19, "label": "11:00 - 19:00"},
    "N": {"start": 9, "end": 19, "label": "09:00 - 19:00"},
}

SCHEDULE_START_HOUR = 7