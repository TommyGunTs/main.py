"""
*******************************************
CS 1026A - Assignment 3 - YouTube Emotions
Code by: Thomas Tyndorf
Student ID: ttyndor3
File created: November 8th, 2024
*******************************************
This program processes YouTube comments to analyze emotions using
keyword matching and generates statistical reports on emotional content.
"""

import os.path
from emotions import *

# List of valid countries for filtering comments
VALID_COUNTRIES = ['bangladesh', 'brazil', 'canada', 'china', 'egypt', 'france',
                   'germany', 'india', 'iran', 'japan', 'mexico', 'nigeria',
                   'pakistan', 'russia', 'south korea', 'turkey', 'united kingdom',
                   'united states']


def ask_user_for_input():
    """
    Prompts user for input files and validation parameters.
    Returns: tuple containing (keyword_filename, comment_filename, country_filter, report_filename)
    Raises: ValueError for invalid file extensions or countries
            IOError for non-existent files or existing report files
    """
    # Validate keyword file extension and existence
    keyword_filename = input("Input keyword file (ending in .tsv): ")
    if not keyword_filename.endswith('.tsv'):
        raise ValueError("Keyword file does not end in .tsv!")
    if not os.path.exists(keyword_filename):
        raise IOError(f"{keyword_filename} does not exist!")

    # Validate comments file extension and existence
    comment_filename = input("Input comment file (ending in .csv): ")
    if not comment_filename.endswith('.csv'):
        raise ValueError("Comments file does not end in .csv!")
    if not os.path.exists(comment_filename):
        raise IOError(f"{comment_filename} does not exist!")

    # Validate country selection
    country_filter = input("Input a country to analyze (or \"all\" for all countries): ").lower()
    if country_filter != "all" and country_filter not in VALID_COUNTRIES:
        raise ValueError(f"{country_filter} is not a valid country to filter by!")

    # Validate report file extension and non-existence
    report_filename = input("Input the name of the report file (ending in .txt): ")
    if not report_filename.endswith('.txt'):
        raise ValueError("Report file does not end in .txt!")
    if os.path.exists(report_filename):
        raise IOError(f"{report_filename} already exists!")

    return (keyword_filename, comment_filename, country_filter, report_filename)


def main():
    """
    Main program loop that handles user input, data processing, and report generation.
    Continues to ask for input if validation errors occur.
    """
    while True:
        try:
            # Get and validate all user inputs
            keyword_filename, comment_filename, country_filter, report_filename = ask_user_for_input()

            # Create emotion keyword dictionary from TSV file
            emotion_keywords = make_keyword_dict(keyword_filename)

            # Get filtered list of comments based on country selection
            filtered_comments = make_comments_list(country_filter, comment_filename)

            # Generate emotion analysis report and get most common emotion
            dominant_emotion = make_report(filtered_comments, emotion_keywords, report_filename)

            # Display the final result
            print(f"Most common emotion is: {dominant_emotion}")
            break

        except (ValueError, IOError) as error:
            # Handle validation and file errors
            print(f"Error: {str(error)}")
        except RuntimeError as error:
            # Handle runtime errors (e.g., no comments in dataset)
            print(f"Error: {str(error)}")
            break


if __name__ == "__main__":
    main()