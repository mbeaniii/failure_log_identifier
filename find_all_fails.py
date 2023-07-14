import os
import sys
import shutil
from typing import Optional, Tuple
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class FailFileFinder:
    CHROMEDRIVER_PATH = "C:/Users/MarcusBean/Downloads/chromedriver_win32/chromedriver.exe"
    MATCH_PATTERNS = ["AssertionError", '"was_successful": false', 'Exception: FAILED', 'The execution of this command did not finish successfully']

    def __init__(self, directory: str):
        self.directory = directory
        self.fail_dir = os.path.join(self.directory, "fails")
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")

        # Disable logging to suppress Selenium output
        self.chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-logging"]
        )

        self.service = Service(executable_path=FailFileFinder.CHROMEDRIVER_PATH)
        self.driver = webdriver.Chrome(
            service=self.service, options=self.chrome_options
        )

    def __del__(self):
        self.driver.quit()

    def check_file_for_pattern(self, file_path: str) -> Tuple[bool, Optional[int]]:
        self.driver.get(f"file://{file_path}")

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*"))
        )

        content = self.driver.page_source

        if any(
            match_pattern in content for match_pattern in FailFileFinder.MATCH_PATTERNS
        ):
            return True, os.path.getsize(file_path)

        return False, None

    def handle_fail_directory(self, filename: str) -> str:
        os.makedirs(self.fail_dir, exist_ok=True)
        dest_file = os.path.join(self.fail_dir, filename)
        return dest_file

    def process_file(self, file_path: str, dest_file: str, file_size: int) -> bool:
        if os.path.exists(dest_file):
            print(f"{file_path} already exists in {self.fail_dir}")
            return False

        if file_size <= 5 * 1024 * 1024:
            shutil.copy(file_path, dest_file)
            return True
        else:
            print(
                f"{file_path} not included in 'fails' directory because it's larger than 5 MB."
            )
            return False

    def find_fail_files(self) -> None:
        file_found = False
        for root, _, files in os.walk(self.directory):
            if self.fail_dir in root:  # Skip the 'fails' directory
                continue

            for filename in files:
                file_path = os.path.join(root, filename)
                match, file_size = self.check_file_for_pattern(file_path)
                if match:
                    dest_file = self.handle_fail_directory(filename)
                    copied = self.process_file(file_path, dest_file, file_size)
                    if copied:
                        print(file_path)
                        file_found = True

        if not file_found:
            print("No new files containing the specified patterns were found.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python find_fail_files.py [directory]")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"{directory} is not a valid directory.")
        sys.exit(1)

    finder = FailFileFinder(directory)
    finder.find_fail_files()
