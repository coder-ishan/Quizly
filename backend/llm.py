from typing import List
from openai import OpenAI
import os
from dotenv import load_dotenv
import pdfParser
from pydantic import BaseModel, ValidationError
import json

load_dotenv()

client = OpenAI(
	base_url="https://api-inference.huggingface.co/v1/",
	api_key= os.getenv("HF_API")
)

def generateQuestions(query):
	context = pdfParser.getContext(query)
	messages = [
		{
			"role": "user",
			"content": f"""
			Generate EXACTLY 5 multiple choice questions that are STRICTLY derived from the following context:

			{context} """
			+
            """
			Requirements:
			1. Each question must be explicitly supported by information present in the context
			2. Do not introduce any external information or assumptions
			3. Each question must have exactly 4 options
			4. All options must be plausible and related to the context
			5. Exactly one option must be correct

			Output Schema:
			[
				{{
					"question": str,  # The complete question text
					"options": list[str],  # Exactly 4 options
					"correct_answer": int,  # 0-based index of correct option (0-3)
					"explanation": str,  # Explanation citing specific evidence from context
					"context_reference": str  # The exact quote from context supporting the answer
				}}
			]

			Validation:
            - Output must be JSON
			- Questions must be unique
			- Options must be distinct from each other
			- Explanation must reference specific content from context
			- All text fields must be non-empty strings
			- correct_answer must be 0, 1, 2, or 3
			"""
		},
	]

	completion = client.chat.completions.create(
		model="meta-llama/Llama-3.2-3B-Instruct", 
		messages=messages, 
		max_tokens=1000
	)

	return completion.choices[0].message.content





import json
import re

def extract_json_from_output(output_text):
    """
    Extracts and cleans JSON from a block of text that contains random text
    surrounding a JSON snippet enclosed by Markdown-style code fences.

    Parameters:
    - output_text (str): The text containing the JSON snippet.

    Returns:
    - dict or list: The parsed JSON object, either as a dictionary or a list.

    Raises:
    - ValueError: If no JSON object can be found or if the JSON is malformed.
    """
    # Define a regular expression pattern to find JSON enclosed in backticks
    pattern = r"```json\s*([\s\S]*?)\s*```"

    # Search for the JSON block using the pattern
    match = re.search(pattern, output_text)

    if not match:
        raise ValueError("No searchable JSON block found in the text.")

    # Extract the JSON string
    json_str = match.group(1).strip()

    # Parse the JSON string into a Python object
    try:
        parsed_json = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON parsing error: {e}")

    return parsed_json


result = extract_json_from_output(generateQuestions("Mahatma Gandhi"))
print(result)

with open('result.json', 'w', encoding='utf-8') as file:
       file.write(json.dumps(result, indent=2))






