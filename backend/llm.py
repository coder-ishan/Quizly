from openai import OpenAI
import os
from dotenv import load_dotenv
import pdfParser

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
			"content": f"""Generate EXACTLY 5 multiple choice questions that are STRICTLY derived from the following context:

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
            - Output must be a complete valid JSON string
			- Questions must be unique
			- Options must be distinct from each other
			- Explanation must reference specific content from context
			- All text fields must be non-empty strings
			- correct_answer must be 0, 1, 2, or 3
			"""
		}
	]

	completion = client.chat.completions.create(
		model="meta-llama/Llama-3.2-3B-Instruct", 
		messages=messages, 
		max_tokens=1000
	)

	return completion.choices[0].message.content

def parse_quiz_json(input_string):
    
    start_marker = "```"
    end_marker = "```"
    
    start_index = input_string.find(start_marker) + len(start_marker)
    end_index = input_string.rfind(end_marker)
    
    if start_index == -1 or end_index == -1:
        raise ValueError("Invalid Output")
    
    json_str = input_string[start_index:end_index].strip()
    try:
        parsed_data = json.loads(json_str)
        return parsed_data
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {str(e)}")

result = parse_quiz_json(generateQuestions("Raja Ravi Verma"))
print(result)

with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=2, ensure_ascii=False)
