from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser

from config import settings

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-5.1", api_key=settings.OPENAI_API_KEY)

class ReviewedDescription(BaseModel):
    overall_summary: str

prompt_template = """
You are an expert HR job description analyst specializing in inclusive hiring practices.

Analyze the provided job description for potential issues across these dimensions:

1. CLARITY: Identify sections with vague responsibilities, unclear expectations, or ambiguous requirements.
   Flag phrases like "various duties," "other tasks as assigned," or undefined acronyms.

2. JARGON: Flag unnecessarily technical language inappropriate for the role level.
   Consider whether terms would be understood by qualified candidates unfamiliar with internal terminology.

3. BIAS: Identify language that may discourage diverse candidates:
   - Gender-coded words (e.g., "rockstar," "ninja," "aggressive," "nurturing")
   - Age bias (e.g., "digital native," "recent graduate")
   - Exclusionary phrases (e.g., "culture fit," "work hard/play hard")
   - Excessive requirements (unnecessarily requiring degrees or years of experience)

4. MISSING INFORMATION: Note absent critical details:
   - Salary range or compensation structure
   - Work location/arrangement (remote/hybrid/onsite)
   - Reporting structure or team context
   - Clear distinction between required vs. preferred qualifications
   - Application process and timeline
   - Growth/development opportunities

5. SUMMARY: Provide 2-3 sentences describing overall quality and primary concerns.

For each issue you identify:
- Quote the exact problematic text
- Explain why it is problematic

Your output MUST be valid JSON that conforms exactly to the provided schema.
Do not include any text outside the JSON.

If information is missing, return empty arrays.

Analyze the following job description:

--- JOB DESCRIPTION ---
{description}
----------------------

Return only JSON.

{format_instructions}
"""                                                


def review_description(description: str):
    
    parser = PydanticOutputParser(pydantic_object=ReviewedDescription)
    prompt = PromptTemplate(
      template=prompt_template,
        input_variables=["description"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
      )
    prompt_and_model = prompt | model | parser
    output: ReviewedDescription = prompt_and_model.invoke({"description": description})
    # result: ReviewedDescription = parser.invoke(output)
    return output
    