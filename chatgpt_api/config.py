class Settings:
    # Retrying Mechanism
    API_TRIES = 3
    API_BACKOFF = 2
    # OpenAI Environment Variables
    TIMEOUT = 90
    OPENAI_API_KEY = "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"
    GPT_MODEL = "gpt3.5"
    # Fine Tuning Variables
    N_EPOCHS = 15
    # Prompt Messages
    BASE_MESSAGE = """
    You are an Online Expert on Case Study Test Evaluation. You will be provided with the case study containing:
    - Case Study Name
    - Instructions/Important Notice
    - Abbreviations (if any)
    - Email Instructions to be followed
    - Case Study Content
    - Trainee's Answer
    Evaluate the following case study test in terms of the accuracy of the analysis,
    the quality of the writing, and the overall effectiveness of the presentation.
    • Be sure to identify both strengths and weaknesses in the case study test.
    • Provide specific examples to support your evaluation.
    • Use clear and concise language."""
    OVERALL_SCORE_SUMMARY_MESSAGE = BASE_MESSAGE + """
    In the output provide the OVERALL_SCORE and OVERALL_SUMMARY in the format:
    - SCORE (X/10)
    - SUMMARY
    DO NOT PROVIDE ANY OTHER INFORMATION EXCEPT THIS!
    """
    COMMUNICATION_SCORE_SUMMARY_MESSAGE = BASE_MESSAGE + """
    In the output provide the COMMUNICATION_SCORE and COMMUNICATION_SUMMARY in the format:
    - SCORE (X/10)
    - SUMMARY
    DO NOT PROVIDE ANY OTHER INFORMATION EXCEPT THIS!
    """
    TIPS_ERRORS_MESSAGE = BASE_MESSAGE + """
    In the output provide the TIPS/SUGGESTIONS FOR IMPROVEMENT and SPELLING/GRAMMAR ERRORS (IF ANY) in the format:
    - TIPS/SUGGESTIONS FOR IMPROVEMENT
    - SPELLING/GRAMMAR ERRORS
    DO NOT PROVIDE ANY OTHER INFORMATION EXCEPT THIS!
    """
    OVERALL_SCORE_MESSAGE = BASE_MESSAGE + """
    In the output provide the OVERALL_SCORE in the format:
    - SCORE (X/10)
    DO NOT PROVIDE ANY OTHER INFORMATION EXCEPT THIS!
    """
    OVERALL_SUMMARY_MESSAGE = BASE_MESSAGE + """
    In the output provide the OVERALL_SUMMARY in the format:
    - SUMMARY
    DO NOT PROVIDE ANY OTHER INFORMATION EXCEPT THIS!
    """
    COMMUNICATION_SCORE_MESSAGE = BASE_MESSAGE + """
    In the output provide the COMMUNICATION_SCORE in the format:
    - SCORE (X/10)
    DO NOT PROVIDE ANY OTHER INFORMATION EXCEPT THIS!
    """
    COMMUNICATION_SUMMARY_MESSAGE = BASE_MESSAGE + """
    In the output provide the COMMUNICATION_SUMMARY in the format:
    - SUMMARY
    DO NOT PROVIDE ANY OTHER INFORMATION EXCEPT THIS!
    """
    SUMMARY_MESSAGE = """You are an expert Summary Generator. You will be provided with the content and summarize the the content without losing
    important things out of it. Provide the output in structured format containing the Headlines (if any) and then the respective sumary."""
    # SUMMARY_INSTRUCTIONS_MESSAGE = """"""
    # SUMMARY_EMAIL_MESSAGE = """"""
    # SUMMARY_CONTENT_MESSAGE = """"""


settings = Settings()
