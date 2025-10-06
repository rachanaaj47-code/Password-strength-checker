# Password Strength Checker
# File: password_strength_checker.py
# Description: A simple but comprehensive password strength evaluation tool.
# This script analyzes passwords based on length, character diversity, and common patterns.

import re
import string

def check_password_strength(password):
    """Evaluate password strength and return a feedback dictionary."""
    feedback = {
        'length_score': 0,
        'complexity_score': 0,
        'uniqueness_score': 0,
        'total_score': 0,
        'strength': '',
        'recommendations': []
    }

    # 1. Length Analysis
    length = len(password)
    if length < 6:
        feedback['length_score'] = 1
        feedback['recommendations'].append('Use at least 8 characters.')
    elif 6 <= length < 10:
        feedback['length_score'] = 2
    elif 10 <= length < 14:
        feedback['length_score'] = 3
    else:
        feedback['length_score'] = 4

    # 2. Complexity Analysis
    complexity = 0
    if re.search(r'[a-z]', password):
        complexity += 1
    if re.search(r'[A-Z]', password):
        complexity += 1
    if re.search(r'\d', password):
        complexity += 1
    if re.search(rf'[{re.escape(string.punctuation)}]', password):
        complexity += 1

    feedback['complexity_score'] = complexity

    if complexity < 3:
        feedback['recommendations'].append('Include uppercase, lowercase, numbers, and symbols for stronger protection.')

    # 3. Uniqueness Analysis (simple pattern detection)
    common_patterns = [
        'password', '1234', 'qwerty', 'admin', 'letmein', 'welcome', 'iloveyou'
    ]
    uniqueness_score = 4
    for pattern in common_patterns:
        if pattern in password.lower():
            uniqueness_score = 1
            feedback['recommendations'].append('Avoid common or easily guessable patterns.')
            break

    feedback['uniqueness_score'] = uniqueness_score

    # 4. Combine Scores
    total = feedback['length_score'] + feedback['complexity_score'] + feedback['uniqueness_score']
    feedback['total_score'] = total

    # 5. Determine Strength Level
    if total <= 4:
        feedback['strength'] = 'Weak'
    elif 5 <= total <= 7:
        feedback['strength'] = 'Moderate'
    elif 8 <= total <= 10:
        feedback['strength'] = 'Strong'
    else:
        feedback['strength'] = 'Very Strong'

    return feedback


def print_feedback(feedback, password):
    print(f"\nPassword: {password}")
    print(f"Strength: {feedback['strength']}")
    print(f"Total Score: {feedback['total_score']}/12")
    print(f"\nDetails:")
    print(f"  Length Score: {feedback['length_score']}/4")
    print(f"  Complexity Score: {feedback['complexity_score']}/4")
    print(f"  Uniqueness Score: {feedback['uniqueness_score']}/4")
    if feedback['recommendations']:
        print(f"\nRecommendations:")
        for rec in feedback['recommendations']:
            print(f"  - {rec}")


def main():
    print("Password Strength Checker")
    print("--------------------------")
    password = input("Enter a password to test: ")
    result = check_password_strength(password)
    print_feedback(result, password)


if __name__ == '__main__':
    main()
