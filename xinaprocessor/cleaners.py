from xinaprocessor.base import BaseCleaner
from xinaprocessor.helper import *
import warnings
from tqdm import tqdm
import os
import sys
from typing import List
import concurrent.futures as con
from statistics import median_grouped, stdev, variance


class TextCleaner(BaseCleaner):
    def __init__(self, text: str, sep: str = "\n"):
        """A class to clean text.

        Args:
            text (str): Input text to be cleaned.
            sep (str, optional): Separator to split text on. Defaults to "\n".
        """
        super().__init__()

        self.sep = sep
        self.set_text(text, sep)

    @staticmethod
    def create_cleaner(text: str, sep: str = "\n"):
        r"""Creates a TextCleaner object given text and sep.

        Args:
            text (str): Input text to be cleaned.
            sep (str, optional): Separator to split text on. Defaults to "\\n".

        Returns:
            TextCleaner: text cleaner object.
        """
        return TextCleaner(text, sep)

    @staticmethod
    def create_cleaner_from_list(lst: List[str], sep: str = "\n"):
        r"""Creates a TextCleaner object given list of lines.

        Args:
            lst (List[str]): List of lines to be cleaned
            sep (str, optional): Separator used to join the lines. Defaults to "\\n".

        Returns:
            TextCleaner: text cleaner object.
        """
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
        """Extracts all unique characters in the text

        Returns:
            List[str]: List of all unique characters
        """
        return list(set("".join(self.lines)))

    def get_lines_below_len(self, length: int):
        """Extracts lines with length below a threshold

        Args:
            length (int): length of characters to consider.

        Returns:
            List[str]: list of lines with length of characters below `length`
        """
        return list(filter(self.lines, lambda line: len(line) < length))

    def get_lines_above_len(self, length: int):
        """Extracts lines with length above a threshold

        Args:
            length (int): length of characters to consider.

        Returns:
            List[str]: list of lines with length of characters above `length`
        """
        return list(filter(self.lines, lambda line: len(line) > length))

    def get_lines_with_len(self, length: int):
        """Extracts lines with length equal to a threshold

        Args:
            length (int): length of characters to consider.

        Returns:
            List[str]: list of lines with length of characters equal to `length`
        """
        return list(filter(self.lines, lambda line: len(line) == length))

    def count_lines_with_contain(self, text: str):
        return list(filter(self.lines, lambda line: text in line))

    def get_lines_lens(self) -> list:
        """Returns the a list of lengths, where each element in the list represents
         the length of the corresponding line
        """
        return list(map(len, self.lines))

    def get_max_len(self) -> int:
        """Returns the length of the line with the highest length
        """
        return max(self.get_lines_lens())

    def get_min_len(self) -> int:
        """Returns the length of the line with the lowest length
        """
        return min(self.get_lines_lens())

    def get_avg_len(self) -> float:
        """Returns the average of all lines' length
        """
        return sum(self.get_lines_lens()) / len(self)

    def get_median_len(self) -> float:
        """Returns the Median of all lines' length
        """
        return median_grouped(self.get_lines_lens())

    def get_var_len(self) -> float:
        """Returns the variance of all lines' length
        """
        return variance(self.get_lines_lens())

    def get_std_len(self) -> float:
        """Returns the standard deviation of all lines' length
        """
        return stdev(self.get_lines_lens())

    def describe_lines_len(self) -> dict:
        """Return dictionary contains a statistical description about the lines' lengths
        """
        lines_lens = self.get_lines_lens()
        return {"max_length": max(lines_lens),
                "min_length": min(lines_lens),
                "average_length": sum(lines_lens) / len(lines_lens),
                "median_length": median_grouped(lines_lens),
                "length_variance": variance(lines_lens),
                "length_standard_deviation": stdev(lines_lens)
                }

    def head(self, num_samples=1):
        """Return lines from the start of the text

        Args:
            num_samples (int, optional): number of lines to return. Defaults to 1.

        Raises:
            IndexError: If index is out of range.

        Returns:
            List[str]: list of top (num_samples) strings
        """
        if num_samples < 0 or num_samples >= len(self):
            raise IndexError(
                f"Number of samples must be in range [0, f{len(self)}]. Your input {num_samples}")
        return self.lines[:num_samples]

    def tail(self, num_samples=1):
        """Return lines from the end of the text

        Args:
            num_samples (int, optional): number of lines to return. Defaults to 1.

        Raises:
            IndexError: If index is out of range.

        Returns:
            List[str]: list of bottom (num_samples) strings
        """
        if num_samples < 0 or num_samples >= len(self):
            raise IndexError(
                f"Number of samples must be in range [0, f{len(self)}]. Your input {num_samples}")
        return self.lines[-num_samples:]

    def sample(self, num_samples=1, seed=None):
        """Randomly select sample from text

        Args:
            num_samples (int, optional): number of lines to select. Defaults to 1.
            seed (int, optional): seed for reproducibility. Defaults to 0.

        Raises:
            IndexError: If index is out of range.

        Returns:
            List[str]: list of randomly selected (num_samples) strings
        """
        if num_samples < 0 or num_samples >= len(self):
            raise IndexError(
                f"Number of samples must be in range [0, f{len(self)}]. Your input {num_samples}")
        if seed:
            random.seed(seed)
        return random.sample(self.lines, num_samples)

    def remove_duplicates(self):
        """Remove all duplicates from text
        """
        self.lines = list(dict.fromkeys(self.lines))
        return self

    def save2file(self, path: str, encoding = 'utf-8'):
        """Save text to file

        Args:
            path (str): file path to save the text to
            encoding (optional str): file encoding, default 'utf-8'

        Raises:
            FileExistsError: If file already exists
        """
        if os.path.isfile(path):
            raise FileExistsError('File already exists.')
        with open(path, 'w', encoding=encoding) as f:
            f.write('\n'.join(self.lines))
        print(f'File is saved to {path}.')

    def _clean(self, keep):
        """Clean the text by keeping only "keep" string.

        Args:
            keep (str, optional): string of characters to keep. Defaults to ARABIC_CHARS.
        Returns:
            TextCleaner: self
        """
        assert keep is not None
        if not isinstance(keep, list):
            keep = list(keep)
        self.lines = self._mapper(self.lines, lambda x: keep_only(x, keep))

        return self

    def _check_sep(self, other):
        if self.sep != other.sep:
            warnings.warn(
                f"Unequal separators detected, using {self.sep} as a new separator."
            )

    def __sub__(self, other):
        self._check_sep()
        lines = [line for line in self.lines if line not in other.lines] + [
            line for line in other.lines if line not in self.lines
        ]
        return TextCleaner.create_cleaner_from_list(lines, self.sep)

    def __add__(self, other):
        self._check_sep()
        return TextCleaner.create_cleaner_from_list(self.lines + other.lines, self.sep)


