import json
from random import choice
from typing import Literal, Tuple
from agents import Agent, function_tool, set_default_openai_key
from braintrust import load_prompt
from openai import OpenAI
from config import settings
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

# Set API key
set_default_openai_key(settings.OPENAI_API_KEY)

question_bank = {
    "python": {
        "easy": [
            "If `d` is a dictionary, then what does `d['name'] = 'Siddharta'` do?",
            "if `l1` is a list and `l2` is a list, then what is `l1 + l2`?",
        ],
        "medium": [
            "How do you remove a key from a dictionary?",
            "How do you reverse a list in python?"
        ],
        "hard": [
            "If `d` is a dictionary, then what does `d.get('name', 'unknown')` do?",
            "What is the name of the `@` operator (Example `a @ b`) in Python?"
        ]
    },
    "sql": {
        "easy": [
            "What does LIMIT 1 do at the end of a SQL statement?",
            "Explain this SQL: SELECT product_name FROM products WHERE cost < 500'"
        ],
        "medium": [
            "What is a view in SQL?",
            "How do we find the number of records in a table called `products`?"
        ],
        "hard": [
            "What is the difference between WHERE and HAVING in SQL?",
            "Name a window function in SQL"
        ]
    },
    "system design": {
        "easy": [
            "Give one reason where you would prefer a SQL database over a Vector database",
            "RAG requires a vector database. True or False?"
        ],
        "medium": [
            "Give one advantage and one disadvantage of chaining multiple prompts?",
            "Mention three reasons why we may not want to use the most powerful model?"
        ],
        "hard": [
            "Mention ways to speed up retrieval from a vector database",
            "Give an overview of Cost - Accuracy - Latency tradeoffs in an AI system"
        ]
    }
}

@function_tool
def get_question(topic: str, difficulty: Literal['easy', 'medium', 'hard']) -> str:
    return choice(question_bank[topic.lower()][difficulty.lower()])

@function_tool
def check_answer(skill: str, question: str, answer: str) -> Tuple[bool, str]:
    prompt = load_prompt(project="Prodapt", slug="check-answer-prompt-8bad", version="c35af8c353baa23c")
    details = prompt.build(skill=skill, question=question, answer=answer)
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-5.1", temperature=0,
        response_format=details["response_format"],
        messages=details["messages"]
    )
    return json.loads(response.choices[0].message.content)

EVALUATION_SYSTEM_PROMPT = f"""
{RECOMMENDED_PROMPT_PREFIX}

You are a specialised skill evaluator. Your job is to evaluate the candidate's proficiency in a given skill

1. Identify which skill you're evaluating (it will be mentioned in the conversation)
2. Use the get_question tool to get a question to ask (start with 'medium' difficulty). Ask the question verbatim, DO NOT MODIFY it in any way
3. After each candidate answer, use check_answer tool to evaluate
4. Decide the next question:
   - If the check_answer tool returned correct, choose the next higher difficulty, without going above 'hard'
   - If the check_answer tool returned incorrect, choose the lower difficulty, without going below 'easy'
   - Stop after 3 questions MAXIMUM
5. If the correctly answered two of the three questions, then they pass, otherwise they fail
6. After completion of 3 questions, hand off to the "Interview Orchestrator Agent" passing in the result of the evaluation

# DECISION RULES:

- Do not give feedback on the user's answer. Always proceed to the next question
- 3 questions per skill

# OUTPUT:

After the evaluation is complete, return the pass/fail in a json object with the following properties
- result: true or false
"""

EVALUATION_USER_PROMPT = """
Evaluate the user on the following skill: {skill}
"""


skill_evaluation_agent = Agent(
    name="Skill_Evaluation_Agent",
    instructions=EVALUATION_SYSTEM_PROMPT,
    model="gpt-5.1",
    tools=[
        get_question,
        check_answer
    ]
)