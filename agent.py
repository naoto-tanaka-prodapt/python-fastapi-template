import asyncio
from agents import Agent, Runner, function_tool, SQLiteSession, set_default_openai_key
from config import settings

# Set API key
set_default_openai_key(settings.OPENAI_API_KEY)

# Create DB
db = {
    "job_descriptions": {
        1: "I need an AI Engineer who knows langchain"
    },
    "state": {
        "session123": {
            "skills": [],
            "evaluation": [] # list of typles (Skill, True/False), eg: [("Python", True)]
        }
    }
}

@function_tool
def extract_skills(session_id: str, job_id: int) -> list[str]:
    return ["Python", "SQL", "System Design"]

@function_tool
def update_evaluation(session_id: str, skill: str, evaluation_result: bool | str) -> bool:
    if isinstance(evaluation_result, str):
        evaluation_result = True if evaluation_result.lower() == "true" else False
    db["state"][session_id]["evaluation"].append((skill, evaluation_result))
    return True

@function_tool
def transfer_to_skill_evaluator(session_id: str, skill: str) -> bool:
    return True


INSTRUCTION = """
You are an interview orchestrator. Your goal is to evaluate the candidate on the required skills.

# INSTRUCTIONS

Follow the following steps exactly

1. Extract key skills from the job description using extract_skills tool
2. Then welcome the candidate, explain the screening process and ask the candidate if they are ready 
3. Then, for EACH skill in the list, use transfer_to_skill_evaluator tool to delegate evaluation
4. Once you get the response, use the update_evaluation tool to save the evaluation result into the database
5. Once all skills are evaluated, mention that the screening is complete and thank the candidate for their time
"""

ORCHESTRATOR_USER_PROMPT = """
Start an interview for the following values:

session_id: {session_id}
job_id: {job_id}

Begin by welcoming the applicant, extracting the key skills, then evaluate each one.
"""


async def run_orchestrator_agent(session_id, job_id):
    session = SQLiteSession(f"screening-{session_id}")

    interview_orchestrator_agent = Agent(
        name="Interview_Orchestrator_Agent",
        instructions=INSTRUCTION,
        model="gpt-5.1",
        tools=[
            extract_skills,
            transfer_to_skill_evaluator,
            update_evaluation
        ]
    )

    query = ORCHESTRATOR_USER_PROMPT.format(job_id=job_id, session_id=session_id)

    user_reply = ""
    while user_reply != "bye":
        result = await Runner.run(
            interview_orchestrator_agent,
            query,
            session=session
        )
        print(f"Answer: {result.final_output}")
        user_reply = input("User: ")

    
async def main():
    job_id = 1
    session_id = "session123"
    
    await run_orchestrator_agent(session_id, job_id) 
    print(f"FINAL EVALUATION STATUS: {db["state"][session_id]}")

if __name__ == "__main__":
    asyncio.run(main())