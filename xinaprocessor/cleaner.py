from typing import Text
from xinaprocessor.base import BaseCleaner
from xinaprocessor.helper import *
import warnings


class TextCleaner(BaseCleaner):
    def __init__(self, text: str, sep="\n") -> None:
        super().__init__()

        self.raw_lines = self._split_text(sep)
        self.sep = sep

    @property
    def text(self):
        return self.sep.join(self.lines)

    @property
    def raw_text(self):
        return self.sep.join(self.raw_lines)

    def get_text(self):
        return self.text

    def get_row_text(self):
        return self.raw_text

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

    def __sub__(self, other):
        if self.sep != other.sep:
            warnings.warn(
                f"Unequal separators detected, using {self.sep} as a new separator."
            )
        new_object = TextCleaner("", self.sep)
        new_object.lines = [line for line in self.lines if line not in other.lines] + [
            line for line in other.lines if line not in self.lines
        ]
        new_object.raw_lines = self.raw_lines + other.raw_lines
        new_object.raw_text = self.raw_text + other.raw_text

    def __add__(self, other):
        if self.sep != other.sep:
            warnings.warn(
                f"Unequal separators detected, using {self.sep} as a new separator."
            )
        new_object = TextCleaner("", self.sep)
        new_object.lines = self.lines + other.lines
        new_object.raw_lines = self.raw_lines + other.raw_lines
        new_object.raw_text = self.raw_text + other.raw_text


class FileCleaner(TextCleaner):
    def __init__(self, filepath: str, sep="\n", encoding="utf8") -> None:

        self.file = open(filepath, "r", encoding=encoding)
        super().__init__(self.file.read(), sep)


class FolderCleaner(BaseCleaner):
    pass


class TextStreamCleaner(TextCleaner):
    pass


class TwitterCleaner(BaseCleaner):
    pass
