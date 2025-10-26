from langchain_openai import ChatOpenAI

from src.graph.prompts.image_analyzer import IMAGE_ANALYZER_PROMPT
from src.models.api import Report
from src.models.graph import State
from src.settings import Settings


def analyze_image(state: State) -> State:
    messages = [
        ('system', IMAGE_ANALYZER_PROMPT),
    ]
    
    image_message = {
    "role": "user",
    "content": [
        {
            "type": "image",
            "source_type": "url",
            "url": state['image_url'],
        },
    ],
}
    
    messages.append(image_message)

    settings = Settings()
    model = ChatOpenAI(
        model='gpt-4o-mini',
        temperature=settings.DEFAULT_TEMPERATURE,
        top_p=settings.DEFAULT_TOP_P,
        api_key=settings.OPENAI_API_KEY
    )

    model_with_structured_output = model.with_structured_output(Report)

    response = model_with_structured_output.invoke(messages)
    state['report'] = response

    return state
