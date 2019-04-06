import re
import subprocess
from pathlib import Path
from typing import List


def root_and_diff_files():
    root_dir = subprocess.Popen('git rev-parse --show-toplevel'.split(), stdout=subprocess.PIPE).communicate()
    path_root = Path(root_dir[0].decode().replace('\n', ''))

    file_names_result = subprocess.Popen('git diff development --name-only'.split(), stdout=subprocess.PIPE).communicate()
    file_names = file_names_result[0].decode().splitlines()

    return path_root, file_names


def check_assert_in_file(file_path: Path):
    with file_path.open() as f:
        contents_ = f.read()
    content_by_line = contents_.splitlines()

    file_results = list()
    for line_number, line in enumerate(content_by_line):
        if re.search(r'\bwith.*\.connect.*', line, re.IGNORECASE):
            if not re.search(r'\bassert.*', content_by_line[line_number + 1]):
                file_results.append({'line': line, 'line_number': line_number})
    return None if len(file_results) == 0 else {str(file_path): file_results}


def check_test_files(root_dir: Path):
    all_good = True
    test_dir = root_dir / 'tests'
    results = map(check_assert_in_file, test_dir.glob('**/*.py'))
    test_files = list(filter(lambda x: x is not None, results))
    for file in test_files:
        for file_name, lines in file.items():
            print('Missing assert statements:')
            print(file_name)
            print('lines: ', [i['line_number'] for i in lines])
            if file_name:
                all_good = False

    return all_good


def check_dag_files(root_dir: Path, files: List):
    all_good = True
    for i in [i for i in files if i.endswith('py') and i.startswith('dag')]:
        file_path = root_dir / i

        with file_path.open() as f:
            contents_ = f.read()
        if re.search(r'\btest\b|.*_test.*|.*test_.*', contents_, re.IGNORECASE):
            all_good = False
            print('Test in : {}'.format(file_path.resolve()))
        email_address = 'cupjohn@condati.com'
        if re.search(r'{}'.format(email_address), contents_, re.IGNORECASE):
            all_good = False
            print('Bad Email address {}  : {}'.format(email_address, file_path.resolve()))

    return all_good


def main():
    path_root, file_names = root_and_diff_files()

    dag_check = check_dag_files(path_root, file_names)
    tests_check = check_test_files(path_root)

    return 0 if all([dag_check, tests_check]) else 1


if __name__ == '__main__':
    main()
