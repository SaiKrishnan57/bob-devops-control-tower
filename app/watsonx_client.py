import os
import requests
from dotenv import load_dotenv


load_dotenv()


class WatsonxClient:
    def __init__(self):
        self.api_key = os.getenv("WATSONX_API_KEY", "").strip()
        self.project_id = os.getenv("WATSONX_PROJECT_ID", "").strip()
        self.url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com").strip()
        self.model_id = os.getenv("WATSONX_MODEL_ID", "ibm/granite-3-8b-instruct").strip()

        if not self.api_key:
            raise ValueError("WATSONX_API_KEY environment variable is required")

        if not self.project_id:
            raise ValueError("WATSONX_PROJECT_ID environment variable is required")

    def _get_token(self):
        response = requests.post(
            "https://iam.cloud.ibm.com/identity/token",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            },
            data=f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={self.api_key}",
            timeout=30
        )

        if response.status_code != 200:
            print("IAM TOKEN ERROR STATUS:", response.status_code)
            print("IAM TOKEN ERROR BODY:", response.text)

        response.raise_for_status()
        return response.json()["access_token"]

    def generate_summary(self, issues: list, score_data: dict, mcp_findings: list) -> str:
        try:
            print("Calling watsonx...")

            token = self._get_token()
            prompt = self._create_prompt(issues, score_data, mcp_findings)

            endpoint = f"{self.url}/ml/v1/text/generation?version=2023-05-29"

            payload = {
                "model_id": self.model_id,
                "project_id": self.project_id,
                "input": prompt,
                "parameters": {
                    "decoding_method": "greedy",
                    "max_new_tokens": 900,
                    "min_new_tokens": 250,
                    "temperature": 0.2
                }
            }

            response = requests.post(
                endpoint,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                json=payload,
                timeout=60
            )

            if response.status_code != 200:
                print("WATSONX ERROR STATUS:", response.status_code)
                print("WATSONX ERROR BODY:", response.text)

            response.raise_for_status()

            result = response.json()["results"][0]["generated_text"].strip()

            print("watsonx response received")

            return f"""## watsonx.ai Engineering Plan

{result}

---
*Generated dynamically using IBM watsonx.ai model: `{self.model_id}`*
"""

        except Exception as error:
            print("watsonx failed:", error)
            return self._fallback_summary(issues, score_data, mcp_findings, error)

    def _create_prompt(self, issues: list, score_data: dict, mcp_findings: list) -> str:
        return f"""
You are an expert DevOps engineering lead preparing a code improvement plan for IBM Bob IDE.

Your job is to transform raw code-quality findings into a precise, actionable engineering plan and a high-quality IBM Bob prompt.

Code Health:
- Score: {score_data["score"]}/100
- Status: {score_data["status"]}

Static Code Issues:
{issues}

Tool Findings:
{mcp_findings}

Return the response in this exact markdown structure:

## Executive Summary
Write 2 short paragraphs explaining the current code health, the main engineering risks, and why this repo needs improvement.

## Priority Fix Plan
List the top 3 fixes in priority order.
Each fix must mention:
- the file name
- the affected function name if available
- the risk being fixed
- the expected improvement

## IBM Bob IDE Prompt
Write a complete prompt that can be pasted directly into IBM Bob IDE.

The Bob prompt must:
- tell Bob to act as a senior software engineer
- reference the file `app.py`
- reference these functions if relevant: `login`, `calculate_total`, `divide_numbers`, `get_user_role`
- ask Bob to remove or secure hardcoded credentials
- ask Bob to add zero-division handling in `divide_numbers`
- ask Bob to add concise docstrings
- ask Bob to keep function names unchanged
- ask Bob to avoid over-engineering
- ask Bob to return the full updated `app.py`
- ask Bob to generate basic tests
- ask Bob to explain changes in before/after format

Important:
Do not write incomplete code snippets.
Do not generate only a docstring.
Do not stop halfway.
The IBM Bob prompt must be complete and ready to paste.
"""

    def _fallback_summary(self, issues: list, score_data: dict, mcp_findings: list, error=None) -> str:
        return f"""
## watsonx.ai Engineering Plan

Fallback summary used because watsonx.ai failed.

Error:
`{error}`

## Executive Summary
The repository has a code health score of **{score_data["score"]}/100** with status **{score_data["status"]}**. The analysis found **{len(issues)}** static issues and **{len(mcp_findings)}** tool findings.

The highest-priority risks are hardcoded credentials, unsafe division, and missing documentation.

## Priority Fix Plan
1. Fix hardcoded credential risk in `app.py`, especially around `login`.
2. Add zero-division handling in `divide_numbers`.
3. Add concise docstrings to `login`, `calculate_total`, `divide_numbers`, and `get_user_role`.

## IBM Bob IDE Prompt
You are a senior software engineer working inside IBM Bob IDE.

Refactor `app.py` using the following instructions:

1. In `login(username, password)`:
   - Remove hardcoded credentials such as `admin123`.
   - Use a safer approach such as environment variables.
   - Keep the function name unchanged.
   - Keep the implementation simple.

2. In `divide_numbers(a, b)`:
   - Add protection against division by zero.
   - Raise a clear `ValueError` if `b == 0`.

3. In `calculate_total(price, tax)`:
   - Add simple validation for invalid or negative values if appropriate.
   - Keep the function easy to understand.

4. In `get_user_role(user)`:
   - Keep the function name unchanged.
   - Improve readability without over-engineering.

5. Add concise docstrings to:
   - `login`
   - `calculate_total`
   - `divide_numbers`
   - `get_user_role`

6. Generate basic tests for the changed functions.

Constraints:
- Do not introduce complex architecture.
- Do not create custom exception classes unless necessary.
- Do not rename existing functions.
- Return the full updated `app.py`.
- Explain each change using a before/after format.
"""


def get_watsonx_client():
    try:
        return WatsonxClient()
    except Exception as error:
        print("Warning:", error)
        return None