class Settings:
    # Retrying Mechanism
    API_TRIES = 3
    API_BACKOFF = 2
    # OpenAI Environment Variables
    OPENAI_API_KEY = "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"
    GPT_MODEL = "gpt3.5"
    # Prompt Messages
    OVERALL_SCORE_SUMMARY_MESSAGE = ""
    COMMUNICATION_SCORE_SUMMARY_MESSAGE = ""
    TIPS_ERRORS_MESSAGE = ""


settings = Settings()
