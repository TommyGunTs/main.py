"""
*******************************************
CS 1026A - Assignment 3 - YouTube Emotions
Code by: Thomas Tyndorf
Student ID: ttyndor3
File created: November 8th, 2024
*******************************************
Core functionality for analyzing emotions in YouTube comments
using keyword matching and generating statistical reports.
"""

# List of emotions we're analyzing
EMOTIONS = ['anger', 'joy', 'fear', 'trust', 'sadness', 'anticipation']


def clean_text(comment):
    """
    Cleans comment text by removing non-letter characters and converting to lowercase.
    Args:
        comment (str): Raw comment text
    Returns:
        str: Cleaned comment text
    """
    cleaned_comment = ''
    for char in comment.lower():
        if char.isalpha():
            cleaned_comment += char
        else:
            cleaned_comment += ' '
    return cleaned_comment


def make_keyword_dict(keyword_file_name):
    """
    Creates dictionary of emotion keywords from TSV file.
    Args:
        keyword_file_name (str): Name of TSV file containing emotion keywords
    Returns:
        dict: Nested dictionary mapping words to emotion scores
    """
    emotion_dict = {}
    with open(keyword_file_name, 'r') as file:
        for line in file:
            # Split line into word and emotion scores
            parts = line.strip().split('\t')
            word = parts[0]
            scores = [int(score) for score in parts[1:]]

            # Create emotion score dictionary for this word
            emotion_scores = {}
            for emotion, score in zip(EMOTIONS, scores):
                emotion_scores[emotion] = score
            emotion_dict[word] = emotion_scores

    return emotion_dict


def make_comments_list(filter_country, comments_file_name):
    """
    Creates list of comments filtered by country.
    Args:
        filter_country (str): Country to filter by or 'all'
        comments_file_name (str): Name of CSV file containing comments
    Returns:
        list: List of comment dictionaries
    """
    comment_list = []
    with open(comments_file_name, 'r') as file:
        for line in file:
            # Parse comment data
            comment_id, username, country, text = line.strip().split(',', 3)

            # Filter by country (case insensitive)
            if filter_country == 'all' or country.lower() == filter_country.lower():
                comment_dict = {
                    'comment_id': int(comment_id),
                    'username': username,
                    'country': country,
                    'text': text
                }
                comment_list.append(comment_dict)

    return comment_list


def classify_comment_emotion(comment, keywords):
    """
    Determines primary emotion in a comment using keyword matching.
    Args:
        comment (str): Comment text to analyze
        keywords (dict): Emotion keyword dictionary
    Returns:
        str: Most prevalent emotion
    """
    # Initialize emotion counters
    emotion_counts = {emotion: 0 for emotion in EMOTIONS}

    # Clean and split comment into words
    clean_words = clean_text(comment).split()

    # Count emotion matches
    for word in clean_words:
        if word in keywords:
            word_emotions = keywords[word]
            for emotion in EMOTIONS:
                emotion_counts[emotion] += word_emotions[emotion]

    # Find highest scoring emotion (using priority order for ties)
    max_score = max(emotion_counts.values())
    for emotion in EMOTIONS:  # Priority order is maintained by EMOTIONS list order
        if emotion_counts[emotion] == max_score:
            return emotion


def make_report(comment_list, keywords, report_filename):
    """
    Generates emotion analysis report and returns most common emotion.
    Args:
        comment_list (list): List of comments to analyze
        keywords (dict): Emotion keyword dictionary
        report_filename (str): Name of output report file
    Returns:
        str: Most common emotion
    Raises:
        RuntimeError: If comment_list is empty
    """
    if not comment_list:
        raise RuntimeError("No comments in dataset!")

    # Count emotions in comments
    emotion_totals = {emotion: 0 for emotion in EMOTIONS}
    for comment in comment_list:
        dominant_emotion = classify_comment_emotion(comment['text'], keywords)
        emotion_totals[dominant_emotion] += 1

    # Calculate total comments and percentages
    total_comments = sum(emotion_totals.values())

    # Find most common emotion (using priority order for ties)
    max_count = max(emotion_totals.values())
    for emotion in EMOTIONS:
        if emotion_totals[emotion] == max_count:
            most_common = emotion
            break

    # Generate report
    with open(report_filename, 'w') as file:
        file.write(f"Most common emotion: {most_common}\n")
        file.write("Emotion Totals\n")
        for emotion in EMOTIONS:
            count = emotion_totals[emotion]
            percentage = (count / total_comments) * 100
            file.write(f"{emotion}: {count} ({percentage:.2f}%)\n")

    return most_common