from xinaprocessor.base import BaseCleaner
from xinaprocessor.helper import *
import warnings
from tqdm import tqdm
import os
import sys


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

    def get_unique_chars(self):
        return list(set("".join(self.lines)))

    def get_lines_below_len(self, length: int):
        return list(filter(self.lines, lambda line: len(line) < length))

    def get_lines_above_len(self, length: int):
        return list(filter(self.lines, lambda line: len(line) > length))

    def get_lines_with_len(self, length: int):
        return list(filter(self.lines, lambda line: len(line) == length))

    def head(self, num_samples=1):
        assert num_samples > -1 and num_samples < len(self)
        return self.lines[:num_samples]

    def tail(self, num_samples=1):
        assert num_samples > -1 and num_samples < len(self)
        return self.lines[-num_samples:]

    def sample(self, num_samples=1, seed=0):
        assert num_samples > 0 and num_samples < len(self)
        random.seed(seed)
        return random.sample(self.cleaned_data, num_samples,)

    def split_on(self, symbol):
        """ Further split each line by the input "symbol"
        """
        lines = self._map_lines(lambda x: x.split(symbol))
        self.lines = [item for line in lines for item in line]

    def remove_duplicates(self):
        self.lines = list(dict.fromkeys(self.lines))
        return self

    def _split_text(self, sep):
        self.lines = self.raw_text.strip().split(sep)
        self.strip()
        return self.lines

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


class FileStreamCleaner(BaseCleaner):
    def __init__(self, filepath: str, savepath: str = None, encoding="utf8") -> None:

        self.filepath = filepath
        self.encoding = encoding

        if not savepath:
            input_filename = os.path.splitext(os.path.basename(filepath))[0]
            input_extention = os.path.splitext(os.path.basename(filepath))[1]
            savepath = os.path.join(
                os.path.dirname(filepath), input_filename + f"_cleaned{input_extention}"
            )
        assert os.path.isfile(filepath), "File does not exist."
        assert not os.path.isfile(savepath), "File already exists."

        self.file = open(filepath, "r", encoding=encoding)
        self.savefile = open(savepath, "w", encoding=encoding)
        super().__init__([], True)

    def clean(self, n_lines=10):
        """Clean the input file by applying all selected functions in sequence.

        Args:
            n_lines (int, optional): number of lines to be processed at the same time. Defaults to 10.
        """
        assert len(self._sequential) > 0, "No functions to apply"
        lines = []
        with tqdm(
            total=os.path.getsize(self.filepath),
            desc="Processing",
            unit="B",
            unit_scale=True,
            file=sys.stdout,
            position=0,
            leave=True,
        ) as pbar:
            for i, line in enumerate(self.file, 1):
                pbar.update(len(line.encode(self.encoding)))
                lines.append(line)
                if i % n_lines == 0:
                    self._apply_and_save(lines)
                    lines = []

            if len(lines) > 0:
                self._apply_and_save(lines)

    def _apply_and_save(self, lines):
        cleaned = self._sequential.apply(lines)
        self.savefile.writelines("%s\n" % l for l in cleaned)

    def clean_sample(self, n_lines=1000):
        """Clean a sample of the input file by applying all selected functions in sequence.

        Args:
            n_lines (int, optional): number of lines to be processed at the same time. Defaults to 1000.
        """
        lines = []
        for i, line in enumerate(self.file, 1):
            lines.append(line)
            if i % n_lines == 0:
                self._apply_and_save(lines)
                break

    def __del__(self):
        if hasattr(self, "file"):
            del self.file, self.savefile


class FolderStreamCleaner(FileStreamCleaner):
    pass
