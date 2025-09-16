import re


def clean_text(text):

    pattern = re.compile(r"^\s*---\s*$", re.MULTILINE)
    txt = pattern.sub("", text)

    pattern = re.compile(r"(?m)^(\s+)\*(\s+)", re.MULTILINE)
    txt = pattern.sub(r"\1" + "`" + "\U00002022" + "`" + r"\2", txt)

    def replace_asterisk(match):
        leading_ws = match.group(1) or ""
        after_ws = match.group(2) or ""
        return f"{leading_ws}`\U00002022`{after_ws}"

    txt = re.sub(r"(?m)^(\s*)\*(\s+)", replace_asterisk, txt)

    txt = re.sub(r"###", "\U000025ab\U0000fe0f", txt)

    pattern = r"```(?!\w+)(.*?)\n```"
    repl = r"```info\1\n```"
    txt = re.sub(pattern, repl, txt, flags=re.DOTALL)

    return txt
