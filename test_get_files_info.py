import unittest
from functions.get_files_info import get_files_info


class TestHTMLNode(unittest.TestCase):
    def test_get_files_info(self):
        print(
                "Result for current directory: \n" +
                get_files_info("calculator", ".")
        )
        print(
                "Results for 'pkg' directory: \n" +
                f'\t{get_files_info("calculator", "pkg")}'
        )
        print(
                "Results for '/bin' directory: \n" +
                f'\t{get_files_info("calculator", "/bin")}'
        )
        print(
                "Results for '../' directory: \n" +
                f'\t{get_files_info("calculator", "../")}'
        )


if __name__ == "__main__":
    unittest.main()
