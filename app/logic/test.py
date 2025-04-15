from google.generativeai import GenerativeModel, list_models
import google.generativeai as genai
import os
from dotenv import *

load_dotenv()

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
for m in list_models():
    print(m.name)
