from xinaprocessor.cleaner import *
from test_const import *
import pytest

@pytest.mark.parametrize("inp_text, target_text", [
    (text_test_example_1, example_1_remove_english_text), 
    (text_test_example_2, example_2_remove_english_text), 
    (text_test_example_3, example_3_remove_english_text), 
    (text_test_example_4, example_4_remove_english_text)
])
def test_remove_english_text(inp_text, target_text):
    cleaner = TextCleaner(inp_text)
    assert cleaner.remove_english_text().text.strip() == target_text.strip()


@pytest.mark.parametrize("inp_text, target_text", [
    (text_test_example_1, example_1_remove_arabic_text), 
    (text_test_example_2, example_2_remove_arabic_text), 
    (text_test_example_3, example_3_remove_arabic_text), 
    (text_test_example_4, example_4_remove_arabic_text)
])
def test_remove_arabic_text(inp_text, target_text):
    cleaner = TextCleaner(inp_text)
    assert cleaner.remove_arabic_text().text.strip() == target_text.strip()


@pytest.mark.parametrize("inp_text, target_text", [
    (text_test_example_1, example_1_remove_arabic_text), 
    (text_test_example_2, example_2_remove_arabic_text), 
    (text_test_example_3, example_3_remove_arabic_text), 
    (text_test_example_4, example_4_remove_arabic_text)
])
def test_remove_numbers(inp_text, target_text):
    cleaner = TextCleaner(inp_text)
    assert cleaner.remove_arabic_text().text.strip() == target_text.strip()


@pytest.mark.parametrize("inp_text, target_text", [
    (text_test_example_1, example_1_remove_numbers), 
    (text_test_example_2, example_2_remove_numbers), 
    (text_test_example_3, example_3_remove_numbers), 
    (text_test_example_4, example_4_remove_numbers)
])
def test_remove_numbers(inp_text, target_text):
    cleaner = TextCleaner(inp_text)
    assert cleaner.remove_numbers().text.strip() == target_text.strip()


@pytest.mark.parametrize("inp_text, target_text", [
    (text_test_example_1, example_1_remove_arabic_numbers), 
    (text_test_example_2, example_2_remove_arabic_numbers), 
    (text_test_example_3, example_3_remove_arabic_numbers), 
    (text_test_example_4, example_4_remove_arabic_numbers)
])
def test_remove_arabic_numbers(inp_text, target_text):
    cleaner = TextCleaner(inp_text)
    assert cleaner.remove_arabic_numbers().text.strip() == target_text.strip()


@pytest.mark.parametrize("inp_text, target_text", [
    (text_test_example_1, example_1_remove_english_numbers), 
    (text_test_example_2, example_2_remove_english_numbers), 
    (text_test_example_3, example_3_remove_english_numbers), 
    (text_test_example_4, example_4_remove_english_numbers)
])
def test_remove_english_numbers(inp_text, target_text):
    cleaner = TextCleaner(inp_text)
    assert cleaner.remove_english_numbers().text.strip() == target_text.strip()


@pytest.mark.parametrize("inp_text, target_text", [
    (text_test_example_1, example_1_remove_arabic_punctuation), 
    (text_test_example_2, example_2_remove_arabic_punctuation), 
    (text_test_example_3, example_3_remove_arabic_punctuation), 
    (text_test_example_4, example_4_remove_arabic_punctuation)
])
def test_remove_arabic_punctuation(inp_text, target_text):
    cleaner = TextCleaner(inp_text)
    assert cleaner.remove_arabic_punctuation().text.strip() == target_text.strip()

@pytest.mark.parametrize("inp_text, target_text", [
    (text_test_example_1, example_1_remove_english_punctuation), 
    (text_test_example_2, example_2_remove_english_punctuation), 
    (text_test_example_3, example_3_remove_english_punctuation), 
    (text_test_example_4, example_4_remove_english_punctuation)
])
def test_remove_english_punctuation(inp_text, target_text):
    cleaner = TextCleaner(inp_text)
    assert cleaner.remove_english_punctuation().text.strip() == target_text.strip()


@pytest.mark.parametrize("inp_text, target_text", [
    (text_test_example_1, example_1_remove_punctuation), 
    (text_test_example_2, example_2_remove_punctuation), 
    (text_test_example_3, example_3_remove_punctuation), 
    (text_test_example_4, example_4_remove_punctuation)
])
def test_remove_punctuation(inp_text, target_text):
    cleaner = TextCleaner(inp_text)
    assert cleaner.remove_punctuation().text.strip() == target_text.strip()