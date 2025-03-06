#Qian Yi Wang 40211303 - putyournameandidhere
import spacy
from spacy.matcher import PhraseMatcher, Matcher

#### INITIALIZATION ####
# Load the model 
nlp = spacy.load("en_core_web_sm")

# Initialize matchers 
matcher = Matcher(nlp.vocab)
phraseMatcher = PhraseMatcher(nlp.vocab, attr="LOWER")

# Dictionary of responses for the chatbot
response_dict = {
    # general responses
    "greet": "Hello! How can I help you today?",
    "bye": "Goodbye! Have a great day!",
    "help": "I can answer your questions. Try asking about something more specific!",
    "default": "I'm sorry, I didn't understand that. Could you rephrase?",
    # Java keyword/statement responses
    "for": "A for loop is a control flow statement for specifying iteration. It allows code to be executed repeatedly.", # java res 1
    "while": "A while loop executes a block of code as long as a specified condition is true.", # java res 2
    "if": "An if statement allows conditional execution of a block of code based on a boolean expression.", # java res 3
    "else": "An else statement provides an alternative execution path if the if condition is false.", # java res 4
    "switch": "A switch statement allows a variable to be tested for equality against multiple cases.", # java res 5
    "case": "A case inside a switch statement defines a branch to be executed when the value matches.", # java res 6
    "break": "A break statement terminates the nearest enclosing loop or switch statement.", # java res 7
    "continue": "A continue statement skips the current iteration of a loop and proceeds with the next iteration.", # java res 8
    "return": "A return statement exits from a function and optionally returns a value.", # java res 9
    "public": "Public is an access modifier that allows a member to be accessible from any class.", # java res 10
    "private": "Private is an access modifier that restricts access to the defining class only.", # java res 11
    "protected": "Protected allows access within the same package and by subclasses.", # java res 12
    "static": "A static keyword defines a class-level variable or method that does not require an instance.", # java res 13
    "final": "Final prevents modification of a variable, method, or class once assigned.",  # java res 14
    "abstract": "Abstract defines a class that cannot be instantiated and may contain abstract methods.", # java res 15
    "interface": "An interface in Java is a blueprint for a class that defines abstract methods.", # java res 16
    "extends": "Extends is used to inherit from a superclass.", # java res 17
    "implements": "Implements is used by a class to implement an interface.",   # java res 18
    "instanceof": "Instanceof is used to check if an object is an instance of a class.", # java res 19
    "super": "Super refers to the immediate parent class of a subclass.", # java res 20
    "this": "This is a reference to the current object within an instance method.", # java res 21
    "try": "Try is used to define a block of code that will be tested for exceptions.",  # java res 22
    "catch": "Catch defines a block of code to handle exceptions thrown by a try block.", # java res 23
    "finally": "Finally defines a block of code that is always executed after a try-catch block, regardless of exceptions.", # java res 24
    "throw": "Throw is used to explicitly throw an exception.", # java res 25
}

#### KEYWORD PATTERNS ####  
# Create keytword patterns for matching 
keyword_patterns = {
    "greet": [{"LOWER": {"FUZZY":"greet"}}],
    "help": [{"LOWER": {"FUZZY":"help"}}],
    "bye": [{"LOWER": {"FUZZY":"bye"}}],
    "for": [{"LOWER": "for"}],
    "while": [{"LOWER": "while"}],
    "for": [{"LOWER": "for"}],
    "if": [{"LOWER": "if"}],
    "else": [{"LOWER": "else"}],
    "switch": [{"LOWER": {"FUZZY":"switch"}}],
    "case": [{"LOWER": "case"}],
    "break": [{"LOWER": {"FUZZY":"break"}}],
    "continue": [{"LOWER": {"FUZZY":"continue"}}],
    "return": [{"LOWER": "return"}],
    "public": [{"LOWER": "public"}],
    "private": [{"LOWER": "private"}],
    "protected": [{"LOWER": "protected"}],
    "static": [{"LOWER": "static"}],
    "final": [{"LOWER": "final"}],
    "abstract": [{"LOWER": "abstract"}],
    "interface": [{"LOWER": "interface"}],
    "extends": [{"LOWER": "extends"}],
    "implements": [{"LOWER": "implements"}],
    "instanceof": [{"LOWER": "instanceof"}],
    "super": [{"LOWER": "super"}],
    "this": [{"LOWER": "this"}],
    "try": [{"LOWER": "try"}],
    "catch": [{"LOWER": "catch"}],
    "finally": [{"LOWER": "finally"}],
    "throw": [{"LOWER": "throw"}]
}

# Add the keyword patterns to the matcher
for key, pattern in keyword_patterns.items():
    matcher.add(key, [pattern]) # must be a list of the pattern for keyword

