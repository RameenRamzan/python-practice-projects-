import json
import random

with open("words.json" , "r") as file:
    data = json.load(file)
    words_list = data["words"]

def get_word():
    word = random.choice(words_list)
    return word.upper()

def play_hangman(word):
    word = word.upper()
    word_completion = '_' * len(word)
    guessed = False
    guessed_letters = []
    guessed_word = []
    tries = 6

    print("---@@@==== WELCOME TO HANGMAN ====@@@---\n")
    print("RULES: \n. You have to guess letters or word.\n2. You will have 6 tries.")
    print("Let's begin !!!")
    print(display_hangman(tries))
    print(word_completion)
    print("\n")

    while not guessed and tries > 0:
        guess = input("Please enter a guess word or letter: ").strip().upper()

        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("You have already guessed this letter" , guess)
            elif guess not in word:
                print(guess, "is not the letter :(")
                print("Please try again!!")
                tries -= 1
                guessed_letters.append(guess)
            else:
                print("Good Job!! You have guessed the correct word.")
                guessed_letters.append(guess)
                word_as_list = list(word_completion)
                indices = [i for i , letter in enumerate(word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                word_completion = "".join(word_as_list)

                if "_"  not in word_completion:
                    guessed = True
                    
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_word:
                print("You already guessed the word", guess)
            elif guess not in guessed_word:
                print(guess, "is not the word!!")
                tries -= 1
                guessed_word.append(guess)
            else:
                guessed = True
                word_completion = word
        else:
            print("Not a valid guess !!")
        print(display_hangman(tries))
        print(word_completion)
        print("\n")
    
    if guessed:
        print("Congrats, you guessed the word !!")
        print("You win !!!!!!")
    else:
        print("Sorry, ran out of tries. The word was" ,word, ".Better luck next time !!")

def display_hangman(tries):
    stages = [  # final state: head, torso, both arms, and both legs
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """,
                # head, torso, both arms, and one leg
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                """,
                # head, torso, and both arms
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                """,
                # head, torso, and one arm
                """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                """,
                # head and torso
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                """,
                # head
                """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """,
                # initial empty state
                """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """
    ]
    return stages[tries]
  

def main():
    word = get_word()
    play_hangman(word)

    while input("Do you want to play again ? (Y / N)").upper() == 'Y':
        word = get_word()
        play_hangman(word)

if __name__ == "__main__":
    main()



