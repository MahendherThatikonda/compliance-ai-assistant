import os
import sys

sys.path.append(os.path.abspath("."))

from src.rag_pinecone.generation.rag_pipeline import rag_answer


question = "What are the requirements for gully traps?"

answer = rag_answer(question)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(answer)