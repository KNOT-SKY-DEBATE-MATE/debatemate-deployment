import openai

from decouple import config
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.exceptions import HTTPException


class TalkMessage(BaseModel):

    # OpenAI role
    role: str

    # OpenAI content
    content: str


class Talk(BaseModel):

    # Meeting description
    description: str

    # Meeting contents of messages
    messages: list[TalkMessage]


class TalkAnnotation(BaseModel):

    # Summary of talk
    summary: str

    # Suggestions of talk
    suggestion: str

    # Criticism of talk
    criticism: str | None

    # Evaluation of talk
    evaluation: str

    # Warning of talk
    warning: str | None


# Create FastAPI application
application = FastAPI()

# Create OpenAI API client
client = openai.Client(api_key=config("OPENAI_API_KEY"))

# Create OpenAI tools
tools = [
    {
        "name": "annotate",
        "description": "議論内容を分析し、要約、提案、批判、評価、ポリシー違反の警告を提供します。",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "議論全体の簡潔な要約。",
                    "maxLength": 255,
                },
                "suggestion": {
                    "type": "string",
                    "description": "議論の方向性や内容に関する提案。",
                    "maxLength": 255
                },
                "criticism": {
                    "type": "string",
                    "description": "論理的な洞察や発話内容の間違いに関する批判。",
                    "maxLength": 255
                },
                "evaluation": {
                    "type": "string",
                    "description": "発話内容に対する批判を踏まえた評価。",
                    "maxLength": 255
                },
                "warning": {
                    "type": "string",
                    "description": "ポリシー違反やメンバーの行動に関する警告。",
                    "maxLength": 255
                }
            },
            "required": ["summary", "suggestion", "evaluation"]
        }
    }
]


@application.post("/ai/annotate/")
async def onannotate(talk: Talk):
    """
    Annotate meeting contents
    """

    try:
        # Call OpenAI API
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content":
                        "<BEHAVIOR>"
                        "<ANNOUNCE>"
                        "あなたは議長です。"
                        "以下のポリシーに従って、議論を分析し、要約してください。"
                        "</ANNOUNCE>"
                        "<POLICY>"
                        "- 感情的にならず、中立的であること。"
                        "- 論理的で批判的な視点を持つこと。"
                        "- 議論メンバーの意見を適切に要約、批判、評価すること。"
                        "- 議題から外れた発言があれば指摘すること。"
                        "- 常に日本語で回答すること。"
                        "</POLICY>"
                        "</BEHAVIOR>"
                        "<TOPIC>{}</TOPIC>".format(talk.description)
                },
            ] + [
                {
                    "role": "user",
                    "content":
                        "<MESSAGE>"
                        "<SPEAKER>{}</SPEAKER>"
                        "<CONTENT>{}</CONTENT>"
                        "</MESSAGE>".format(message.sender.nickname, message.content)
                } for message in talk.messages
            ],
            tools=tools,
            tool_choice="annotate",
            temperature=1.0,
        )

        # Parse response
        return TalkAnnotation(**response["choices"][0]["message"]["content"])

    except Exception as e:

        # Return error
        raise HTTPException(status_code=500, detail=str(e))
