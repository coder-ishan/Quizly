from typing import List
from openai import OpenAI
import os
from dotenv import load_dotenv
import pdfParser
from pydantic import BaseModel, ValidationError
import json
import re

load_dotenv()

client = OpenAI(
	base_url="https://api-inference.huggingface.co/v1/",
	api_key= os.getenv("HF_API")
)


def extract_json_from_output(output_text):

    json_specific_pattern = r"```json\n([\s\S]*?)\n```"  
    generic_fence_pattern = r"```[\s\S]*?({[\s\S]*?}|\[[\s\S]*?\])[\s\S]*?```"  
    
    
    match = re.search(json_specific_pattern, output_text)
    
    
    if not match:
        match = re.search(generic_fence_pattern, output_text)
    
    if not match:
        raise ValueError("No JSON block found in the text.")
    
    json_str = match.group(1).strip()
    
    try:
        parsed_json = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON parsing error: {e}\nExtracted JSON string:\n{json_str}")
    
    return parsed_json


def generateQuestions(query,id):
	context =  pdfParser.getContext(query,id)
	
	messages = [
		{
			"role": "user",
			"content": f"""
			Generate EXACTLY 5 multiple choice questions that are STRICTLY derived from the following context:

			{context} on query related to {query} """
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
			- Options must be distinct from each other
			- Explanation must reference specific content from context
			- All text fields must be non-empty strings
			- correct_answer must be 0, 1, 2, or 3
			"""
		},
	]
	print("question bana rha abb ")
	completion = client.chat.completions.create(
		model="meta-llama/Llama-3.2-3B-Instruct", 
		messages=messages, 
		max_tokens=1000
	)

	return  extract_json_from_output(completion.choices[0].message.content)


