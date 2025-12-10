from agents import Agent, Runner, function_tool, SQLiteSession, set_default_openai_key, set_trace_processors
from config import settings
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from eval_agent import skill_evaluation_agent
from braintrust import init_logger
from braintrust.wrappers.openai import BraintrustTracingProcessor

# Set API key
set_default_openai_key(settings.OPENAI_API_KEY)
set_trace_processors([BraintrustTracingProcessor(
    init_logger("Prodapt", api_key=settings.BRAINTRUST_API_KEY))])

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
    skills = ["Python", "SQL", "System Design"]
    db["state"][session_id]["skills"] = skills
    return skills

@function_tool
def update_evaluation(session_id: str, skill: str, evaluation_result: bool | str) -> bool:
    if isinstance(evaluation_result, str):
        evaluation_result = True if evaluation_result.lower() == "true" else False
    db["state"][session_id]["evaluation"].append((skill, evaluation_result))
    return True

@function_tool   
def get_next_skill_to_evaluate(session_id: str) -> str | None:
    """Retrieve the next skill to evaluate. Returns None if there are no more skills to evaluate"""
    all_skills = db["state"][session_id]["skills"]
    evaluated = db["state"][session_id]["evaluation"]
    evaluated_skills = [item[0] for item in evaluated]
    remaining_skills = set(all_skills) - set(evaluated_skills)
    try:
        next_skill = remaining_skills.pop()
        print("NEXT SKILL TOOL", next_skill)
        return next_skill
    except KeyError:
        print("No more skills")
        return None


ORCHESTRATOR_SYSTEM_PROMPT = f"""
{RECOMMENDED_PROMPT_PREFIX}

You are an interview orchestrator. Your goal is to evaluate the candidate on the required skills.

# INSTRUCTIONS

Follow the following steps exactly

1. Extract key skills from the job description using extract_skills tool
2. Then welcome the candidate, explain the screening process and ask the candidate if they are ready 
3. Then, use the get_next_skill_to_evaluate tool to get the skill to evaluate
4. If the skill is not `None` then hand off to the "Skills Evaluator Agent" to perform the evaluation. Pass in the skill to evaluate
4. Once you get the response, use the update_evaluation tool to save the evaluation result into the database
5. Once get_next_skill_to_evaluate returns `None`, return a json with a single field `status` set to "done" to indicate completion
"""

ORCHESTRATOR_USER_PROMPT = """
Start an interview for the following values:

session_id: {session_id}
job_id: {job_id}

Begin by welcoming the applicant, extracting the key skills, then evaluate each one.
"""

interview_orchestrator_agent = Agent(
    name="Interview_Orchestrator_Agent",
    instructions=ORCHESTRATOR_SYSTEM_PROMPT,
    model="gpt-5.1",
    tools=[
        extract_skills,
        update_evaluation,
        get_next_skill_to_evaluate
    ]
)

interview_orchestrator_agent.handoffs = [skill_evaluation_agent]
skill_evaluation_agent.handoffs = [interview_orchestrator_agent]

def run(session_id, job_id):
    session = SQLiteSession(f"screening-{session_id}")
    user_input = ORCHESTRATOR_USER_PROMPT.format(job_id=job_id, session_id=session_id)

    agent = interview_orchestrator_agent

    while user_input != 'bye':
        result = Runner.run_sync(agent, user_input, session=session, max_turns=20)
        agent = result.last_agent
        print(result.final_output)
        user_input = input("User: ")
  
def main():
    job_id = 1
    session_id = "session123"
    
    run(session_id, job_id) 
    print(f"FINAL EVALUATION STATUS: {db["state"][session_id]}")

if __name__ == "__main__":
    main()