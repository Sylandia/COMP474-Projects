import spacy
from spacy.matcher import Matcher

# Load the model 
nlp = spacy.load("en_core_web_sm")

# Initialize the matcher
# matcher = Matcher(nlp.vocab) 
# response_dict = {
#     # Generic responses 
#     "greet": "Hello! How can I help you today?",
#     "bye": "Goodbye! Have a great day!",
#     "help": "I can answer your questions. Try asking about something more specific!",
#     "default": "I'm sorry, I didn't understand that. Could you rephrase?",
#     # Java Keyword/Statement responses 
#     "for": "A for loop is a loop that allows you to iterate over a sequence of items. It is used to repeat a block of code a certain number of times. For example, you can use a for loop to iterate over a list of numbers and print each number to the console.",
#     "while": "A while loop is a loop that allows you to repeat a block of code as long as a certain condition is true. It is used to repeat a block of code until a condition is met. For example, you can use a while loop to repeat a block of code until a user enters a specific input.",
#     "if": "An if statement is a conditional statement that allows you to execute a block of code only if a certain condition is true. It is used to make decisions in your code. For example, you can use an if statement to check if a number is greater than 10 and print a message to the console if it is.",
#     "else": "An else statement is used in conjunction with an if statement to execute a block of code if the if condition is false. It is used to provide an alternative block of code to execute when the if condition is not met. For example, you can use an else statement to print a message to the console if a number is not greater than 10.",
#     "switch": "A switch statement is a conditional statement that allows you to execute different blocks of code based on the value of a variable. It is used to make decisions in your code with multiple possible outcomes. For example, you can use a switch statement to check the value of a variable and execute different blocks of code based on the value.",
#     "break": "A break statement is used to exit a loop or switch statement. It is used to terminate the execution of a loop or switch statement and continue with the next statement in the program. For example, you can use a break statement to exit a loop when a certain condition is met.",
#     "continue": "A continue statement is used to skip the current iteration of a loop and continue with the next iteration. It is used to skip over certain iterations of a loop based on a condition. For example, you can use a continue statement to skip over even numbers in a loop and only process odd numbers.",
#     "return": "A return statement is used to exit a function and return a value to the caller. It is used to pass a value back to the caller of a function. For example, you can use a return statement to return the result of a calculation from a function to the main program.",

# }

matcher = Matcher(nlp.vocab)
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

def get_response(user_input):
    doc = nlp(user_input) # Tokenize the user input   
    best_match = "default" # Default response initally for best match 
    matches = matcher(doc) # Find matches in the user input
    
    # get the best match
    for mID, start, end in matches:
        match_id_str = nlp.vocab[mID].text
        if match_id_str in response_dict:
            best_match = match_id_str
        else:
            best_match = "default"

    return response_dict[best_match] # Return the response with the best match

def chat():
    print("Chatbot: Hello! (Type 'bye' to exit.)")
    while True:
        user_input = input("You: ")
        # print("User:", user_input)wha
        if user_input.lower() == "bye":
            print("Chatbot: Goodbye! Have a great day!")
            break
        else:
            response = get_response(user_input)
            print("Chatbot:", response)
# Create pattern for matching 
# keyword_patterns = { 
    
#     "for": [{"LOWER": "for"},],
#     "while": [{"LOWER": "while"},],
#     "if": [{"LOWER": "if"},],
#     "else": [{"LOWER": "else"},],
#     "switch": [{"LOWER": {"FUZZY":"switch"}},],
#     "break": [{"LOWER": {"FUZZY":"break"}},],throws
#     "continue": [{"LOWER": {"FUZZY":"continue"}},],
#     "return": [{"LOWER": "return"},],
# }

keyword_patterns = {
    "for": [{"LOWER": "for"}],
    "while": [{"LOWER": "while"}],
    "if": [{"LOWER": "if"}],
    "else": [{"LOWER": "else"}],
    "switch": [{"LOWER": "switch"}],
    "case": [{"LOWER": "case"}],
    "break": [{"LOWER": "break"}],
    "continue": [{"LOWER": "continue"}],
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


# Add the patterns to the matcher
for key, pattern in keyword_patterns.items():
    matcher.add(key, [pattern]) # must be a list of the pattern for keyword


def generate_sample():
    with open("chatbot_samples.txt", "w") as f:
        for keyword in response_dict.keys():
            user_input = f"What is {keyword} in Java?"
            response = get_response(user_input)
            f.write(f"User: {user_input}\n")
            f.write(f"Chatbot: {response}\n\n")
generate_sample()


chat()






