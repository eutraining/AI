from database.db_data import fetch_prompt_message


class Settings:
    # Retrying Mechanism
    API_TRIES = 3
    API_BACKOFF = 2
    # OpenAI Environment Variables
    TIMEOUT = 90
    OPENAI_API_KEY = "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"
    GPT_MODEL = "gpt3.5"
    # Fine-Tuning Variables
    N_EPOCHS = 15
    # Prompt Messages
    BASE_MESSAGE = fetch_prompt_message("./prompt_messages_files/BASE_MESSAGE.txt")
    OVERALL_SCORE_SUMMARY_MESSAGE = BASE_MESSAGE + fetch_prompt_message("./prompt_messages_files/OVERALL_SCORE_SUMMARY_MESSAGE.txt")
    COMMUNICATION_SCORE_SUMMARY_MESSAGE = BASE_MESSAGE + fetch_prompt_message("./prompt_messages_files/COMMUNICATION_SCORE_SUMMARY_MESSAGE.txt")
    TIPS_ERRORS_MESSAGE = BASE_MESSAGE + fetch_prompt_message("./prompt_messages_files/TIPS_ERRORS_MESSAGE.txt")
    OVERALL_SCORE_MESSAGE = BASE_MESSAGE + fetch_prompt_message("./prompt_messages_files/OVERALL_SCORE_MESSAGE.txt")
    OVERALL_SUMMARY_MESSAGE = BASE_MESSAGE + fetch_prompt_message("./prompt_messages_files/OVERALL_SUMMARY_MESSAGE.txt")
    COMMUNICATION_SCORE_MESSAGE = BASE_MESSAGE + fetch_prompt_message("./prompt_messages_files/COMMUNICATION_SCORE_MESSAGE.txt")
    COMMUNICATION_SUMMARY_MESSAGE = BASE_MESSAGE + fetch_prompt_message("./prompt_messages_files/COMMUNICATION_SUMMARY_MESSAGE.txt")
    SUMMARY_MESSAGE = fetch_prompt_message("./prompt_messages_files/SUMMARY_MESSAGE.txt")


settings = Settings()
