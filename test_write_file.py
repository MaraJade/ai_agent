import unittest
from functions.write_files import write_file


class TestHTMLNode(unittest.TestCase):
    def test_write_files(self):
        result0 = write_file(
            "calculator",
            "lorem.txt",
            "wait, this isn't lorem ipsum"
        )
        result1 = write_file(
            "calculator",
            "pkg/morelorem.txt",
            "lorem ipsum dolor sit amet"
        )
        result2 = write_file(
            "calculator",
            "/tmp/temp.txt",
            "this should not be allowed"
        )

        print(result0)
        print(result1)
        print(result2)


if __name__ == "__main__":
    unittest.main()
