# Find All Fails
This Python script searches for files containing a specified pattern ("AssertionError") within a given directory and its subdirectories. Matching files are then copied into a "fails" folder, unless they are larger than 5 MB.

## Dependencies
To install the required dependencies, please use the requirements.txt file provided in this repository. To do this, open your terminal or command prompt, navigate to the project directory, and run the following command:

    pip install -r requirements.txt

## Chromedriver Setup

This script uses Selenium with Chromedriver to process the files. To set up Chromedriver, follow these steps:

1. Check your Google Chrome version: Open Google Chrome, click the three vertical dots in the top-right corner > Help > About Google Chrome. Note down your Chrome version.
2. Download the appropriate Chromedriver for your machine and Chrome version from the Chromedriver downloads page.
3. Extract the downloaded archive and place the chromedriver executable in a suitable location.
4. Update the CHROMEDRIVER_PATH variable in the find_all_fails.py script to the absolute path of the chromedriver executable on your machine.

Example:
    CHROMEDRIVER_PATH = "/path/to/your/chromedriver"

# Basic Usage
To use the script, navigate to the project directory using your terminal or command prompt and run the following command:

    python find_all_fails.py [directory]

Replace [directory] with the path to the directory you want to search for files containing the specified pattern.

Example:
    python find_all_fails.py C:\Users\Username\Downloads\test_files

The script will search the specified directory and its subdirectories for files containing the specified pattern. Matching files will be copied to a "fails" folder within the given directory unless they are larger than 5 MB.

