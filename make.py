import pylint
import mypy
import pytest
import flake8
import coverage


#todo: finish make.py file

def run_tests():
    pytest.main()


def run_pylint():
    pylint.run_pylint()


if __name__ == '__main__':
    run_tests()
    run_pylint()
