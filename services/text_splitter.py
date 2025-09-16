import re

from services.logging import write_log


def split_into_blocks(text):

    lines_txt = text.split("\n")

    pattern_lang = re.compile(r"^```")

    parts = []
    current_part = ""

    flag = 0

    for line in lines_txt:
        if pattern_lang.match(line) and flag == 0:
            flag = 1
            if current_part:
                parts.append(current_part)
            current_part = line + "\n"
            continue
        elif pattern_lang.match(line) and flag == 1:
            flag = 0
            current_part += line + "\n"
            parts.append(current_part)
            current_part = ""
            continue
        current_part += line + "\n"
    if current_part:
        parts.append(current_part)

    write_log(parts, "raw_blocks.log")

    return parts
