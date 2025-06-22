import collections
import json
import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Type, TypeVar

import litellm
import tenacity
from litellm import completion, completion_cost
from openai import OpenAI
from openai.types.chat import ChatCompletion
from pydantic import BaseModel

from pyframework.jwt_util import logger
from pyframework.utils import current_datetime_tz
from .timezone import get_current_timezone


class ChatUsageModel(BaseModel):
    id: Optional[str] = None
    agent_id: Optional[str] = None
    prompt: int = 0
    response: int = 0
    total: float
    cost: float = 0.0


class ChatMessageType(str, Enum):
    USER_INPUT = "USER_INPUT"
    USER_INFO = "USER_INFO"
    ASSISTANT_FOLLOW_UP_QUESTION = "ASSISTANT_FOLLOW_UP_QUESTION"
    ASSISTANT_INFORMATIONAL = "ASSISTANT_INFORMATIONAL"
    ASSISTANT_REPLY = "ASSISTANT_REPLY"
    NOTIFICATION = "NOTIFICATION"
    ORIENTATION = "ORIENTATION"
    REFERENCE_DATA = "REFERENCE_DATA"



pending_chat_usages = []

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

litellm.drop_params = True

# litellm.enable_json_schema_validation = True
# litellm.set_verbose=True
# os.environ['LITELLM_LOG'] = 'DEBUG'


ModelConfig = collections.namedtuple('ModelConfig',
                                     [
                                         'classification',
                                         'big_summary',
                                         'code',
                                         'summary',
                                         'reminder',
                                         'reminder_process',
                                         'answer',
                                         'question',
                                         'command',
                                         'infer_context',
                                         'response_eval',
                                         'response_prep',
                                         'response_refine',
                                         'grounding',
                                         'utility',
                                         'decision',
                                         'scrape',
                                         'reference',
                                         'post_answer',
                                         'reason',
                                         'quick_reason',
                                         'alt_reason',
                                     ])

gpt_main_alt = os.getenv('GPT_MAIN', 'gpt-4.1')
gpt_o3_mini = os.getenv('GPT_MAIN', 'o3-mini')
gpt_main = os.getenv('GPT_MAIN', 'gpt-4.1')
gpt_command = os.getenv('GPT_MAIN', 'gpt-4.1')
gpt_mini = os.getenv('GPT_MINI', 'gpt-4.1-mini')
gpt_reasoning = os.getenv('GPT_REASONING', 'o3')
gpt_quick_reasoning = os.getenv('GPT_REASONING', 'o4-mini')
gemini_flash = os.getenv('GEMINI_FLASH', 'gemini/gemini-2.0-flash-exp')
gemini_flash_reasoning = os.getenv('GEMINI_FLASH', 'gemini/gemini-2.0-thinking-exp-1219')
gemini_pro = os.getenv('GEMINI_PRO', 'gemini/gemini-1.5-pro-002')
claude_sonnet = os.getenv('CLAUDE_SONNET', 'claude-3-5-sonnet-20241022')
claude_haiku = os.getenv('CLAUDE_SONNET', 'claude-3-5-haiku-20241022')
groq_versatile = os.getenv('GROQ_VERSATILE', 'groq/llama-3.1-70b-versatile')
groq_high = os.getenv('GROQ_HIGH', 'groq/llama-3.2-3b-preview')
deepseek_reasoner = os.getenv('DEEPSEEK_REASONER', 'deepseek-reasoner')

MODEL_CONFIG = ModelConfig(
    classification=gpt_main,
    big_summary=gpt_main,
    code=gpt_main_alt,
    summary=groq_versatile,
    reminder=gpt_main,
    reminder_process=gpt_main,
    answer=gpt_mini,
    question=gpt_mini,
    command=gpt_main,
    infer_context=gpt_mini,
    response_eval=gpt_main,
    response_prep=gpt_mini,
    response_refine=gpt_mini,
    grounding=gemini_flash,
    utility=gpt_main,
    decision=gpt_main,
    scrape=gemini_flash,
    reference=gpt_mini,
    post_answer=gpt_quick_reasoning,
    reason=gpt_quick_reasoning,
    quick_reason=gpt_quick_reasoning,
    alt_reason=deepseek_reasoner,
)

