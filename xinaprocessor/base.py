from xinaprocessor.constants import *
from xinaprocessor.helper import *
from typing import List
from xinaprocessor.classes import Sequential
from functools import partial, reduce
import operator
from xinaprocessor.decorators import show_empty_warning


@show_empty_warning
class BaseCleaner:
    """Base class for all cleaners, it contains all basic functionality of the cleaner

    Args:
        lines (List[str]): list of strings, text to be processed
        stream (bool): whether to use streaming or not
    """

    def __init__(self, lines: List[str] = [], stream=False) -> None:
        self.lines = lines
        self.stream = stream
        # used for streaming
        self._sequential = Sequential()

    # region remove functions
    def remove_english_text(self):
        """Removes english characters from text.
        """
        return self._remove(ENGLISH_CHARS)

    def remove_arabic_text(self):
        """Removes arabic characters from text.
        """
        return self._remove(ARABIC_CHARS)

    def remove_numbers(self):
        """Removes english and arabic numbers from text.
        """
        return self._remove(ENGLISH_NUM + ARABIC_NUM)

    def remove_arabic_numbers(self):
        """Removes arabic numbers from text.
        """
        return self._remove(ARABIC_NUM)

    def remove_english_numbers(self):
        """Removes english numbers from text.
        """
        return self._remove(ENGLISH_NUM)

    def remove_arabic_punctuations(self):
        """Removes arabic punctuations from text.
        """
        return self._remove(ARABIC_PUNCTUATION)

    def remove_english_punctuations(self):
        """Removes english punctuations from text.
        """
        return self._remove(ENGLISH_PUNCTUATION)

    def remove_other_punctuations(self):
        """Removes all punctuations other than english and arabic punctuations from text.
        """
        return self._remove(OTHER_PUNCTUATION)

    def remove_punctuations(self):
        """Removes all punctuations from text.
        """
        return self._remove(PUNCTUATION)

    def remove_tashkeel_main(self):
        """Removes the 8 known arabic harakat from text.
        """
        return self._remove(HARAKAT_MAIN)

    def remove_tashkeel_other(self):
        """Removes less known arabic harakat from text.
        """
        return self._remove(HARAKAT_OTHERS)

    def remove_tashkeel(self):
        """Removes all arabic harakat from text.
        """
        return self._remove(HARAKAT)

    def remove_tatweel(self):
        """Removes tatweel symbol "\u0640" from text.
        """
        return self._remove(TATWEEL)

    def remove_extra_spaces(self, keep_space=1):
        """Removes extra spaces from text

        Args:
            keep_space (int, optional): number of maximum spaces to keep. Defaults to 1.
        """
        return self._map_lines(lambda line: remove_extra_spaces(line, keep_space))

    def remove_emojis(self):
        """Removes all emojis using emojis library
        """
        return self._map_lines(remove_emoji)

    def remove_hashtags(self):
        """Removes all hashtags from text
        """
        return self._map_lines(remove_hashtags)

    def remove_emails(self):
        """Removes all emails address from text
        """
        return self._map_lines(remove_emails)

    def remove_quranic_annotations(self):
        """Removes all quranic annotations from text
        """
        return self._remove(QURANIC_ANNOTATION)

    def remove_honorific_signs(self):
        """Removes all honorific signs from text
        """
        return self._remove(HONORIFIC_SIGN)

    def remove_links(self):
        """Removes all links from text
        """
        return self._map_lines(remove_links)

    def remove_mentions(self):
        """Removes all mentions from text
        """
        return self._map_lines(remove_mentions)

    # endregion
    # region internal functions

    def _filter_lines(self, fn):
        return self._filter_map(self.lines, fn)

    def _filter_map(self, inp_list, fn):
        assert isinstance(inp_list, list)
        fnc = partial(filter, fn)
        return self._apply(inp_list, fnc)

    def _apply_on_lines(self, fnc):
        return self._apply(self.lines, fnc)

    def _apply(self, inp_list, fnc):
        if self.stream:
            self._sequential.add(fnc)
        else:
            self.lines = list(fnc(inp_list))
        return self

    def _keep_only(self, to_keep, remove_tashkeel=True, remove_tatweel=True):
        self.lines = self._get(
            to_keep, remove_tashkeel=remove_tashkeel, remove_tatweel=remove_tatweel,
        )
        return self

    def _get(self, to_keep, remove_tashkeel=True, remove_tatweel=True):
        if not isinstance(to_keep, list):
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
        assert isinstance(list_map, list)
        fnc = partial(map, fn)
        if self.stream:
            self._sequential.add(fnc)
            return self.lines
        else:
            return list(fnc(list_map))

    def _remove(self, remove):
        assert remove is not None
        if not isinstance(remove, list):
            remove = list(remove)
        return self._map_lines(lambda line: replace_list(remove, line))

    def _replace(self, replace, rep_with):
        assert replace is not None
        if not isinstance(replace, list):
            replace = list(replace)
        return self._map_lines(lambda line: replace_list(replace, line, rep_with))

    def _join_text(self, lines, sep):
        return sep.join(lines).strip() if sep else lines[0]

    def _flatten_list(self, indices=None):
        """Flatten a list of lists and keeps only the provided indices.
        if indices is None, all indices are kept and flattened

        Args:
            indices (List[int], optional): indices to keep from the inner. Defaults to None.
        """
        fnc = partial(map, lambda line: [item for i, item in enumerate(line)
                                         if indices is None or i in indices])
        fnc2 = partial(reduce, operator.iconcat)
        return self._apply_on_lines(fnc)._apply_on_lines(fnc2)
    # endregion
    # region filter functions

    def drop_lines_below_count(self, symbol: str, threshold: int):
        """Drops any line has frequency for a certain symbol below the threshold
        """
        filter_fn = (
            lambda line: line.count(symbol) >= threshold
        )
        return self._filter_lines(filter_fn)

    def drop_lines_above_count(self, symbol: str, threshold: int):
        """Drops any line has frequency for a certain symbol more than the threshold
        """
        filter_fn = (
            lambda line: line.count(symbol) <= threshold
        )
        return self._filter_lines(filter_fn)

    def drop_empty_lines(self):
        """Drop all empty lines.
        """
        return self.drop_lines_below_len(1)

    def drop_lines_below_len(self, length: int, word_level=True):
        """Drop all lines below a certain length

        Args:
            length (int): Number of characters or words to use
            word_level (bool, optional): False to use character level. Defaults to True.
        """
        filter_fn = (
            lambda line: (len(line.split())
                          if word_level else len(line)) >= length
        )
        return self._filter_lines(filter_fn)

    def drop_lines_above_len(self, length: int, word_level=True):
        """Drop all lines above a certain length

        Args:
            length (int): Number of characters or words to use
            word_level (bool, optional): False to use character level. Defaults to True.
        """
        filter_fn = (
            lambda line: (len(line.split())
                          if word_level else len(line)) <= length
        )
        return self._filter_lines(filter_fn)

    def drop_lines_with_len(self, length: int, word_level=True):
        """Drop all lines with a certain length

        Args:
            length (int): Number of characters or words to use
            word_level (bool, optional): False to use character level. Defaults to True.
        """
        filter_fn = (
            lambda line: (len(line.split())
                          if word_level else len(line)) != length
        )
        return self._filter_lines(filter_fn)

    def drop_lines_contain_single_char(self):
        """Drop all lines contain at least a single character word (single character between spaces or
        single character at start or end of a line)

        Args:
            length (int): Number of characters or words to use
            word_level (bool, optional): False to use character level. Defaults to True.
        """
        filter_fn = (
            lambda line: not contains_single_char(line))
        return self._filter_lines(filter_fn)

    def drop_lines_with_repeated_chars(self, repeated=3):
        """Drop all lines with certain number of consecutively repeated characters.

        Args:
            repeated (int, optional): number of consecutively repeated characters. Defaults to 3.
        """
        return self._filter_lines(
            lambda line: not contains_repeated_chars(line, repeated)
        )

    def drop_lines_contain(self, input_string: str):
        """Drop all lines contain a certain string

        Args:
            input_string (str): string to match lines on
        """
        return self._filter_lines(lambda line: input_string not in line)

    def drop_lines_contain_persian(self):
        """Drop all lines contain persian specific characters
        """
        filter_fn = (
            lambda line: not contains_persian(line))
        return self._filter_lines(filter_fn)

    def drop_lines_contain_english(self):
        """Drop all lines contain english character
        """
        filter_fn = (
            lambda line: not contains_english(line))
        return self._filter_lines(filter_fn)

    def keep_lines_contain(self, input_string: int):
        """Keep only all lines contain a certain string

        Args:
            input_string (str): string to match lines on
        """
        return self._filter_lines(lambda line: input_string in line)

    # endregion
    # region additional functions

    def clear_text(self):
        """Clear text. Text should be added before you can clean again.
        """
        self.lines = []
        return self

    def clear_sequential(self):
        """Clear all functions that will be applied to the text when streaming is true
        """
        if self.stream:
            self._sequential.clear()

    def split_lines_on(self, symbol: str):
        """Further split each line by the input "symbol".
        Number of lines will increase by the number of splits applied.

        Args:
            symbol (str): Symbol to split on
        """
        return self._map_lines(lambda line: line.split(symbol))._flatten_list()

    def split_and_remove_lines_on(self, symbol: str, columns: List[int]):
        """Further split each line by the input "symbol" and keeps only (columns) indices

        Args:
            symbol (str): Symbol to split on
            columns (List[int]): columns to keep after splitting.
        """
        return self._map_lines(lambda line: line.split(symbol))._flatten_list(columns)

    def add_text(self, text: str, sep: str = None):
        """Add more text to be processed

        Args:
            text (str): input text to add
            sep (str, optional): separator to split text if needed. Defaults to None.
        """
        new_lines = [text] if not sep else text.split(sep)
        self.lines.extend(new_lines)
        return self

    def set_text(self, text: str, sep: str = None):
        """Replace text with a new text

        Args:
            text (str): input text to add
            sep (str, optional): separator to split text if needed. Defaults to None.
        """
        if not text:
            return self
        text = text.strip()
        self.lines = [text] if not sep else text.split(sep)
        return self.strip()

    def connect_single_char(self, with_prev=False):
        """Connect all single character word with the previous or next word.

        Normally used to connect conjunctions or other letters with the next word.

        Args:
            with_prev (bool, optional): True to connect with the previous word. Defaults to False.
        """
        return self._map_lines(remove_single_char_space_before
                               if with_prev else remove_single_char_space_after)

    def replace_repeated_chars(self, repeated=3, keep_char=1):
        """Keep only certain number of consecutively repeated characters.

        Consecutively repeated (repeated or higher) times characters will be kept (keep_char) times

        Args:
            repeated (int, optional): number of consecutively repeated characters. Defaults to 3.
            keep_char (int, optional): number of characters to keep. Defaults to 1.
        """
        return self._map_lines(
            lambda line: replace_repeated_chars(line, repeated, keep_char)
        )

    def replace_except(self, keep_symbols: str, replace_by: str):
        return self._map_lines(
            lambda line: replace_except(line, keep_symbols, replace_by)
        )

    def convert_arabic_numbers_to_english(self):
        """Convert arabic numbers to english numbers.
        """
        return self._map_lines(lambda line: multi_replace(ARABIC_NUM, ENGLISH_NUM, line))

    def strip(self):
        """Strip left and right spaces from all lines in text.
        """
        return self._map_lines(str.strip)

    # endregion
    # region properties

    @ property
    def text(self):
        return '\n'.join(self.lines)
    # endregion
    # region keep functions

    def keep_arabic_only(self):
        """Keep arabic text only.
        """
        return self._keep_only(ARABIC_CHARS)

    def keep_numbers_only(self):
        """Keep arabic and english numbers only.
        """
        return self._keep_only(ARABIC_NUM + ENGLISH_NUM)

    def keep_english_only(self):
        """Keep english text only.
        """
        return self._keep_only(ENGLISH_CHARS)

    def keep_arabic_and_numbers_only(self):
        """Keep arabic text and arabic and english numbers only.
        """
        return self._keep_only(ARABIC_CHARS + ARABIC_NUM + ENGLISH_NUM)

    def keep_arabic_and_english_numbers_only(self):
        """Keep arabic text and english numbers only.
        """
        return self._keep_only(ARABIC_CHARS + ENGLISH_NUM)

    def keep_arabic_with_tashkeel_only(self):
        """Keep arabic text and main harakat only.
        """
        return self._keep_only(list(ARABIC_CHARS) + HARAKAT_MAIN, remove_tashkeel=False)

    def keep_arabic_and_english_only(self):
        """Keep arabic and english text only.
        """
        return self._keep_only(ENGLISH_CHARS + ARABIC_CHARS)

    def keep_english_and_numbers_only(self):
        """Keep englsih text and english numbers only.
        """
        return self._keep_only(ENGLISH_CHARS + ENGLISH_NUM)

    # endregion

    # region swap functions
    def swap_tanween_alef(self):
        """swap the tanween alef pattern by alef then tanween 
        """
        return self._map_lines(swap_tanween_alef)

    # endregion

    # region get functions

    def get_lines(self):
        """Return lines

        Returns:
            List[str]: list of all lines
        """
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
        """Convert single lam_alef char to two characters lam and alef
        """
        return self._replace(LAM_ALEF_COMBINED, LAM_ALEF_NORMAL)

    def normalize_hamza(self):
        """Convert all hamza variations to the normal hamza
        """
        return self._replace(HAMZA_CHARS, NORMAL_HAMZA)

    def normalize_alef(self):
        """Convert all alef variations to the normal alef
        """
        return self._replace(ALEF_CHARS, NORMAL_ALEF)

    def normalize_tah_marbota(self):
        """Convert all tah marbota to ha
        """
        return self._replace(TAH_MARBOTA, HA)

    def normalize_alef_maksora(self):
        """Convert all alef maksora to ya
        """
        return self._replace(ALEF_MAKSORA, YA)

    def normalize(self):
        """Convert all alef variations to the normal alef,
        convert single lam_alef char to two characters lam and alef, and
        convert all tah marbota to ha
        """
        return self.normalize_lamalef().normalize_alef().normalize_tah_marbota()

    def denormalize_hamza(self):
        """Convert normal hamza to all possible hamza forms
        """
        return self._replace(HAMZA_CHARS, f"[{HAMZA_CHARS}]")

    def denormalize_alef(self):
        """Convert normal alef to all possible alef forms
        """
        return self._replace(ALEF_CHARS, f"[{ALEF_CHARS}]")

    def denormalize(self):
        """Convert normal alef and hamza to all possible forms
        """
        return self.denormalize_alef().denormalize_hamza()

    # endregion
    # region general pipeline clean functions
    def twitter_pipeline(self):
        """Clean twitter text by removing hashtags, mentions and links
        """
        return self.strip().remove_hashtags().remove_mentions().remove_links()

    def twitter_arabic_pipeline(self):
        """Clean arabic twitter text by removing hashtags, mentions and links.
        Then, keep only arabic text, replace repeated characters and drop empty lines.
        """
        return self.twitter_pipeline().keep_arabic_only().replace_repeated_chars(3, 2).drop_empty_lines()
    # endregion

    # region replace functions
    def transliteration_to_arabic(self):
        return self._map_lines(transliteration_to_arabic)

    def arabic_to_transliteration(self):
        return self._map_lines(arabic_to_transliteration)
    # endregion
