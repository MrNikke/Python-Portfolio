import string            # Imports the string module
import random            # Imports the random module
import logging           # Imports the logging module

def respond(text):
    text = text.lower()
    # Split the user's sentence into a list of words
    original_words = str.split(text)
    # Create a new list that contains the same words (a copy)
    new_words = original_words[:]
    # Go through all words, one at a time. If the word is in the first person, replace it with
    # the corresponding word in the second person
    for i in range(len(original_words)):
        if original_words[i] == 'i':
            new_words[i] = 'you'
        elif original_words[i] == 'my':
            new_words[i] = 'your'
        elif original_words[i] == 'your':
            new_words[i] = 'my'
        elif original_words[i] == 'mine':
            new_words[i] = 'yours'
        elif original_words[i] == 'me':
            new_words[i] = 'you'
        elif original_words[i] == 'myself':
            new_words[i] = 'yourself'

    if "no" in original_words or 'never' in original_words or 'not' in original_words or 'none' in original_words or 'unfortunately' in original_words:
        # Random negative responses
        negative_responses = ['Not that?', 'Are you sure?', 'Is that true?', 'Why not?', 'Why are you in such a bad mood?', 'Why do you say that?']
        response = random.choice(negative_responses)

    elif "mom" in original_words or 'dad' in original_words or 'brother' in original_words or 'sister' in original_words or 'family' in original_words or 'relatives' in original_words:
        # Family-related responses, randomly chosen
        family_responses = ['Are your siblings the same?', 'Is your sister the same?', 'What does dad think about that?', 'What does mom say about that?', 'Is your brother the same?', 'Tell me more about your family.']
        response = random.choice(family_responses)

    elif new_words == original_words:
        # Random positive expressions, respond "smartly" by randomly choosing an expression from the list
        positive_responses = ['That sounds interesting.', 'Keep talking.', 'I understand what you mean.', 'That’s right.', 'Tell me more.']
        response = random.choice(positive_responses)
    else:
        # Replace the last word in the response if it's followed by punctuation
        last_word = new_words[-1]
        if last_word[-1] in string.punctuation:  # string.punctuation contains all possible punctuation marks
            last_word = last_word[:-1]
        new_words[-1] = last_word + "?"
        response = " ".join(new_words)

    print(response)
    logging.info(response)  # Writes the response to a log file

def main():
    print("**************************************************")
    print()
    print(" Welcome to Eliza's consultation ")
    print()
    print("**************************************************")
    print()
    print('(You can exit at any time by saying "goodbye")')
    print()
    print('Tell me about your problems...')

    # Continue the conversation indefinitely
    while True:
        # Wait for the user to input something
        text = input("\n> ")
        if text in ["goodbye", "Stop!", "OK, that does it!", "Thanks and good night"]:  # If the user types any of these options, the program exits
            break

        logging.info(text)  # Writes the user's input to the log file.
        respond(text)

    print('Thank you for your visit. Please transfer 150 EUR to my account.')  # Final message

main()