client_openai = OpenAI()

class BaseChat(ABC):

    @abstractmethod
    def __init__(self, system_instruction: str, model_name: str, functions=None):
        self.system_instruction = system_instruction
        self.model_name = model_name
        self.functions = functions

    @abstractmethod
    def create_model(self, chat_history: List = None, add_tools=True):
        pass

    @abstractmethod
    def start_session(self, chat_history: List = None):
        pass

    @abstractmethod
    def communicate(self, messages: List):
        pass

    @abstractmethod
    def send_message(self, message: str, json_mode: bool = False, json_schema: Optional[List] = None):
        pass

    @abstractmethod
    def reset_chat(self):
        pass


def create_chat_message(role, content, timestamp=None):
    """
    Create a chat message with the given role and content.

    Args:
    role (str): The role of the message sender, e.g., "system", "user", or "assistant".
    content (str): The content of the message.

    Returns:
    dict: A dictionary containing the role and content of the message.
    """
    return {"role": role, "content": content, **({"timestamp": timestamp} if timestamp else {})}


def add_message(role, content, messages_list):
    messages_list.append(create_chat_message(role, content))


def convert_chat_messages_to_role_format(messages: list, system_prompt: Optional[str] = None):
    converted_messages = []
    if system_prompt:
        converted_messages.append({
            "role": "system",
            "content": system_prompt
        })
    for message in messages:
        #TODO remove this condition when the audio message has content
        if 'media_type' in message and message['media_type'] == "AUDIO" and message['content'] == "":
            continue

        role = "user" if message['type'] in [ChatMessageType.USER_INPUT, ChatMessageType.USER_INFO] else "assistant"
        converted_messages.append({
            "role": role,
            "content": message['content']
        })
    return converted_messages


def convert_memory_entries_to_role_format(memory_entries: list):
    converted_messages = []
    for entry in memory_entries:
        role = "user" if entry['doc_type'] == ChatMessageType.USER_INPUT.name else "assistant"
        converted_messages.append({
            "role": role,
            "content": f"{entry['text']}\n{entry['created_at']}"
        })
    return converted_messages


def group_messages_by_role(messages: list):
    grouped_messages = []
    current_role = None
    current_content = []

    for message in messages:
        # Ensure message['content'] is a list
        content = message["content"] if isinstance(message["content"], list) else [message["content"]]

        if message["role"] == current_role:
            # Append content to the current group
            current_content.extend(content)
        else:
            # Save the previous group if any
            if current_role is not None:
                grouped_messages.append({
                    "role": current_role,
                    "content": current_content
                })
            # Start a new group
            current_role = message["role"]
            current_content = content

    # Append the final group
    if current_role is not None:
        grouped_messages.append({
            "role": current_role,
            "content": current_content
        })

    return grouped_messages


def add_chat_usage(response):
    try:
        if response.usage:
            payload = response.dict() if isinstance(response, ChatCompletion) else response

            try:
                cost = round(completion_cost(completion_response=payload), 4)
            except Exception as e:
                # Cost should be 2.19 per million of response.usage.total_tokens
                cost = round(2.19 * response.usage.total_tokens / 1_000_000, 4)

            usage = ChatUsageModel(
                response=response.usage.completion_tokens,
                prompt=response.usage.prompt_tokens,
                total=response.usage.total_tokens,
                cost=cost
            )
            pending_chat_usages.append(usage)
        else:
            logger.warn("No usage information found in the response")
    except Exception as e:
        logger.warn(f"Error while calculating usage: {e}")

T = TypeVar('T', bound=BaseModel)

