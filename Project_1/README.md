# **Installation**
For installations, it is general best practice to create a virtual environmnet so to not have conflicting dependencies. 

In command line (terminal):
`python -m venv env`

To activate:
`env/Scripts/activate`  

**NOTE:** For the environment name (`env`) it can be set to whatever you would like. 

Install the required libraries:
`pip install -r requirements.txt`

# **Run the Script**

To run the chatbot: `python chatbot.py`

The chatbot will ask for your input and respond accordingly. You can ask it questions about Java keywords. The list of keywords used can be found at in the dictionary at the top of our script. 

# **is_generate_sample Flag**
The `is_generate_sample` flag, in code, determines whether the chatbot will generate sample conversations and save them to a file.

Set `is_generate_sample` = True to generate sample interactions, otherwise, it will just run the chatbot as usual.


# **Example interaction:**

You: Hello
Chatbot: Hello! How can I help you today?

You: What is for in Java?
Chatbot: A for loop is a control flow statement for specifying iteration. It allows code to be executed repeatedly.

You: Bye
Chatbot: Goodbye! Have a great day!

# **Directory Structure**

/comp474_project_1
    |- chatbot.py           # Main script for the chatbot
    |- requirements.txt     # Required Python libraries
    |- chatbot_samples.txt  # Sample interactions saved here
    |- README.md            # Readme