class FileCleaner(TextCleaner):
    """Process and clean file

    Args:
        filepath (str): path of the file to be processed
        savepath (str, optional): path to save the processed text. Defaults to None
        encoding (str, optional): encoding of the input file. Defaults to "utf8".
        header (bool, optional): true if the file contains header. Defaults to None.
        large (bool, optional): true if you want to process large files. Defaults to False

    Raises:
        FileNotFoundError: If file does not exist.
        OSError: If file size is larger than 1 GB.

    Examples:
    """

    def __init__(self, filepath: str, savepath: str = None, encoding="utf8",
                 header: bool = None, large: bool = False) -> None:

        if not os.path.isfile(filepath):
            raise FileNotFoundError("File does not exist.")
        # raise error if the file size is larger than one GB
        if not large and os.path.getsize(filepath) / 2 ** 30 > 1:
            raise OSError("File too large. It is prefable to use FileStreamCleaner instead.\n"
                          "Use large=True to disable this error.")

        self.file = open(filepath, "r", encoding=encoding)
        self.savepath = savepath
        self.encoding = encoding

        if header:
            self.file = next(self.file)
        super().__init__(self.file.read())

    def save(self):
        self.save2file(self.savepath, self.encoding)


class FileStreamCleaner(BaseCleaner):
    """Clean file in a streaming manner (fast + memory efficient)

    Args:
        filepath (str): path of the file to be processed
        savepath (str, optional): path to save the processed text. Defaults to None
            If None, the file will be saved in the same directory with a suffix '_cleaned'.
        encoding (str, optional): encoding of the input file. Defaults to "utf8".
        sep (str, optional): separator to split columns if needed. Defaults to None.
        columns (List[int], optional): index of the column to be processed. Defaults to None.
            If None, all columns will be processed
            Will only be applied when sep is specified.
        header (bool, optional): true if the file contains header. Defaults to None.
    """

    def __init__(self, filepath: str, savepath: str = None, encoding="utf8",
                 sep: str = None, columns: List[int] = None, header: bool = None) -> None:
        super().__init__(stream=True)
        self.encoding = encoding
        self.sep = sep
        self.columns = columns or []
        self.header = header
        self._set_newfile(filepath, savepath)

    def _add_split(self):
        if self.sep:
            self.split_lines_on(self.sep) if not self.columns else self.split_and_remove_lines_on(
                self.sep, self.columns)

    def _set_newfile(self, filepath, savepath):
        self.filepath = filepath
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"File {filepath} does not exist.")
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

    def _get_tqdm(self):
        return tqdm(
            total=os.path.getsize(self.filepath),
            desc="Processing",
            unit="B",
            unit_scale=True,
            file=sys.stdout,
            # position=0,
            leave=True,
        )

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
        if len(self._sequential) == 0:
            raise ValueError(
                "Make sure to call the functions you want before start cleaning.")
        self._prepare_clean()

        self.clear_text()
        with self._get_tqdm() as pbar:
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
            n_lines (int, optional): number of lines to process. Defaults to 1000.
        """
        self._prepare_clean()
        self.clear_text()
        for i, line in enumerate(self.file, 1):
            self.add_text(line)
            if i % n_lines == 0:
                self._apply_and_save()
                break

    def get_unique_chars(self):
        """Find all unique characters presented in the file

        Returns:
            List[str]: list of all unique characters
        """
        self.file.seek(0)
        chars = set()
        with self._get_tqdm() as pbar:
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
    """Process all files in a given folder

    Args:
        folderdir (str): path of the folder in which all files will be processed
        savedir (str, optional): save directory path. Defaults to None.
            If None, files will be saved in the same directory with suffix '_cleaned'.
            Files will be saved in the same tree structure.
        include_subdir (bool, optional): If True, files in sub directories will be processed. Defaults to False.
        encoding (str, optional): encoding of the input file. Defaults to "utf8".
        sep (str, optional): separator to split columns if needed. Defaults to None.
        columns (List[int], optional): index of the column to be processed. Defaults to None.
            If None, all columns will be processed.
            Will only be applied when sep is specified.
        header (bool, optional): true if the files contain header. Defaults to None.
        n_jobs (int, optional): number of files to be processed at the same time. Defaults to 4.

    Raises:
        ValueError: if no files are found.
    """

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

        if len(self.files) == 0:
            raise ValueError(
                f"No files were found in {folderdir}. You can use 'include_subdir' to look in sub directories.")
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
        """Clean a file by applying all selected functions in sequence.

        Args:
            file (str): path to the file to be processed
            sample (bool, optional): True to clean a sample (1000 lines) of the file. Defaults to False.
        """
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
        """Clean all files by applying all selected functions in sequence.

        Args:
            sample (bool, optional): True to clean a sample (1000 lines) of the file. Defaults to False.
        """
        self._run(lambda file: self.clean_file(file, sample), self.files)

    def _run(self, fn, my_iter):
        with con.ThreadPoolExecutor(max_workers=self.n_jobs) as executor:
            futures = []
            for item in my_iter:
                futures.append(executor.submit(fn, item))
            for i, _ in enumerate(con.as_completed(futures)):
                print(f'\n{i}/{len(self)} has been cleaned.')

    def __len__(self):
        return len(self.files)
