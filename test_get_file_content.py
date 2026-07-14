import unittest
from functions.get_file_content import get_file_content


class TestHTMLNode(unittest.TestCase):
    def test_get_file_content(self):
        result = get_file_content("calculator", "lorem.txt")
        print(f"lorem.txt length: {len(result)}")
        print(f"lorem.txt truncated: {'truncated' in result}")
        print(f"{get_file_content('calculator', 'main.py')}")
        print(f"{get_file_content('calculator', 'pkg/calculator.py')}")
        print(f"{get_file_content('calculator', '/bin/cat')}")
        print(f"{get_file_content('calculator', 'pkg/does_not_exist.py')}")


if __name__ == "__main__":
    unittest.main()
