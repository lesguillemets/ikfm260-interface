import re

ID_PAT: re.Pattern = re.compile(r"TC([HA])\d\d\d")

CONDITION1_MAP: dict[int, str] = {0: "none", 1: "self", 2: "other"}
CONDITION2_MAP: dict[int, str] = {0: "self", 1: "other"}

EMOTION_MAP: dict[int, str] = {
    0: "sad",
    1: "anger",
    2: "happy",
    3: "excite",
    4: "relax",
    5: "dist",
    6: "fear",
    7: "surprise",
    8: "eight",
}

FILE_SUFFIXES: dict[str, str] = {"QR": "_qr_decoded.csv"}
