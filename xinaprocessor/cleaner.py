import random
from typing import Text
from xinaprocessor.base import BaseCleaner
from xinaprocessor.constants import ARABIC_CHARS
from xinaprocessor.helper import *


class TextCleaner(BaseCleaner):
    def __init__(self, text: str, sep="\n") -> None:
        super().__init__()

        self.raw_text = text
        self.lines = []
        self.raw_lines = []
        self.sep = sep
        self._split_text(sep)

    # region remove functions
    def remove_english_text(self):
        return self._remove(ENGLISH_CHARS)

    def remove_arabic_text(self):
        return self._remove(ARABIC_CHARS)

    def remove_numbers(self):
        return self._remove(ENGLISH_NUM + ARABIC_NUM)

    def remove_arabic_numbers(self):
        return self._remove(ARABIC_NUM)

    def remove_english_numbers(self):
        return self._remove(ENGLISH_NUM)

    def remove_arabic_puntuation(self):
        return self._remove(ARABIC_PUNCTUATION)

    def remove_english_puntuation(self):
        return self._remove(ENGLISH_PUNCTUATION)

    def remove_other_puntuation(self):
        return self._remove(OTHER_PUNCTUATION)

    def remove_puntuation(self):
        return self._remove(PUNCTUATION)

    def remove_tashkeel_main(self):
        return self._remove(HARAKAT_MAIN)

    def remove_tashkeel_other(self):
        return self._remove(HARAKAT_OTHERS)

    def remove_tashkeel(self):
        return self._remove(HARAKAT)

    def remove_tatweel(self):
        return self._remove(TATWEEL)

    def remove_extra_spaces(self, keep_space=1):
        return self._map_lines(lambda line: remove_extra_spaces(line, keep_space))

    def remove_emojis(self):
        return self._map_lines(remove_emoji)

    def remove_hashtags(self):
        return self._map_lines(remove_hashtags)

    def remove_quranic_annotations(self):
        return self._remove(QURANIC_ANNOTATION)

    def remove_honorific_signs(self):
        return self._remove(HONORIFIC_SIGN)

    def remove_links(self):
        return self._map_lines(remove_links)

    def remove_mentions(self):
        return self._map_lines(remove_mentions)

    def remove_duplicates(self):
        self.lines = list(dict.fromkeys(self.lines))
        return self

    def remove_single_char(self):
        """Remove words of a single character

        Returns:
            TextCleaner: self

        Examples:
            inp = 'hello h r you?'
            print(remove_single_char(inp))
                'hello you?'
        """
        return self._map_lines(remove_single_char)

    # endregion
    # region filter functions
    def remove_empty_lines(self):
        return self.filter_lines_below_len(1)

    def remove_lines_below_len(self, length: int):
        return self._filter(self.lines, lambda line: len(line) < length)

    def remove_lines_above_len(self, length: int):
        return self._filter(self.lines, lambda line: len(line) > length)

    def remove_lines_with_len(self, length: int):
        return self._filter(self.lines, lambda line: len(line) == length)

    def remove_lines_contain(self, char: int):
        return self._filter(self.lines, lambda line: char not in line)

    def filter_lines_contain(self, char: int):
        return self._filter(self.lines, lambda line: char in line)

    # endregion
    # region internal functions

    def __getitem__(self, item):
        assert item > -1 and item < len(self), "Index must be in range."
        return self.lines[item]

    def __len__(self):
        return len(self.lines)

    def _clean(self, keep):
        """Clean the text by keeping only "keep" string.
        If sep is not None, text will be splitted into a list.

        Args:
            keep (str, optional): string of characters to keep. Defaults to ARABIC_CHARS.
            sep (str, optional): separator to split text on. Defaults to \n.
        Returns:
            TextCleaner: self
        """
        assert keep is not None
        if type(keep) != list:
            keep = list(keep)
        self.lines = self._mapper(self.lines, lambda x: keep_only(x, keep))

        return self

    def _filter(self, inp_list, fn):
        assert type(inp_list) == list
        self.lines = list(filter(fn, inp_list))
        return self

    def _keep_only(self, to_keep, remove_tashkeel=True, remove_tatweel=True):
        self.lines = self._get(self, to_keep, remove_tashkeel=True, remove_tatweel=True)
        return self

    def _get(self, to_keep, remove_tashkeel=True, remove_tatweel=True):
        if type(to_keep) != list:
            to_keep = list(to_keep)
        if remove_tashkeel:
            self.remove_tashkeel()
        if remove_tatweel:
            self.remove_tatweel()
        return self._mapper(self.lines, lambda line: keep_only(line, to_keep))

    def _split_text(self, sep):
        self.raw_lines = self.raw_text.strip().split(sep)
        self.lines = self.raw_lines
        self.strip()

    def _map(self, inp_list, fn):
        self.lines = self._mapper(inp_list, fn)
        return self

    def _map_lines(self, fn):
        return self._map(self.lines, fn)

    def _mapper(self, list_map, fn):
        assert type(list_map) == list
        return list(map(fn, list_map))

    def _remove(self, remove):
        assert remove is not None
        if type(remove) != list:
            remove = list(remove)
        return self._map_lines(lambda x: replace_list(x, remove))

    # endregion
    # region additional functions
    def sample(self, num_samples=1):
        assert num_samples > 0 and num_samples < len(self)
        return random.sample(self.cleaned_data, num_samples)

    def split_on(self, symbol):
        """ Further split each line by the input "symbol"
        """
        lines = self._map_lines(lambda x: x.split(symbol))
        self.lines = [item for line in lines for item in line]

    def replace_repeated_chars(self, repeated=1, keep_char=1):
        return self._map_lines(
            lambda line: replace_repeated_chars(line, repeated, keep_char)
        )

    def strip(self):
        return self._map_lines(str.strip)

    def head(self, num_samples=1):
        assert num_samples > -1 and num_samples < len(self)
        return self.lines[:num_samples]

    def tail(self, num_samples=1):
        assert num_samples > -1 and num_samples < len(self)
        return self.lines[-num_samples:]

    # endregion
    # region keep functions
    def keep_arabic_only(self):
        return self._keep_only(ARABIC_CHARS)

    def keep_english_only(self):
        return self._keep_only(ENGLISH_CHARS)

    def keep_arabic_and_numbers_only(self):
        return self._keep_only(ARABIC_CHARS + ARABIC_NUM + ENGLISH_NUM)

    def keep_arabic_with_tashkeel_only(self):
        return self._keep_only(list(ARABIC_CHARS) + HARAKAT_MAIN, remove_tashkeel=False)

    def keep_arabic_and_english_only(self):
        return self._keep_only(ENGLISH_CHARS + ARABIC_CHARS)

    def keep_english_and_numbers_only(self):
        return self._keep_only(ENGLISH_CHARS + ENGLISH_NUM)

    # endregion
    # region get functions

    @property
    def text(self):
        return self.sep.join(self.lines)

    def get_text(self):
        return self.text

    def get_row_text(self):
        return self.raw_text

    def get_lines(self, sep="\n"):
        return self.lines

    def get_arabic_text(self):
        """Extract the Arabic text only.

        Returns:
            str: Arabic text
        """
        return self.sep.join(self._get(ARABIC_CHARS))

    def get_english_text(self):
        """Extract the English text only.

        Returns:
            str: English text
        """
        return self.sep.join(self._get(ENGLISH_CHARS))

    def get_arabic_with_numbers(self):
        """Extract Arabic text and numbers only.

        Returns:
            str: Arabic text with numbers
        """
        return self.sep.join(self._get(ARABIC_CHARS + ARABIC_NUM + ENGLISH_NUM))

    def get_arabic_with_harakat(self):
        """Extract Arabic text and harakat only.

        Returns:
            str: Arabic text with harakat
        """
        return self.sep.join(self._get(ARABIC_CHARS, remove_tashkeel=False))

    def get_unique_chars(self):
        return list(set("".join(self.lines)))

    def get_lines_below_len(self, length: int):
        return list(filter(self.lines, lambda line: len(line) < length))

    def get_lines_above_len(self, length: int):
        return list(filter(self.lines, lambda line: len(line) > length))

    def get_lines_with_len(self, length: int):
        return list(filter(self.lines, lambda line: len(line) == length))
    # endregion

    #region object operations
    def __add__(self, other):
        new_object = TextCleaner(text = "")
        new_object.lines = self.lines + other.lines
        new_object.raw_lines = new_object.lines
        new_object.raw_text = new_object.text
        return new_object

    def __sub__(self, other):
        new_object = TextCleaner(text = "")
        new_object.lines = [line for line in self.lines if line not in other.lines] + [line for line in self.other if line not in self.lines]
        new_object.raw_lines = new_object.lines
        new_object.raw_text = new_object.text
        return new_object

    def __iadd__(self, other):
        self.lines += other.lines
        return self

    def __neg__(self):
        self.lines = self.lines[::-1]
        return self
    #endregion

class FileCleaner(TextCleaner):
    def __init__(self, filepath: str, sep="\n", encoding="utf8") -> None:

        self.file = open(filepath, "r", encoding=encoding)
        super().__init__(self.file.read(), sep)


class FolderCleaner(BaseCleaner):
    pass


class StreamCleaner(TextCleaner):
    pass


class TwitterCleaner(BaseCleaner):
    pass


