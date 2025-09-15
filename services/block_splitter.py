import re
from math import ceil

from services.logging import write_log

MAX_MESSAGE_LENGTH = 3900


def size_parts(block):
    max_length = MAX_MESSAGE_LENGTH
    size = 0

    if len(block) <= (max_length * 2):
        size = len(block) // 2
    else:
        k = ceil(len(block) / max_length)
        size = len(block) // k
    return size


def split_txt(txt_split, block):
    block_split = block.split("\n")
    current_part = ""
    size = size_parts(block)
    for line in block_split:
        if len(current_part) + len(line) + 1 <= size:
            current_part += line + "\n"
        else:
            txt_split.append(current_part)
            current_part = line + "\n"
    if current_part:
        txt_split.append(current_part)

    return txt_split


def split_code(txt_split, block, lang_pre):
    block_split = block.split("\n")
    current_part = ""
    size = size_parts(block)
    for line in block_split:
        if len(current_part) + len(line) + 1 <= size:
            current_part += line + "\n"
        else:
            txt_split.append(current_part + "\n```")
            current_part = lang_pre + line + "\n"
    if current_part:
        txt_split.append(current_part)

    return txt_split


def split_by_length(blocks):
    pattern_lang = re.compile(r"^```(\S+)")
    txt_split = []

    for block in blocks:
        if len(block) <= MAX_MESSAGE_LENGTH:
            txt_split.append(block)
        else:
            match_obj = pattern_lang.match(block)
            if match_obj:
                lang_pre = match_obj.group(0)
                txt_split = split_code(txt_split, block, lang_pre)
            else:
                txt_split = split_txt(txt_split, block)
    write_log(txt_split, "blocks.log")
    return txt_split
