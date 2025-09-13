import re
from fuzzywuzzy import fuzz

reversal_pairs = [('b', 'd'), ('p', 'q'), ('m', 'w'), ('n', 'u')]

common_misspellings = {
    'because': ['becuase', 'becasue'],
    'friend': ['freind'],
    'said': ['saied', 'seid'],
    'the': ['teh'],
    'was': ['wsa'],
}

def detect_reversals(text):
    issues = []
    words = text.lower().split()
    for word in words:
        for a, b in reversal_pairs:
            # Check if word contains reversed letters in sequence
            if a+b in word or b+a in word:
                issues.append(f"Possible letter reversal in word '{word}'")
    return issues

def detect_misspellings(text):
    issues = []
    words = text.lower().split()
    for word in words:
        for correct, misspellings in common_misspellings.items():
            for misspelling in misspellings:
                if fuzz.ratio(word, misspelling) > 80:
                    issues.append(f"Possible misspelling: '{word}' instead of '{correct}'")
    return issues

def analyze_text(text):
    issues = []
    issues.extend(detect_reversals(text))
    issues.extend(detect_misspellings(text))
    if not issues:
        return "No obvious dyslexia-related issues detected."
    return "\n".join(issues)

if __name__ == "__main__":
    print("Enter sentences for dyslexia analysis (type 'exit' to quit):")
    while True:
        user_input = input("> ")
        if user_input.lower() == 'exit':
            break
        result = analyze_text(user_input)
        print(result)
