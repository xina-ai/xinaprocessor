from typing import List
from xinaprocessor.constants import *
import re
import emoji
import random
from collections import Counter


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
    return re.sub("http[s]?://\S+|[wW]{3,}[\S/\?=\.&]+", "", text)


def remove_mentions(text: str):
    return re.sub(r" @[\w_]+ | @[\w_]+|^@[\w_]+ ", " ", text)

def remove_emails(text: str):
    return re.sub(r"\S+@\S+", "", text)

def contains_single_char(text: str):
    return True if re.search(r"(?:^| )\w(?:$| )", text) else False


def contains_persian(text: str):
    return True if re.search(r"[\uFB50-\uFB9F{}]".format(''.join(PERSIAN_UNIQUE_CHARS)), text) else False

def contains_english(text: str):
    return True if re.search(r"[A-Za-z]", text) else False

def remove_single_char_space_before(text: str):
    return re.sub(r"(?:^| )(\w)(?:$| )", r"\1 ", text).strip()


def remove_single_char_space_after(text: str):
    return re.sub(r"(?:^| )(\w)(?:$| )", r" \1", text).strip()


def multi_replace(keys: List[str], values: List[str], text: str):
    """Replace each item in keys with the corresponding item in values in the input text

    Args:
        keys (List[str]): a list of strings to be replaces
        values (List[str]): list of strings with same length of keys to with values to be replaced with
        text (str): input text to apply replacements on

    Returns:
        str: text with strings in keys replaced with corresponding strings in values
    """
    exp = "|".join(map(re.escape, keys))
    def func(match): return values[keys.index(match.group(0))]
    return re.sub(exp, func, text)


def keep_only(text: str, list_chars):
    chars = "".join(list_chars)
    spaced_text = re.sub(f"[^{chars}]", " ", text)
    return remove_extra_spaces(spaced_text).strip()


def replace_repeated_chars(text: str, repeated=1, keep_char=1):
    assert repeated > 0
    assert keep_char >= 0
    pattern = r"(.)\1{}".format(f"{{{repeated-1},}}")
    return re.sub(pattern, r"\1" * keep_char, text)

def replace_except(text: str, keep_symbols: str, replace_by: str) -> str:
    return re.sub(f"[^{keep_symbols}]", replace_by, text)

def contains_repeated_chars(text: str, repeated=1):
    pattern = r"(.)\1{}".format(f"{{{repeated-1},}}")
    return True if re.search(pattern, text) else False


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


def transliteration_to_arabic(text: str):
    for ar_char, buc_symbole in BUCKWALTER_TRANSLITERATION.items():
        text = text.replace(buc_symbole, ar_char)
    return text


def arabic_to_transliteration(text: str):
    for ar_char, buc_symbole in BUCKWALTER_TRANSLITERATION.items():
        text = text.replace(ar_char, buc_symbole)
    return text


def str_count_frequency(text: str, sep= " ", word_level= True):
    if word_level:
        return Counter(text.split(sep))
    return Counter(text)


def doc_count_frequency(texts: list, split_by= " ", word_level= True):
    text = split_by.join(texts)
    return str_count_frequency(text, sep= split_by, word_level= word_level)

def swap_tanween_alef(text: str):
    return text.replace(TANWEEN + NORMAL_ALEF, NORMAL_ALEF + TANWEEN)