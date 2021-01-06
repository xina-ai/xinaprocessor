from constants import *
import re
import emoji


def replace_list(list_chars, text, replace_with=""):
    chars = "".join(list_chars)
    return re.sub(f"[{chars}]", replace_with, text)


def remove_extra_spaces(text: str, keep_spaces=1):
    return re.sub(" +", " " * keep_spaces, "".join(text))


def remove_emoji(text: str):
    return emoji.get_emoji_regexp().sub("", text)


def remove_hashtags(text: str):
    return re.sub(r"#.*?(?=\s)", "", text)


def remove_links(text: str):
    return re.sub("http[s]?://\S+", "", text)


def remove_mentions(text: str):
    return re.sub(r"@.*?(?=\s)", "", text)


def remove_single_char(text: str):
    return re.sub(r"(?:^| )\w(?:$| )", " ", text).strip()


def keep_only(text: str, list_chars):
    chars = "".join(list_chars)
    spaced_text = re.sub(f"[^{chars}]", " ", text)
    return remove_extra_spaces(spaced_text).strip()


def replace_repeated_chars(text: str, repeated=1, keep_char=1):
    assert repeated > 0
    assert keep_char >= 0
    pattern = r"(.)\1{}".format(f"{{{repeated},}}")
    return re.sub(pattern, r"\1" * keep_char, text)
