import re
from pathlib import Path

from loguru import logger

dir_ = 'AdobeAnalytics'


def main():
    my_dir = Path.home() / 'projects' / 'Airflow' / 'dags' / dir_
    for i in my_dir.glob('*.py'):
        with i.open() as f:
            contents_ = f.read()
        if re.search(r'\btest\b|.*_test.*|.*test_.*', contents_, re.IGNORECASE):
            logger.info('Test in : {}'.format(i.resolve()))
        email_address = 'cupjohn@condati.com'
        if re.search(r'{}'.format(email_address), contents_, re.IGNORECASE):
            logger.info('Bad Email address {}  : {}'.format(email_address, i.resolve()))

    # todo: do recursive check
    # todo: add test
    test_dir = Path.home() / 'projects' / 'Airflow' / 'tests' / 'tests_ad_roll'
    for i in test_dir.glob('*.py'):
        with i.open() as f:
            contents_ = f.read()
        content_by_line = contents_.splitlines()
        for line_number, line in enumerate(content_by_line):
            if re.search(r'\bwith.*\.connect.*', line, re.IGNORECASE):
                if not re.search(r'\bassert.*', content_by_line[line_number + 1]):
                    logger.info('missing assert statement after with connect: line number {}, {}, {}'.format(line_number, line, i))


if __name__ == '__main__':
    main()
