from typing import List
import aiofiles
from openai import OpenAI
import os
from dotenv import load_dotenv
import pdfParser
from pydantic import BaseModel, ValidationError
import json
import re
from langchain_community.document_loaders import PyMuPDFLoader
from groq import Groq

load_dotenv()

client  = Groq(
    api_key=os.environ.get("GROQ_API"),
)


async def extract_json_from_output(output_text):

    json_specific_pattern = r"```json\n([\s\S]*?)\n```"  
    generic_fence_pattern = r"```[\s\S]*?({[\s\S]*?}|\[[\s\S]*?\])[\s\S]*?```"  
    
    
    match = re.search(json_specific_pattern, output_text)
    
    
    if not match:
        match = re.search(generic_fence_pattern, output_text)
    
    if not match:
        raise ValueError("No JSON block found in the text.")
    
    try:
        parsed_json = json.loads(match.group(0))
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return [
				{
					"status": "error",
				}
				]
    
    return parsed_json


    

async def generateQuestions(query, quizId, numQuestions, difficulty, files):
	context = ""
	upload_dir = f"uploads/{quizId}"
	
	# Ensure the directory exists
	os.makedirs(upload_dir, exist_ok=True)
	
	for file in files:
		file_path = f"{upload_dir}/{file.filename}"
		
		# Write the file content
		async with aiofiles.open(file_path, "wb") as buffer:
			content = await file.read()
			await buffer.write(content)
		
		# Ensure the file is not empty before loading
		if os.path.getsize(file_path) > 0:
			loader = PyMuPDFLoader(file_path)
			docs = loader.load()
			context = pdfParser.getContext(query, quizId, docs)
		else:
			print(f"File {file_path} is empty.")
		
		print("Context:") 
		print(context)
	messages = [
		{
			"role": "user",
			"content": f"""You are a helpful assistant that generates multiple choice questions from a given context. Please generate {numQuestions} multiple choice questions with {difficulty} difficulty level that are strictly derived from the following context:

			{context}

			The questions should be related to the query: {query}

			The format of the response should be a List of JSON objects, where each object contains the following keys:

			* `question`: The complete question text
			* `options`: Exactly 4 options
			* `correct_answer`: 0-based index of the correct option (0-3)
			* `explanation`: Explanation citing specific evidence from the context but do not mention "context"
			* `context_reference`: The exact quote from the context supporting the answer

			Please ensure that the questions are unique, unbiased, and unambiguous. The options should be plausible and the correct answer should be objectively verifiable using the context provided. Also, please make sure that the questions and options do not include any unrelated or misleading information.
		"""
            +
            """
			Here's an example of a valid response for one question:

			
			[
				{
					"question": String,
					"options": [String, String, String, String],
					"correct_answer": Integer,
					"explanation": String,
					"context_reference": String
				},
			]
			

			Please generate the questions in the given format as the example above. Thank you!
			""",
		},
	]
	print("Generating question now...")
	try:
		completion = client.chat.completions.create(
			model="llama-3.3-70b-specdec",
			messages=messages,
			max_tokens=1024,
			temperature=1,
			response_format={"type": "json_object"},
			top_p=1,
		)
		print(completion.choices[0].message.content)
	except Exception as e:
		print(f"Erorr: {e}")
	result = completion.choices[0].message.content
	return result
    


	