import openai
from chatgpt_api.config import settings


def call_gpt35_turbo(system_message: str, prompt: str, model="gpt-3.5-turbo-16k") -> str:
    """Calls OpenAI GPT3.5 turbo API with the specified system message and prompt"""
    result = ""
    tries = 0
    while not result and tries < settings.API_TRIES:
        try:
            openai.api_key = settings.OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                # model="gpt-3.5-turbo",
                model=model,
                temperature=0.0,
                timeout=settings.TIMEOUT,
                request_timeout=settings.REQUEST_TIMEOUT,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
            )
            result = response["choices"][0]["message"]["content"]
        except Exception as e:
            print(str(e))
            tries += 1
    return result


def call_gpt3_davinci(system_message: str, prompt: str) -> str:
    """Calls OpenAI GPT-3 Davinci API with the specified system message and prompt"""
    tries = 0
    result = ""
    prompt = f"{system_message}\n\n{prompt}"
    while not result and tries < settings.API_TRIES:
        try:
            openai.api_key = settings.OPENAI_API_KEY
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.0,
                timeout=settings.TIMEOUT,
                request_timeout=settings.REQUEST_TIMEOUT,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            result = response["choices"][0]["text"]
        except Exception as e:
            print(str(e))
            tries += 1
    return result


def call_gpt4(system_message: str, prompt: str) -> str:
    """Calls OpenAI GPT-4 API with the specified system message and prompt"""
    result = ""
    tries = 0
    while not result and tries < settings.API_TRIES:
        try:
            openai.api_key = settings.OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model="gpt-4",
                temperature=0.0,
                timeout=settings.TIMEOUT,
                request_timeout=settings.REQUEST_TIMEOUT,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
            )
            result = response["choices"][0]["message"]["content"]
        except Exception as e:
            print(str(e))
            tries += 1
    return result


def call_gpt_api(system_message: str, prompt: str, model="gpt-3.5-turbo-16k") -> str:
    """Selects and calls the correct GPT model to use from settings"""
    if settings.GPT_MODEL == "gpt3.5":
        # GPT3.5
        return call_gpt35_turbo(system_message, prompt, model)
    elif settings.GPT_MODEL == "davinci":
        # GPT3 Davinci
        return call_gpt3_davinci(system_message, prompt)
    else:
        # GPT-4
        return call_gpt4(system_message, prompt)