#### PHRASE PATTERNS ####
# Create phrase patterns for matching
phrase_patterns = {
    "greet": ["hello", "hi", "hey", "howdy", "greetings"],
    "help": ["help", "help me", "can you help", "need assistance"],
    "bye": ["goodbye", "bye", "see you later", "see you soon"],
    "for": ["for", "for loop", "for statement", "for keyword"],
    "while": ["while", "while loop", "while statement", "while keyword"],
    "if": ["if", "if statement", "if condition", "if keyword"],
    "else": ["else", "else statement", "else keyword", "else condition"],
    "switch": ["switch", "switch statement", "switch case", "switch keyword"],
    "case": ["case", "case statement", "case label", "case keyword"],
    "break": ["break", "break statement", "break keyword"],
    "continue": ["continue", "continue statement", "continue keyword"],
    "return": ["return", "return statement", "return keyword"],
    "public": ["public", "public keyword", "public modifier", "public access"],
    "private": ["private", "private keyword", "private modifier", "private access"],
    "protected": ["protected", "protected keyword", "protected modifier", "protected access"],
    "static": ["static", "static keyword", "static modifier"],
    "final": ["final", "final keyword", "final modifier"],
    "abstract": ["abstract", "abstract keyword", "abstract class", "abstract method"],
    "interface": ["interface", "interface keyword", "interface definition"],
    "extends": ["extends", "extends keyword", "extends relationship"],
    "implements": ["implements", "implements keyword", "implements interface", "implement"],
    "instanceof": ["instanceof", "instanceof operator", "instanceof keyword"],
    "super": ["super", "super keyword", "super reference"],
    "this": ["this", "this keyword", "this reference", "this object"],
    "try": ["try", "try block", "try statement", "try keyword"],
    "catch": ["catch", "catch block", "catch statement", "catch keyword"],
    "finally": ["finally", "finally block", "finally statement", "finally keyword"],
    "throw": ["throw", "throw statement", "throw exception", "throw keyword"]
}

# add the phrase patterns to the phrase matcher
for key, phrases in phrase_patterns.items():
   patterns = [nlp(term) for term in phrases]
   phraseMatcher.add(key,[*patterns]) # must be a list of the pattern for keyword
 
#### FUNCTIONS #### 

# Function to take user input and return best response for keyword patterns.
def get_response_keyword(user_input):
    doc = nlp(user_input) # Tokenize the user input   
    best_match = "default" # Default response initally for best match 
    
    # Find matches
    keyword_matches = matcher(doc) # Find keyword matches in the user input

    # Get matches 
    matches = []
    # Get the start and end index of the matched keyword
    for mID, start, end in keyword_matches:
        matches.append(mID)

    # Get the best match
    for mID in matches:
        #match_id_str = nlp.vocab[mID].text
        match_id_str = nlp.vocab.strings[mID]
        if match_id_str in response_dict:
            best_match = match_id_str
        else:
            best_match = "default"

    return response_dict[best_match] # Return the response with the best match

# Function to take user input and return best response for phrase patterns. 
def get_response_phrase(user_input):
    doc = nlp(user_input) # Tokenize the user input   
    best_match = "default" # Default response initally for best match 
    
    # Find matches
    phrase_matches = phraseMatcher(doc) # Find phrase matches in the user input

    # Get matches
    matches = []    
    # Get the start and end index of the matched phrase
    for mID, start, end in phrase_matches:
        matches.insert(0, mID)

    # Get the best match
    for mID in matches:
        match_id_str = nlp.vocab.strings[mID]
        if match_id_str in response_dict:
            best_match = match_id_str
        else:
            best_match = "default"

    return response_dict[best_match] # Return the response with the best match

# Function to take user input and return best response for phrase patterns with similarity score.
def get_response_phrase(user_input):
    doc = nlp(user_input) # Tokenize the user input   
    best_match = "default" # Default response initally for best match 
    
    # Find matches
    phrase_matches = phraseMatcher(doc) # Find phrase matches in the user input

    # Get matches
    matches = []    
    # Get the start and end index of the matched phrase
    for mID, start, end in phrase_matches:
        matches.insert(0, mID)

    # Get the best match
    for mID in matches:
        match_id_str = nlp.vocab.strings[mID]

        # Set best match 
        if match_id_str in response_dict:
            best_match = match_id_str
        else:
            best_match = "default"

    return response_dict[best_match] # Return the response with the best match

# Function for general terminal chatbot
def chat(is_generate_sample):
    if is_generate_sample:
        generate_sample()
    else:
        try: 
            print("Chatbot: Hello! (Type 'bye' to exit.)")
            while True:
                user_input = input("You: ")
                if user_input.lower() == "bye":
                    print("Chatbot: " + response_dict["bye"])
                    break
                else:
                    response = get_response_phrase(user_input) # Phrase works way better than keyword
                    print("Chatbot:", response)
    
        except Exception as e:
            print("Error:", e)

# Function for testing general chatbot functionality 
def generate_sample():
    with open("chatbot_samples.txt", "w") as f:
        # user says hi
        user_input = f"Hello how are you"
        response = get_response_phrase(user_input)
        f.write(f"User: {user_input}\n")
        f.write(f"Chatbot: {response}\n\n")

        # user asks for help (generic)
        user_input = f"Help me please"
        response = get_response_phrase(user_input)
        f.write(f"User: {user_input}\n")
        f.write(f"Chatbot: {response}\n\n")

        # user asks for specific keywords
        for keyword in list(response_dict.keys())[4:]:  # Skip the first 4 items
            user_input = f"What is {keyword} in Java?"
            response = get_response_phrase(user_input)
            f.write(f"User: {user_input}\n")
            f.write(f"Chatbot: {response}\n\n")

        # user says random thing to trigger default unknowmn
        user_input = f"what is icecream in java"
        response = get_response_phrase(user_input)
        f.write(f"User: {user_input}\n")
        f.write(f"Chatbot: {response}\n\n")

        # user says bye
        user_input = f"bye"
        response = get_response_phrase(user_input)
        f.write(f"User: {user_input}\n")
        f.write(f"Chatbot: {response}\n\n")



#### MAIN METHOD #### 
if __name__ == "__main__":
    is_generate_sample = False # Flag for running chatbot with sample creation
    chat(is_generate_sample)

