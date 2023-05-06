# Builtin
import unittest


def main():
    # Discover tests in the 'tests' folder
    test_suite = unittest.TestLoader().discover("tests")

    # Run the tests
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)


if __name__ == "__main__":
    main()
