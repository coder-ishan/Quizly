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
from jsonformer import Jsonformer
from transformers import AutoModelForCausalLM, AutoTokenizer

load_dotenv()

client = OpenAI(
	base_url="https://api-inference.huggingface.co/v1/",
	api_key= os.getenv("HF_API")
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
        parsed_json = json.loads(match)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return [
				{{
					"status": "error",
				}}
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
			"content": f"""
			   
			Generate EXACTLY {numQuestions} multiple choice questions with {difficulty} difficulty level that are STRICTLY derived from the following context:

			{context} on query related to {query} """
			+
			"""
			Requirements:
			1. Each question must be explicitly supported by information present in the context
			2. Do not introduce any external information or assumptions
			3. Each question must have exactly 4 options
			4. All options must be plausible and related to the context
			5. Exactly one option must be correct
			6. Return in valid JSON format schema

			Output Schema:
			[
				{
					"question": str,  # The complete question text
					"options": list[str],  # Exactly 4 options
					"correct_answer": int,  # 0-based index of correct option (0-3)
					"explanation": str,  # Explanation citing specific evidence from context
					"context_reference": str  # The exact quote from context supporting the answer
				}
			]

			Validation:
			- Output must be a valid JSON following the schema
			- Options must be distinct from each other
			- Explanation must reference specific content from context
			- All text fields must be non-empty strings
			- correct_answer must be 0, 1, 2, or 3
			"""
		},
	]
	print("Generating question now...")
	completion = client.chat.completions.create(
		model="meta-llama/Llama-3.2-3B-Instruct",
		messages=messages,
		max_tokens=1000
	)
		   
	print (completion.choices[0].message.content)
	return extract_json_from_output(completion.choices[0].message.content)
    


	