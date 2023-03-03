""" This module contains functions for running tests and coverage, and for running flake8 static code analyzer. """
import subprocess
import sys

from logs.logger import logger
from config.config_parser import config


def run_tests_and_coverage():
    """
    Runs tests and checks coverage.
    :return: None
    """
    coverage_repo_folder = f"{config()['MAKE']['reports_path']}{config()['MAKE']['coverage_report_folder']}"
    logger.info("Running tests and checking coverage...")
    subprocess.run("coverage run -m pytest")
    subprocess.run(f"coverage report -m > {coverage_repo_folder}")
    logger.info("Generating coverage report and saving to reports folder...")
    subprocess.run(f"coverage html -d {coverage_repo_folder}")


def run_static_code_analyzer():
    """
    Runs flake8 static code analyzer and writes the report to a file.
    :return: None
    """
    logger.info("Running flake8 static code analyzer...")
    report_path = f'{config()["MAKE"]["reports_path"]}{config()["MAKE"]["flake8_report_name"]}'
    try:
        with open(report_path, "w") as file:
            file.write(subprocess.run("flake8 --exclude env", capture_output=True).stdout.decode())
    except FileNotFoundError:
        logger.exception("File not found.")
        sys.exit(1)


if __name__ == '__main__':
    run_tests_and_coverage()
    run_static_code_analyzer()


