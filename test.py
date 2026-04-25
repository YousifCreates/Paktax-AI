import os
os.environ['PYTHONPATH'] = '.'
from chain.qa_chain_openai import ask

result = ask('Hi, At which amount of savings, am i suppose to pay a tax?')
print(result)