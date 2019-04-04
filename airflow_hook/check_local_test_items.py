import re
import subprocess
from pathlib import Path

from loguru import logger


def main():
    root_dir = subprocess.Popen('git rev-parse --show-toplevel'.split(), stdout=subprocess.PIPE).communicate()
    path_root = Path(root_dir[0].decode().replace('\n', ''))

    file_names = subprocess.Popen('git diff development --name-only'.split(), stdout=subprocess.PIPE).communicate()
    for i in [i for i in file_names[0].decode().splitlines() if i.endswith('py') and i.startswith('dag')]:
        file_path = path_root / i

        with file_path.open() as f:
            contents_ = f.read()
        if re.search(r'\btest\b|.*_test.*|.*test_.*', contents_, re.IGNORECASE):
            logger.info('Test in : {}'.format(file_path.resolve()))
        email_address = 'cupjohn@condati.com'
        if re.search(r'{}'.format(email_address), contents_, re.IGNORECASE):
            logger.info('Bad Email address {}  : {}'.format(email_address, file_path.resolve()))

    test_dir = path_root / 'tests'
    for i in test_dir.glob('**/*.py'):
        with i.open() as f:
            contents_ = f.read()
        content_by_line = contents_.splitlines()
        for line_number, line in enumerate(content_by_line):
            if re.search(r'\bwith.*\.connect.*', line, re.IGNORECASE):
                if not re.search(r'\bassert.*', content_by_line[line_number + 1]):
                    logger.info('missing assert statement after with connect: line number {}, {}, {}'.format(line_number, line, i))


if __name__ == '__main__':
    main()
