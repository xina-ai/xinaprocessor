from xinaprocessor.base import BaseCleaner
from xinaprocessor.helper import *
import warnings
from tqdm import tqdm
import os
import sys
from typing import List
import concurrent.futures as con


class TextCleaner(BaseCleaner):
    def __init__(self, text: str, sep="\n"):
        super().__init__()

        self.sep = sep
        self.set_text(text, sep)

    @staticmethod
    def create_cleaner(text: str, sep="\n"):
        return TextCleaner(text, sep)

    @staticmethod
    def create_cleaner_from_list(lst, sep="\n"):
        cleaner = TextCleaner.create_cleaner('', sep)
        cleaner.lines = lst
        return cleaner

    def get_arabic_text(self):
        """Extract the Arabic text only.

        Returns:
            str: Arabic text
        """
        return self._join_text(self._get(ARABIC_CHARS))

    def get_english_text(self):
        """Extract the English text only.

        Returns:
            str: English text
        """
        return self._join_text(self._get(ENGLISH_CHARS))

    def get_arabic_with_numbers(self):
        """Extract Arabic text and numbers only.

        Returns:
            str: Arabic text with numbers
        """
        return self._join_text(self._get(ARABIC_CHARS + ARABIC_NUM + ENGLISH_NUM))

    def get_arabic_with_harakat(self):
        """Extract Arabic text and harakat only.

        Returns:
            str: Arabic text with harakat
        """
        return self._join_text(self._get(ARABIC_CHARS, remove_tashkeel=False))

    def get_unique_chars(self):
        return list(set("".join(self.lines)))

    def get_lines_below_len(self, length: int):
        return list(filter(self.lines, lambda line: len(line) < length))

    def get_lines_above_len(self, length: int):
        return list(filter(self.lines, lambda line: len(line) > length))

    def get_lines_with_len(self, length: int):
        return list(filter(self.lines, lambda line: len(line) == length))

    def remove_duplicates(self):
        self.lines = list(dict.fromkeys(self.lines))
        return self

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
        lines = [line for line in self.lines if line not in other.lines] + [
            line for line in other.lines if line not in self.lines
        ]
        return TextCleaner.create_cleaner_from_list(lines, self.sep)

    def __add__(self, other):
        if self.sep != other.sep:
            warnings.warn(
                f"Unequal separators detected, using {self.sep} as a new separator."
            )
        return TextCleaner.create_cleaner_from_list(self.lines + other.lines, self.sep)


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
                                            if None, all columns are processed
            header (bool, optional): true if the file contains header. Defaults to None.
        """

        super().__init__(stream=True)
        self.encoding = encoding
        self.sep = sep
        self.columns = columns if columns else []
        self.header = header
        self._set_newfile(filepath, savepath)

    def _add_split(self):
        if self.sep:
            self.split_lines_on(self.sep) if not self.columns else self.split_and_remove_lines_on(
                self.sep, self.columns)

    def _set_newfile(self, filepath, savepath):
        self.filepath = filepath
        assert os.path.isfile(filepath), "File does not exist."
        self.savepath = self._get_save_path() if not savepath else savepath
        if os.path.isfile(self.savepath):
            warnings.warn(self.savepath + ': File already exists.')
        self._add_split()

    def _get_save_path(self):
        input_filename = os.path.splitext(os.path.basename(self.filepath))[0]
        input_extention = os.path.splitext(os.path.basename(self.filepath))[1]
        savepath = os.path.join(
            os.path.dirname(self.filepath), input_filename +
            f"_cleaned{input_extention}"
        )
        return savepath

    def _handle_header(self, save=True):
        self.header = next(self.file) if self.header else None
        if self.header and save:
            self.savefile.write(self.header)

    def _prepare_handlers(self):
        self.savefile = open(self.savepath, "w", encoding=self.encoding)
        self.file = open(self.filepath, "r", encoding=self.encoding)

    def _prepare_clean(self):
        self._prepare_handlers()
        self._handle_header()

    def _get_tqdm_file(self):
        return tqdm(
            total=os.path.getsize(self.filepath),
            desc="Processing",
            unit="B",
            unit_scale=True,
            file=sys.stdout,
            # position=0,
            leave=True,
        )

    def _join_text(self, lines):
        return self.sep.join(lines) if self.sep else self.lines[0]

    def _save_lines(self, lines: List[str]):
        col_len = max(1, len(self.columns))
        for i in range(0, len(lines), col_len):
            line = self._join_text(lines[i:i + col_len])
            self.savefile.write(line + '\n')

    def _apply_and_save(self):
        cleaned = self._sequential.apply(self.lines)
        self._save_lines(cleaned)

    def clean(self, n_lines=10):
        """Clean the input file by applying all selected functions in sequence.

        Args:
            n_lines (int, optional): number of lines to be processed at the same time. Defaults to 10.
        """
        assert len(self._sequential) > 0, "No functions to apply"
        self._prepare_clean()

        self.clear_text()
        with self._get_tqdm_file() as pbar:
            if self.header:
                pbar.update(len(self.header.encode(self.encoding)))
            for i, line in enumerate(self.file, 1):
                pbar.update(len(line.encode(self.encoding)))
                self.add_text(line)
                if i % n_lines == 0:
                    self._apply_and_save()
                    self.clear_text()

        if len(self.lines) > 0:
            self._apply_and_save()

    def clean_sample(self, n_lines=1000):
        """Clean a sample of the input file by applying all selected functions in sequence.

        Args:
            n_lines (int, optional): number of lines to be processed at the same time. Defaults to 1000.
        """
        self._prepare_clean()
        self.clear_text()
        for i, line in enumerate(self.file, 1):
            self.add_text(line)
            if i % n_lines == 0:
                self._apply_and_save()
                break

    def get_unique_chars(self):
        self.file.seek(0)
        chars = set()
        with self._get_tqdm_file() as pbar:
            for line in self.file:
                pbar.update(len(line.encode(self.encoding)))
                chars.update(list(''.join(line)))
        return list(chars)

    def __del__(self):
        if hasattr(self, "file"):
            self.file.close()
        if hasattr(self, "savefile"):
            self.savefile.close()


class FolderStreamCleaner:
    def __init__(
            self, folderdir: str, savedir: str = None, include_subdir=False, encoding="utf8",
            sep: str = None, columns: List[int] = None, header: bool = None, n_jobs=4) -> None:
        self.folderdir = folderdir
        self.savedir = savedir
        self.include_subdir = include_subdir
        self.encoding = encoding
        self.sep = sep
        self.columns = columns
        self.header = header
        self.n_jobs = n_jobs
        self.files = self._get_files()

        assert len(self.files) > 0, 'No files found.'
        self.apply = BaseCleaner([], stream=True)

    def _get_files(self):
        if not hasattr(self, 'files'):
            self.files = []
            for path, _, filenames in os.walk(self.folderdir):
                self.files += [os.path.join(path, filename)
                               for filename in filenames if not filename.startswith('.')]
                if not self.include_subdir:
                    break
        return self.files

    def clean_file(self, file, sample=False):
        savefile = self._get_save_dir(file)
        filestream = FileStreamCleaner(
            file, savefile, sep=self.sep, columns=self.columns, header=self.header)
        filestream._sequential = self.apply._sequential
        clean_fn = filestream.clean_sample if sample else filestream.clean
        clean_fn()

    def _get_save_dir(self, file):
        filedir = file.replace(self.folderdir, "")
        filedir = filedir[1:] if filedir.startswith('/') else filedir
        savefile = os.path.join(
            self.savedir, filedir) if self.savedir else None
        if not os.path.isdir(os.path.dirname(savefile)):
            os.makedirs(os.path.dirname(savefile))
        return savefile

    def clean_files(self, sample=False):
        self.run(lambda file: self.clean_file(file, sample), self.files)

    def run(self, fn, my_iter):
        with con.ThreadPoolExecutor(max_workers=self.n_jobs) as executor:
            futures = []
            for item in my_iter:
                futures.append(executor.submit(fn, item))
            for i, _ in enumerate(con.as_completed(futures)):
                print(f'\n{i}/{len(self)} has been cleaned.')

    def __len__(self):
        return len(self.files)
