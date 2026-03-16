from langchain_core.prompts import ChatPromptTemplate


SYSTEM_PROMPT = """You are an AI healthcare planning assistant.

You are NOT a doctor and you do NOT provide diagnoses.
You provide structured, general informational guidance only.

Always include clear disclaimers that this is not medical advice and that the user must consult a qualified healthcare professional for diagnosis and treatment.
"""

USER_PROMPT_TEMPLATE = """A user has described the following symptoms and context:

Symptoms: {symptoms}
Age: {age}
Sex: {sex}
Duration: {duration}

Using this information, provide structured healthcare planning advice in FOUR clearly delineated sections:

1. Possible Conditions
2. Precautions
3. Medication Guidance
4. Nutrition Advice

Requirements:
- Be cautious and conservative; when in doubt, recommend seeing a doctor.
- Do NOT make definitive diagnoses.
- Do NOT prescribe specific dosages or off-label use.
- Highlight any red-flag symptoms that warrant urgent or emergency care.
- Write in clear, layman-friendly language.
- End with a short disclaimer reiterating that this is not a substitute for professional medical advice.
"""


def build_prompt():
    return ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("user", USER_PROMPT_TEMPLATE),
        ]
    )

