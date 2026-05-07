import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def get_resume_tips(job_description: str) -> list[str]:
    """
    Takes a job description and returns 3 tailored resume bullet points using Gemini API.

    Args:
        job_description: The full job description text

    Returns:
        A list of 3 resume bullet points optimized for the job
    """
    if not GEMINI_API_KEY:
        return [
            "Error: GEMINI_API_KEY not configured. Please set it in your .env file.",
            "",
            ""
        ]

    try:
        model = genai.GenerativeModel("gemini-pro")

        prompt = f"""Based on this job description, provide exactly 3 specific, actionable resume bullet points that would help a candidate stand out for this role. Format as a numbered list.

Job Description:
{job_description}

Return only the 3 bullet points, nothing else."""

        response = model.generate_content(prompt)

        if response.text:
            # Parse the response to extract 3 bullet points
            lines = response.text.strip().split('\n')
            bullet_points = []

            for line in lines:
                line = line.strip()
                # Remove numbering (1., 2., 3., etc.)
                if line and any(char.isalpha() for char in line):
                    cleaned = line.lstrip('0123456789.-) ')
                    if cleaned:
                        bullet_points.append(cleaned)

            # Return exactly 3 points, or fill with empty if less
            while len(bullet_points) < 3:
                bullet_points.append("")

            return bullet_points[:3]
        else:
            return ["No response from API", "", ""]

    except Exception as e:
        return [f"Error calling Gemini API: {str(e)}", "", ""]
