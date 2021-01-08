from xinaprocessor.constants import *
import re
import emoji
import random


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


def remove_single_char_space_before(text: str):
    return re.sub(r"(?:^| )(\w)(?:$| )", r"\1 ", text).strip()


def remove_single_char_space_after(text: str):
    return re.sub(r"(?:^| )(\w)(?:$| )", r" \1", text).strip()


def keep_only(text: str, list_chars):
    chars = "".join(list_chars)
    spaced_text = re.sub(f"[^{chars}]", " ", text)
    return remove_extra_spaces(spaced_text).strip()


def replace_repeated_chars(text: str, repeated=1, keep_char=1):
    assert repeated > 0
    assert keep_char >= 0
    pattern = r"(.)\1{}".format(f"{{{repeated-1},}}")
    return re.sub(pattern, r"\1" * keep_char, text)


def train_test_split(x: list, test_size: float, random_seed=None):
    assert test_size > 0.0 and test_size < 1.0, "test size sould be between 0 and 1"
    assert len(x) > 1, "the length of the given list should be greater than 1"
    if random_seed:
        random.random(random_seed).shuffle(x)
    else:
        random.shuffle(x)
    test = x[: int(len(x) * test_size)]
    train = x[int(len(x) * test_size):]
    return train, test


def export_text(file_path, data: list, sep="\n", encoding="utf-8"):
    with open(file_path, "a", encoding=encoding) as f:
        f.write(sep.join(data))
