"""This file has the function for the AI assistant. It takes a question as input and returns the answer from the AI model."""

from openai import OpenAI

client = OpenAI(
  api_key = '' # Add your OpenAI API key here https://platform.openai.com/api-keys
)

def AIHelp(question):
    """
    This function takes a question as input and returns the answer from the AI model.
    
    Parameters:
    question (str): The question to be asked.

    Returns:
    str: The answer from the AI model.
    """

    completion = client.chat.completions.create(
      model = 'gpt-4o-mini',
      messages = [
        {'role': 'user', 'content': question},
      ]
    )
    return(completion.choices[0].message.content)
