"""This file has the function for the AI assistant. It takes a question as input and returns the answer from the AI model."""

from openai import OpenAI

client = OpenAI(
  api_key = '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'
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
