from os import write
import re

from services.logging import write_log


def split_into_blocks(text):

    lines_txt = text.split("\n")

    pattern_lang = re.compile(r"^```(\S+)")
    pattern_exact = re.compile(r"^```$")

    parts = []
    current_part = ""

    for line in lines_txt:
        if pattern_lang.match(line):
            parts.append(current_part)
            current_part = line + "\n"
            continue
        elif pattern_exact.match(line):
            current_part += line + "\n"
            parts.append(current_part)
            current_part = ""
            continue
        current_part += line + "\n"
    if current_part:
        parts.append(current_part)

    write_log(parts, "raw_blocks.log")
    return parts
