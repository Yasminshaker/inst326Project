
''' 
December 12, 2024
INST 326: Final Project: Flashcard Application
flashcard.py file
'''

import csv
import requests
from abc import ABC, abstractmethod
import html

class FlashCard(ABC):
    """
    Base class for the flashcard.
    """
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    @abstractmethod
    def display(self):
        """
        Display the flashcard.
        """
        pass

    @abstractmethod
    def check_answer(self, user_answer):
        """
        Check if the user's answer is correct.
        """
        pass

class VocabularyFlashCard(FlashCard):
    """
    Practice for the Vocabulary on the Flashcard.
    """
    def display(self):
        """
        Display the definition as the question.
        """
        print(f"Definition: {self.question}")

    def check_answer(self, user_answer):
        """
        Check if the user's answer is correct.
        """
        return self.answer.strip().lower() == user_answer.strip().lower()

class MathFlashCard(FlashCard):
    """
    Flashcard for math problems.
    """
    def display(self):
        """
        Display the problem statement as the question.
        """
        print(f"Problem: {self.question}")

    def check_answer(self, user_answer):
        """
        Check if the user's answer is correct.
        """
        try:
            return float(user_answer) == eval(self.answer)
        except:
            return False


class ProgressTracker:
    """
    Tracks total and correct attempts.
    """
    def __init__(self):
        """
        Initializes the progress tracker.
        """
        self.total_attempts = 0
        self.correct_attempts = 0

    def record_attempt(self, correct):
        """
        Records the attempt.
        """
        self.total_attempts += 1
        if correct:
            self.correct_attempts += 1

    def display_progress(self):
        """
        Displays the user's progress as a percentage.
        """
        if self.total_attempts == 0:
            print("No progress to display yet.")
        else:
            accuracy = (self.correct_attempts / self.total_attempts) * 100
            print(f"Progress: {self.correct_attempts}/{self.total_attempts} correct ({accuracy:.2f}%)")

def load_flashcards_from_csv(flashcards_csv):
    """
    Load flashcards from a CSV file.
    """
    flashcards = []
    try:
        with open(flashcards_csv, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 3:
                    if row[0] == "Vocabulary":
                        flashcards.append(VocabularyFlashCard(row[1], row[2]))
                    elif row[0] == "Math":
                        flashcards.append(MathFlashCard(row[1], row[2]))
    except FileNotFoundError:
        print(f"File '{flashcards_csv}' not found.")
    return flashcards

def save_flashcards_to_csv(flashcards_csv, flashcards):
    """
    Save flashcards to a CSV file.
    """
    with open(flashcards_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        for card in flashcards:
            card_type = "Vocabulary" if isinstance(card, VocabularyFlashCard) else "Math"
            writer.writerow([card_type, card.question, card.answer])

def import_flashcards_from_api():
    """
    Import flashcards from an external API.
    """
    url = "https://opentdb.com/api.php?amount=5&type=multiple"
    response = requests.get(url)
    flashcards = []
    if response.status_code == 200:
        data = response.json()
        for item in data['results']:
            question = html.unescape(item['question'])
            answer = html.unescape(item['correct_answer'])
            flashcards.append(VocabularyFlashCard(question, answer))
    else:
        print("Failed to fetch data from API.")
    return flashcards


def main():
    """
    Run the flashcard application.
    """
    flashcards = load_flashcards_from_csv('flashcards_example.csv')
    tracker = ProgressTracker()

    print("\nType 'exit' at any prompt to quit the application.")

    while True:
        print("\nFlashcard Application")
        print("1. Add Flashcard")
        print("2. Review Flashcards")
        print("3. Import Flashcards from API")
        print("4. Load Flashcards from a Specific File")
        print("5. View Progress")
        print("6. Exit")
        choice = input("Choose an option: ").strip().lower()

        if choice == "exit":
            print("Goodbye!")
            break

        if choice == "1":
            card_type = input("Enter type (Vocabulary/Math): ").strip().capitalize()
            if card_type.lower() == "exit":
                break
            question = input("Enter question/definition/problem: ").strip()
            if question.lower() == "exit":
                break
            answer = input("Enter answer: ").strip()
            if answer.lower() == "exit":
                break
            if card_type == "Vocabulary":
                flashcards.append(VocabularyFlashCard(question, answer))
            elif card_type == "Math":
                flashcards.append(MathFlashCard(question, answer))
            save_flashcards_to_csv('flashcards_example.csv', flashcards)

        elif choice == "2":
            for card in flashcards:
                card.display()
                user_answer = input("Your answer: ")
                if user_answer.lower() == "exit":
                    break
                correct = card.check_answer(user_answer)
                tracker.record_attempt(correct)
                print("Correct!" if correct else f"Wrong! The answer was: {card.answer}")
            save_flashcards_to_csv('flashcards_example.csv', flashcards)

        elif choice == "3":
            imported_cards = import_flashcards_from_api()
            flashcards.extend(imported_cards)
            save_flashcards_to_csv('flashcards_example.csv', flashcards)
            print(f"Imported {len(imported_cards)} flashcards.")

        elif choice == "4":
            file_name = input("Enter the file name to load flashcards from: ").strip()
            if file_name.lower() == "exit":
                break
            flashcards = load_flashcards_from_csv(file_name)
            if flashcards:
                print(f"Loaded {len(flashcards)} flashcards from '{file_name}'.")
            else:
                print(f"No flashcards loaded. Ensure the file '{file_name}' exists and is correctly formatted.")

        elif choice == "5":
            tracker.display_progress()

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