def call_llm_completion(target_model,
                        messages,
                        temperature=0.0,
                        response_format: Optional[Type[T]] = None,
                        tools: Optional[List] = None,
                        stream: Optional[bool] = None,
                        **kwargs
):
    # Check if the messages[0] is a system message and replace the marker "datetime" with the current date and time
    if messages and messages[0].get("role") == "system":
        messages[0]["content"] = messages[0]["content"].format(
            datetime=f"\n** The current time and date is {current_datetime_tz().strftime('%Y-%m-%dT%H:%M:%S')}"
                     f"\n** Timezone: {get_current_timezone()}\n"

        )

    target_response_format = response_format
    target_class_response = target_response_format
    if target_model.startswith("gemini"):
        # messages = convert_to_gemini_format(messages)
        safety_settings_arg = safety_settings
    elif target_model.startswith("groq") and target_class_response is not None:
        target_response_format = response_format={"type": "json_object"}
        add_message("user",
                    f"Respond in this format:\n"
                    f"```{json.dumps(target_class_response.model_json_schema(), indent=2)}```",
                    messages)
    elif target_model.startswith("deepseek-reasoner"):
        client = OpenAI(api_key=os.getenv('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

        response = client.chat.completions.create(
            model=target_model,
            temperature=temperature,
            messages=messages
        )

        add_chat_usage(response)

        return response
    else:
        safety_settings_arg = None

    max_attempts = 2
    attempt = 0
    if target_model == 'o3-mini':
        kwargs.pop('temperature', None)
        if 'max_tokens' in kwargs:
            kwargs['max_completion_tokens'] = kwargs.pop('max_tokens')


    completion_params = {
        "messages": messages,
        "model": target_model,
        "stream": stream,
        "response_format": target_response_format,
        "tools": tools,
        **({"safety_settings": safety_settings_arg} if target_model.startswith("gemini") else {}),
        **kwargs
    }

    while attempt < max_attempts:
        attempt += 1
        response = completion(**completion_params)

        add_chat_usage(response)

        if tools is None and response_format is not None:
            try:
                if target_model.startswith("groq") and response_format is not None:
                    # TODO fix for groq
                    response = response_to_json(response)
                    response = response_format(**response)
                elif response_format is not None:
                    response = response_to_json(response)
                    response = response_format(**response)
            except TypeError as e:
                logger.warn(f"Error converting response to {response_format}: {e}")
                # Check if it's the known '**' mapping error and if we have remaining attempts
                if "after '**' must be a mapping" in str(e) and attempt < max_attempts:
                    continue
                raise e
        break

    return response


@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
    retry=tenacity.retry_if_exception_type(Exception),
    reraise=True
)
def call_model(target_model, messages, tools=None, response_format=None, temperature=0.0, max_tokens=None):
    return call_llm_completion(
        target_model=target_model,
        messages=messages,
        tools=tools,
        response_format=response_format,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def call_openai_voice(model, messages, temperature=0.0, **kwargs):
    # Check if the messages[0] is a system message and replace the marker "datetime" with the current date and time
    if messages and messages[0].get("role") == "system":
        messages[0]["content"] = messages[0]["content"].format(
            datetime=f"\n** The current time and date is {current_datetime_tz().strftime('%Y-%m-%dT%H:%M:%S')}"
                     f"\n** Timezone: {get_current_timezone()}\n\n"

        )

    grouped_messages = group_messages_by_role(messages)

    response = client_openai.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=grouped_messages,
        **kwargs
    )

    add_chat_usage(response)

    return response


def prepare_function_call(target_model, messages, tools, response_format=None, temperature=0.0, max_tokens=None):
    response = call_model(
        target_model=target_model,
        messages=messages,
        tools=tools,
        response_format=response_format,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message


def response_to_json(response):
    response_content = response['choices'][0]['message']['content'].strip()
    return json.loads(response_content)
