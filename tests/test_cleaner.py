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
