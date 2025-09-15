import re


def clean_text(text):

    pattern = re.compile(r"^\s*---\s*$", re.MULTILINE)

    txt = pattern.sub("", text)

    pattern = re.compile(r"(?m)^(\s+)\*(\s+)", re.MULTILINE)

    txt = pattern.sub(r"\1" + "`" + "\U00002022" + "`" + r"\2", txt)

    pattern = re.compile(r"^\*\s+", re.MULTILINE)

    txt = pattern.sub("\U00002022" + " ", txt)
    txt = re.sub(r"###", "\U000025aa", txt)

    pattern = r"```(?!\w+)(.*?)\n```"
    repl = r"```info\1\n```"
    txt = re.sub(pattern, repl, txt, flags=re.DOTALL)

    return txt
