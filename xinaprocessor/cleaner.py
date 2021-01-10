from xinaprocessor.base import BaseCleaner
from xinaprocessor.helper import *
import warnings
from tqdm import tqdm
import os
import sys
from typing import List


class TextCleaner(BaseCleaner):
    def __init__(self, text: str, sep="\n") -> None:

        super().__init__([])
        self.raw_text = text
        self.sep = sep
        self.raw_lines = self._split_text(sep)

    @property
    def text(self):
        return self.sep.join(self.lines)

    def get_text(self):
        return self.text

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
        return random.sample(self.lines, num_samples)

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
    def __init__(self, filepath: str, encoding="utf8", sep="\n") -> None:

        self.file = open(filepath, "r", encoding=encoding)
        super().__init__(self.file.read(), '\n')


class FolderCleaner(BaseCleaner):
    pass


class FileStreamCleaner(BaseCleaner):
    def __init__(self, filepath: str, savepath: str = None, encoding="utf8",
                 sep: str = None, columns: List[int] = None, header: bool = None) -> None:
        """Clean file in a streaming manner (fast + memory efficient)

        Args:
            filepath (str): path of the file to be processed
            savepath (str, optional): path to save processed text. Defaults to None (saved in the same directory of filepath).
            encoding (str, optional): encoding of the input file. Defaults to "utf8".
            sep (str, optional): to split coulmns when needed. Defaults to None.
            columns (List[int], optional): index of the column to be processed. Defaults to None.
            header (bool, optional): true if the file contains header. Defaults to None.
        """

        self.encoding = encoding
        self.sep = sep
        self.columns = columns if columns else []
        self.header = header
        self._set_newfile(filepath, savepath)

        super().__init__([], True)

    def _set_newfile(self, filepath, savepath=None):
        assert os.path.isfile(filepath), "File does not exist."
        if not savepath:
            savepath = self._get_save_path()
        assert not os.path.isfile(savepath), "File already exists."
        self.filepath = filepath
        self._prepare_handlers()

    def _prepare_handlers(self):
        self.file = open(self.filepath, "r", encoding=self.encoding)
        self.savefile = open(self.savepath, "w", encoding=self.encoding)
        self._handle_header()

    def _get_save_path(self):
        input_filename = os.path.splitext(os.path.basename(self.filepath))[0]
        input_extention = os.path.splitext(os.path.basename(self.filepath))[1]
        savepath = os.path.join(
            os.path.dirname(self.filepath), input_filename +
            f"_cleaned{input_extention}"
        )
        return savepath

    def _handle_header(self):
        self.header = next(self._read_line()) if self.header else None
        if self.header:
            self._save_lines(self.header)

    def _read_line(self, pbar=None):

        with tqdm(
            total=os.path.getsize(self.filepath),
            desc="Processing",
            unit="B",
            unit_scale=True,
            file=sys.stdout,
            position=0,
            leave=True,
        ) as pbar:
            if len(self.columns):
                for line in self.file:
                    pbar.update(len(line.encode(self.encoding)))
                    line = line.strip().split(self.sep)
                    line = [line[i] for i in self.columns]
                    yield line
            else:
                for line in self.file:
                    pbar.update(len(line.encode(self.encoding)))
                    yield [line]

    def _save_lines(self, lines: List[str]):
        col_len = max(1, len(self.columns))
        for i in range(0, len(lines), col_len):
            line = self.sep.join(lines[i:i+col_len])
            self.savefile.write(line + '\n')

    def _apply_and_save(self, lines):
        cleaned = self._sequential.apply(lines)
        self._save_lines(cleaned)

    def clean(self, n_lines=10):
        """Clean the input file by applying all selected functions in sequence.

        Args:
            n_lines (int, optional): number of lines to be processed at the same time. Defaults to 10.
        """
        assert len(self._sequential) > 0, "No functions to apply"
        lines = []
        for i, line in enumerate(self._read_line(), 1):
            lines.extend(line)
            if i % n_lines == 0:
                self._apply_and_save(lines)
                lines = []

        if len(lines) > 0:
            self._apply_and_save(lines)

    def clean_sample(self, n_lines=1000):
        """Clean a sample of the input file by applying all selected functions in sequence.

        Args:
            n_lines (int, optional): number of lines to be processed at the same time. Defaults to 1000.
        """
        lines = []
        for i, line in enumerate(self._read_line(), 1):
            lines.extend(line)
            if i % n_lines == 0:
                self._apply_and_save(lines)
                break

    def __del__(self):
        if hasattr(self, "file"):
            del self.file, self.savefile


class FolderStreamCleaner:
    def __init__(
            self, folderdir: str, savedir: str = None, include_subdir=False, encoding="utf8",
            sep: str = None, columns: List[int] = None, header: bool = None) -> None:
        self.folderdir = folderdir
        self.savedir = savedir
        self.include_subdir = include_subdir
        self.encoding = encoding
        self.sep = sep
        self.columns = columns
        self.header = header
        self.files = self._get_files()

        assert len(self.files) > 0, 'No files found.'
        self.filestream = FileStreamCleaner(
            self.files[0], sep=',', columns=[0], header=True)

    def _get_files(self):
        if len(self.files) == 0:
            for path, _, filenames in os.walk(self.folderdir):
                self.files += [os.path.join(path, filename)
                               for filename in filenames]
                if not self.include_subdir:
                    break
        return self.files

    def clean_file(self, file, sample=False):
        savefile = os.path.join(self.savedir, file.replace(
            self.folderdir, "")) if self.savedir else None
        self.filestream._set_newfile(file, savefile)
        clean_fn = self.filestream.clean_sample if sample else self.filestream.clean
        clean_fn()

    def clean_files(self, sample=False):
        for file in self.files:
            self.clean_file(file, sample)

    def __len__(self):
        return len(self.files)
