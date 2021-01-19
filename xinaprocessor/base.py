from xinaprocessor.constants import *
from xinaprocessor.helper import *
from typing import List
from xinaprocessor.classes import Sequential
from functools import partial, reduce
import operator


class BaseCleaner:
    def __init__(self, lines: List[str] = [], stream=False) -> None:
        """Base class for all cleaners, it contains all basic functionality of the cleaner

        Args:
            lines (List[str]): list of strings, text to be processed
            stream (bool): whether to use streaming or not
        """
        self.lines = lines
        self.stream = stream
        # used for streaming
        self._sequential = Sequential()

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
        fnc = partial(filter, fn)
        return self._apply(inp_list, fnc)

    def _apply_on_list(self, fnc):
        if self.stream:
            self._sequential.add(fnc)
        else:
            self.lines = list(fnc(self.lines))
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
        fnc = partial(map, fn)
        if self.stream:
            self._sequential.add(fnc)
            return self.lines
        else:
            return list(fnc(list_map))

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

    def _join_text(self, sep=None):
        return sep.join(self.lines) if sep else self.lines[0]

    def _flatten_list(self, indices=None):
        """Flatten a list of lists and keeps only the provided indices.
        if indices is None, all indices are kept and flattened

        Args:
            indices (List[int], optional): indices to keep from the inner. Defaults to None.
        """
        fnc = partial(map, lambda line: [item for i, item in enumerate(line)
                                         if indices is None or i in indices])
        fnc2 = partial(reduce, operator.iconcat)
        return self._apply_on_list(fnc)._apply_on_list(fnc2)
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

    def head(self, num_samples=1):
        if num_samples < 0 or num_samples >= len(self):
            raise IndexError(
                f"Number of samples must be in range [0, f{len(self)}]. Your input {num_samples}")
        return self.lines[:num_samples]

    def tail(self, num_samples=1):
        if num_samples < 0 or num_samples >= len(self):
            raise IndexError(
                f"Number of samples must be in range [0, f{len(self)}]. Your input {num_samples}")
        return self.lines[-num_samples:]

    def sample(self, num_samples=1, seed=0):
        if num_samples < 0 or num_samples >= len(self):
            raise IndexError(
                f"Number of samples must be in range [0, f{len(self)}]. Your input {num_samples}")
        random.seed(seed)
        return random.sample(self.lines, num_samples)

    def clear_text(self):
        self.lines = []
        return self

    def clear_sequential(self):
        if self.stream:
            self._sequential.clear()

    def split_lines_on(self, symbol: str):
        """Further split each line by the input "symbol"

        Args:
            symbol (str): A symbol to split on
        """
        return self._map_lines(lambda line: line.split(symbol))._flatten_list()

    def split_and_remove_lines_on(self, symbol: str, columns=List[int]):
        return self._map_lines(lambda line: line.split(symbol))._flatten_list(columns)

    def add_text(self, text: str, sep=None):
        new_lines = [text] if not sep else text.split(sep)
        self.lines.extend(new_lines)
        return self

    def set_text(self, text: str, sep=None):
        if not text:
            return self
        text = text.strip()
        self.lines = [text] if not sep else text.split(sep)
        return self.strip()

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
    # region properties

    @ property
    def text(self):
        return self._join_text('\n')
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
        if item < 0 or item >= len(self):
            raise IndexError
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
