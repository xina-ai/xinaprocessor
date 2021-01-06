from constants import *
import re
import emoji


def replace_list(list_chars, text, replace_with=""):
    chars = "".join(list_chars)
    return re.sub(f"[{chars}]", replace_with, text)


def remove_tashkeel(text: str):
    return replace_list(HARAKAT, text, "")


def remove_tatweel(text: str):
    return replace_list([TATWEEL], text, "")


def remove_tashkeel_main(text: str):
    return replace_list(HARAKAT_MAIN, text, "")


def remove_tashkeel_others(text: str):
    return replace_list(HARAKAT_OTHERS, text, "")


def remove_punctuation_arabic(text: str):
    return replace_list(list(ARABIC_PUNCTUATION), text, "")


def remove_punctuation_english(text: str):
    return replace_list(list(ENGLISH_PUNCTUATION), text, "")


def remove_punctuation_others(text: str):
    return replace_list(OTHER_PUNCTUATION, text, "")


def remove_punctuation(text: str):
    return replace_list(PUNCTUATION, text, "")


def remove_extra_spaces(text: str, keep_spaces=1):
    return re.sub(" +", " " * keep_spaces, "".join(text))


def remove_emoji(text: str):
    return emoji.get_emoji_regexp().sub("", text)


def remove_numbers(text: str):
    return replace_list(list(ARABIC_NUM + ENGLISH_NUM), text, "")


def remove_hashtags(text: str):
    return re.sub(r"#.*?(?=\s)", "", text)


def remove_links(text: str):
    return re.sub("http[s]?://\S+", "", text)


def remove_english(text: str):
    replace_list(list(ENGLISH_CHARS), text, "")


def remove_mentions(text: str):
    return re.sub(r"@.*?(?=\s)", "", text)


def remove_single_char(text: str):
    return re.sub(r"(?:^| )\w(?:$| )", " ", text).strip()


def keep_only(text: str, list_chars):
    chars = "".join(list_chars)
    spaced_text = re.sub(f"[^{chars}]", " ", text)
    return remove_extra_spaces(spaced_text).strip()


def keep_arabic_only(text: str):
    clean = remove_tashkeel(text)
    clean = remove_tatweel(clean)
    clean = keep_only(clean, list(ARABIC_CHARS))
    return clean


def keep_english_only(text: str):
    clean = remove_tashkeel(text)
    clean = remove_tatweel(clean)
    clean = keep_only(clean, list(ENGLISH_CHARS))
    return clean


def keep_arabic_and_numbers_only(text: str):
    clean = remove_tashkeel(text)
    clean = remove_tatweel(clean)
    clean = keep_only(clean, list(ARABIC_CHARS + ARABIC_NUM + ENGLISH_NUM))
    return clean


def keep_arabic_with_tashkeel_only(text: str):
    clean = remove_tatweel(text)
    clean = keep_only(clean, list(ARABIC_CHARS) + HARAKAT_MAIN)
    return clean


def keep_arabic_and_english_only(text: str):
    clean = remove_tashkeel(text)
    clean = remove_tatweel(clean)
    clean = keep_only(clean, list(ARABIC_CHARS + ENGLISH_CHARS))
    return clean


def replace_repeated_chars(text: str, repeated=1, keep_char=1):
    assert repeated > 0
    assert keep_char >= 0
    pattern = r"(.)\1{}".format(f"{{{repeated},}}")
    return re.sub(pattern, r"\1" * keep_char, text)
