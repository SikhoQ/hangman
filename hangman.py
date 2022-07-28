from random import choice, randint


"""TODO: Add option to create and use user's own word list"""


def print_welcome():
    print("\nWelcome to Hangman. You have 5 chances to guess the missing letters.")


def choose_word_file():
    file = input("\nSelect text file to use [SHORT/LONG/ALL]: ")
    while file.lower() not in ["short", "long", "all"]:
        file = input("\nSelect a valid text file to use [SHORT/LONG/ALL]: ")
    return [words.strip() for words in open(f"C:/Users/School EC/Documents/{file.lower()}_words.txt")]


def choose_random_word(word_list):
    return choice(word_list)


def remove_letters(word):
    if len(word) > 7:
        # remove at least 3 letters for words longer than 7 chars
        num_of_letters_to_remove = randint(3, len(word)-3)
    else:
        # remove at least half of letters for shorter words
        num_of_letters_to_remove = randint(len(word)//2, len(word)-1)
    # num_of_letters_to_remove = randint(len(word)//2, len(word)-2)
    for i in range(num_of_letters_to_remove):
        index = randint(0, len(word)-1)
        while not word[index].isalpha():
            index = randint(0, len(word)-1)
        word = word.replace(word[index], '_')
        if len(word) - word.count('_') == 2:
            break
    return word


def take_a_guess(guess, prev_guesses):
    print(f"\nThe word to guess is {guess}.\n", end=' ')
    letter_or_word = input("\nGuess whole word? (y/n): ")
    while len(letter_or_word) != 1 or letter_or_word.lower() not in "yn":
        letter_or_word = input("\nGuess whole word? (y/n): ")
    letter_only = (letter_or_word.lower() == 'n')
    while True:
        if letter_only:
            letter = input(f"\nGuess a single letter from {guess}: ")
            while not letter.lower().isalpha() or len(letter) != 1:
                letter = input(f"\nGuess a single letter from {guess}: ")
        else:
            letter = input(f"\nGuess the whole word {guess}: ")
            while len(letter) != len(guess):
                letter = input(f"\nGuess the whole word {guess}: ")
        if letter in guess:
            print("That's already there!\n")
            continue
        elif letter in prev_guesses:
            print("You have already made that guess!\n")
            continue
        break
    prev_guesses.append(letter.lower())
    return letter.lower(), prev_guesses


def wrong_guess(letter, word, guess):
    if letter==word or (letter in word and letter not in guess):
        return False
    return True


def update_word(letter, word, guess):
    index_list = [index for index in range(len(word)) if letter == word[index]]
    for i in range(len(index_list)):
        guess = guess[:index_list[i]] + word[index_list[i]] + guess[index_list[i]+1:]
    return guess


def draw_figure(guesses):
    print("   _________")
    print("  | /  (- -)" if guesses != 5 else "  | /  (x x)")
    if guesses == 1:
        print("  |/")
        print("  |")
        print("  |")
        print("  |")
    elif guesses == 2:
        print("  |/     |")
        print("  |")
        print("  |")
        print("  |")
    elif guesses == 3:
        print("  |/     |")
        print("  |     / \\")
        print("  |")
        print("  |")
    elif guesses == 4:
        print("  |/     |")
        print("  |     /|\\")
        print("  |      |")
        print("  |")
    else:
        print("  |/     |")
        print("  |     /|\\")
        print("  |      |")
        print("  |     / \\")
    print("_______")
    print(f"{5-guesses} guess left.\n" if guesses == 4 else f"{5-guesses} guesses left.\n")


def run_game():
    print_welcome()
    word_list = choose_word_file()
    word = choose_random_word(word_list)
    guess = remove_letters(word)
    guesses = 0
    prev_guesses = []
    while guesses != 5:
        letter, prev_guesses = take_a_guess(guess, prev_guesses) # allow to guess a single letter or the whole word
        if wrong_guess(letter, word, guess):
            guesses += 1
            draw_figure(guesses)
            if guesses == 5:
                print(f"\nYou lose! The word was {word}")
                break
        else:
            if len(letter)==1:
                guess = update_word(letter, word, guess)
            if guess == word or letter == word:
                print(f"\n{'*'*8}You win!{'*'*8}\nThe word was {word}")
                break
            else:
                print(f"\nNice! Keep at it! {5-guesses} guesses left.")

if __name__ == "__main__":
    run_game()