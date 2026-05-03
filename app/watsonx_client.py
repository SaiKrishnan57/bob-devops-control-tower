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
- reference these functions if relevant: `login`, `calculate_total`, `divide_numbers`, `get_user_role`, `apply_discount`
- for hardcoded credentials: ask Bob to COMPLETELY REMOVE them and replace with a TODO comment and return False (do NOT use environment variables or hashing as this adds complexity)
- ask Bob to add zero-division handling in `divide_numbers` that returns None when b==0
- ask Bob to add concise docstrings to ALL functions
- ask Bob to keep function names unchanged
- ask Bob to avoid over-engineering (no imports, no external dependencies, no environment variables)
- ask Bob to return the full updated `app.py`
- ask Bob to generate basic tests WITHOUT hardcoded credentials
- ask Bob to explain changes in before/after format

Critical Instructions for the Bob Prompt:
- The login function should return False and have a TODO comment instead of any credential check
- Do NOT add any imports (os, hashlib, etc.)
- Do NOT use environment variables
- Do NOT create password hashes
- Keep it simple - just remove the security risk entirely
- Tests should NOT contain any hardcoded passwords

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
3. Add concise docstrings to `login`, `calculate_total`, `divide_numbers`, `get_user_role`, and `apply_discount`.

## IBM Bob IDE Prompt
```
Act as a senior software engineer.

Analyze the file `app.py`.

1. Remove hardcoded credentials in the `login` function:
   - COMPLETELY REMOVE the credential check (username == "admin" and password == "admin123")
   - Replace with a TODO comment: # TODO: Implement proper authentication with external credential store
   - Make the function return False for security
   - Do NOT use environment variables, hashing, or any imports
   - Keep it simple

2. Implement zero-division handling in the `divide_numbers` function:
   - Add a check: if b == 0: return None
   - Do NOT raise exceptions
   - Return None when division by zero occurs

3. Add concise docstrings to the following functions: `login`, `calculate_total`, `divide_numbers`, `get_user_role`, and `apply_discount`.
   - Use this format:
     \"\"\"
     Brief description.
     
     Args:
         param: Description
         
     Returns:
         type: Description
     \"\"\"

Ensure that function names remain unchanged. Avoid over-engineering and focus on practical improvements.

Return the full updated `app.py`.

Generate basic tests for the functions mentioned above to ensure their correctness and robustness. Do NOT include hardcoded credentials in tests.

Explain the changes made in before/after format.
```

## Post-Implementation Review
After implementing the fixes, the code health score is expected to improve significantly. Hardcoded credentials will be removed, reducing the risk of unauthorized access. The addition of zero-division handling will prevent application crashes and ensure reliable operation. Concise docstrings will enhance code readability and maintainability.

To verify the effectiveness of these fixes, perform the following checks:
1. Run the analyzer again and confirm the score has improved
2. Test the `divide_numbers` function with a zero divisor to confirm it returns None
3. Review the docstrings for clarity and completeness
4. Execute the generated tests to ensure they pass and cover the expected functionality
"""


def get_watsonx_client():
    try:
        return WatsonxClient()
    except Exception as error:
        print("Warning:", error)
        return None