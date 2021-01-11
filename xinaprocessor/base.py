from xinaprocessor.constants import *
from xinaprocessor.helper import *
from typing import List
from xinaprocessor.classes import Sequential


class BaseCleaner:
    def __init__(self, lines: List[str], stream=False) -> None:
        """Base class for all cleaners, it contains all basic functionality of the cleaner

        Args:
            lines (List[str]): list of strings
            stream (bool): whether to use streaming or not
        """
        self.lines = lines  # text to be processed
        self.stream = stream
        self._sequential = Sequential()  # used for streaming

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

    def remove_arabic_punctuation(self):
        return self._remove(ARABIC_PUNCTUATION)

    def remove_english_punctuation(self):
        return self._remove(ENGLISH_PUNCTUATION)

    def remove_other_punctuation(self):
        return self._remove(OTHER_PUNCTUATION)

    def remove_punctuation(self):
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

    # endregion
    # region internal functions

    def _filter_lines(self, fn):
        return self._filter_map(self.lines, fn)

    def _filter_map(self, inp_list, fn):
        assert type(inp_list) == list
        if self.stream:
            self._sequential.add(fn, filter)
            return self
        else:
            self.lines = list(filter(fn, inp_list))
        return self

    def _keep_only(self, to_keep, remove_tashkeel=True, remove_tatweel=True):
        self.lines = self._get(
            to_keep, remove_tashkeel=remove_tashkeel, remove_tatweel=remove_tatweel,
        )
        return self

    def _get(self, to_keep, remove_tashkeel=True, remove_tatweel=True):
        if type(to_keep) != list:
            to_keep = list(to_keep)
        if remove_tashkeel:
            self.remove_tashkeel()
        if remove_tatweel:
            self.remove_tatweel()
        return self._mapper(self.lines, lambda line: keep_only(line, to_keep))

    def _map(self, inp_list, fn):
        self.lines = self._mapper(inp_list, fn)
        return self

    def _map_lines(self, fn):
        return self._map(self.lines, fn)

    def _mapper(self, list_map, fn):
        assert type(list_map) == list

        if self.stream:
            self._sequential.add(fn, map)
            return self.lines
        else:
            return list(map(fn, list_map))

    def _remove(self, remove):
        assert remove is not None
        if type(remove) != list:
            remove = list(remove)
        return self._map_lines(lambda line: replace_list(remove, line))

    def _replace(self, replace, rep_with):
        assert replace is not None
        if type(replace) != list:
            replace = list(replace)
        return self._map_lines(lambda line: replace_list(replace, line, rep_with))

    # endregion
    # region filter functions
    def remove_empty_lines(self):
        return self.remove_lines_below_len(1)

    def remove_lines_below_len(self, length: int, word_level=True):
        filter_fn = (
            lambda line: (len(line.split())
                          if word_level else len(line)) >= length
        )
        return self._filter_lines(filter_fn)

    def remove_lines_above_len(self, length: int, word_level=True):
        filter_fn = (
            lambda line: (len(line.split())
                          if word_level else len(line)) <= length
        )
        return self._filter_lines(filter_fn)

    def remove_lines_contain_single_char(self):
        filter_fn = (
            lambda line: not contains_single_char(line))
        return self._filter_lines(filter_fn)

    def remove_lines_with_len(self, length: int, word_level=True):
        filter_fn = (
            lambda line: (len(line.split())
                          if word_level else len(line)) != length
        )
        return self._filter_lines(filter_fn)

    def remove_lines_contain(self, char: int):
        return self._filter_lines(lambda line: char not in line)

    def remove_lines_contain_persian(self):
        filter_fn = (
            lambda line: not contains_persian(line))
        return self._filter_lines(filter_fn)

    def keep_lines_contain(self, char: int):
        return self._filter_lines(lambda line: char in line)

    # endregion
    # region additional functions

    def connect_single_char(self, with_prev=False):
        return self._map_lines(remove_single_char_space_before
                               if with_prev else remove_single_char_space_after)

    def replace_repeated_chars(self, repeated=1, keep_char=1):
        return self._map_lines(
            lambda line: replace_repeated_chars(line, repeated, keep_char)
        )

    def replace_arabic_numbers_to_english(self):
        return self._map_lines(lambda line: multi_replace(ARABIC_NUM, ENGLISH_NUM, line))

    def strip(self):
        return self._map_lines(str.strip)

    # endregion
    # region keep functions

    def keep_arabic_only(self):
        return self._keep_only(ARABIC_CHARS)

    def keep_numbers_only(self):
        return self._keep_only(ARABIC_NUM + ENGLISH_NUM)

    def keep_english_only(self):
        return self._keep_only(ENGLISH_CHARS)

    def keep_arabic_and_numbers_only(self):
        return self._keep_only(ARABIC_CHARS + ARABIC_NUM + ENGLISH_NUM)

    def keep_arabic_and_english_numbers_only(self):
        return self._keep_only(ARABIC_CHARS + ENGLISH_NUM)

    def keep_arabic_with_tashkeel_only(self):
        return self._keep_only(list(ARABIC_CHARS) + HARAKAT_MAIN, remove_tashkeel=False)

    def keep_arabic_and_english_only(self):
        return self._keep_only(ENGLISH_CHARS + ARABIC_CHARS)

    def keep_english_and_numbers_only(self):
        return self._keep_only(ENGLISH_CHARS + ENGLISH_NUM)

    # endregion
    # region get functions

    def get_lines(self):
        return self.lines

    # endregion
    # region object operations
    def __getitem__(self, item):
        assert item > -1 and item < len(self), "Index must be in range."
        return self.lines[item]

    def __len__(self):
        return len(self.lines)

    def __iadd__(self, other):
        self.lines += other.lines
        return self

    def __neg__(self):
        self.lines = self.lines[::-1]
        return self

    # endregion
    # region normalize functions

    def normalize_lamalef(self):
        return self._replace(LAM_ALEF_COMBINED, LAM_ALEF_NORMAL)

    def normalize_hamza(self):
        return self._replace(HAMZA_CHARS, NORMAL_HAMZA)

    def normalize_alef(self):
        return self._replace(ALEF_CHARS, NORMAL_ALEF)

    def normalize(self):
        return self.normalize_lamalef().normalize_alef().normalize_hamza()

    def denormalize_hamza(self):
        return self._replace(HAMZA_CHARS, f"[{HAMZA_CHARS}]")

    def denormalize_alef(self):
        return self._replace(ALEF_CHARS, f"[{ALEF_CHARS}]")

    def denormalize(self):
        return self.denormalize_alef().denormalize_hamza()

    # endregion
    # region general pipeline clean functions
    def twitter_pipeline(self):
        return self.strip().remove_hashtags().remove_mentions().remove_links()

    def twitter_arabic_pipeline(self):
        return self.twitter_pipeline().keep_arabic_only().replace_repeated_chars(3, 2).remove_empty_lines()
    # endregion

    # region replace functions
    def transliteration_to_arabic(self):
        return self._map_lines(transliteration_to_arabic)

    def arabic_to_transliteration(self):
        return self._map_lines(arabic_to_transliteration)
    # endregion


class BaseProcessor:
    pass


class BaseTokenizer:
    pass
