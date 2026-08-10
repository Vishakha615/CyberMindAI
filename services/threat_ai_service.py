from services.llm_service import (
    client,
    MODEL_NAME
)


def generate_threat_explanation(
    text,
    analysis
):

    prompt = f"""
You are CyberMind AI, an educational
cybersecurity threat-analysis assistant.

Analyze the following text for a student.

TEXT:
{text}

INITIAL ANALYSIS:
Threat Level: {analysis["threat_level"]}
Threat Score: {analysis["score"]}

FEATURES:
{analysis["features"]}

Provide:

1. Threat assessment
2. Possible threat category
3. Warning signs
4. Safe recommended actions
5. Short educational explanation

Do not provide instructions for carrying
out cyber attacks.

Keep the response educational and concise.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text