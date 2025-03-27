import ollama 


def generate_response(prompt, model_name='llama3.2'):
    
    """
    To generate a response from Ollama. 
    """

    try: 
        response = ollama.chat(model = model_name ,messages = [
            {
                "role": "user",
                "content": prompt
            }
        ])
        return response 

    except Exception as e: 
        return f"Error generating response: {str(e)}"



if __name__ == "__main__":
    user_input = input("Enter your prompt: ")
    
    try: 
        response = generate_response(user_input)
        print("\nResponse: ")
        print(response)
    
    except Exception as e:  
        print(f"Error: {str(e)}")   