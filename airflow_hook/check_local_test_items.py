import re
from pathlib import Path

from loguru import logger


def main():
    my_dir = Path.home() / 'projects' / 'Airflow' / 'dags' / 'AdobeAnalytics'
    for i in my_dir.glob('*.py'):
        with i.open() as f:
            contents_ = f.read()
        if re.search(r'\btest\b|.*_test.*|.*test_.*', contents_, re.IGNORECASE):
            logger.info('Test in : {}'.format(i.resolve()))
        email_address = 'cupjohn@condati.com'
        if re.search(r'{}'.format(email_address), contents_, re.IGNORECASE):
            logger.info('Bad Email address {}  : {}'.format(email_address, i.resolve()))


if __name__ == '__main__':
    main()
