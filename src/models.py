from openai import OpenAI
import anthropic
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Retrieve API keys from environment
openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Warn if any API key is missing
if not openai_api_key:
    print("❌ OpenAI API Key is missing!")

if not anthropic_api_key:
    print("❌ Anthropic API Key is missing!")

# Initialize API clients
openai = OpenAI(api_key=openai_api_key)
claude = anthropic.Anthropic()

# Model names
OPENAI_MODEL = "gpt-4o-mini"
CLAUDE_MODEL = "claude-3-5-sonnet-20240620"

# Call OpenAI's GPT model with prompt and system message
def get_gpt_completion(prompt, system_message):
    try:
        response = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            stream=False,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"GPT error: {e}")
        raise

# Call Anthropic's Claude model with prompt and system message
def get_claude_completion(prompt, system_message):
    try:
        result = claude.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=2000,
            system=system_message,
            messages=[{"role": "user", "content": prompt}]
        )
        return result.content[0].text
    except Exception as e:
        print(f"Claude error: {e}")
        raise
