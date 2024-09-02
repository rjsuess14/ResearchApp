##load API key
from dotenv import load_dotenv
import os

load_dotenv()
OAI_api_key = os.getenv('OPENAI_API')

##Download SEC filing
from langchain_community.document_loaders import UnstructuredURLLoader

url = "https://www.sec.gov/Archives/edgar/data/1559720/000155972024000006/abnb-20231231.htm"
loader = UnstructuredURLLoader(urls=[url], headers={'User-Agent': 'yourname yourname@yourorg.com'})
documents = loader.load()

##Chunk data into texts
from langchain_community.document_loaders import UnstructuredURLLoader

url = "https://www.sec.gov/Archives/edgar/data/1559720/000155972024000006/abnb-20231231.htm"
loader = UnstructuredURLLoader(urls=[url], headers={'User-Agent': 'yourname yourname@yourorg.com'})
documents = loader.load()

##Generate the dataset
from financial_datasets.generator import DatasetGenerator

# Create the dataset generator
generator = DatasetGenerator(
   model="gpt-4-0125-preview",
   api_key=OAI_api_key,
)

dataset = generator.generate_from_texts(texts, max_questions=10)

for index, item in enumerate(dataset.items):
  print(f"Question {index + 1}: {item.question}")
  print(f"Answer: {item.answer}")
  print(f"Context: {item.context}")
  print()

