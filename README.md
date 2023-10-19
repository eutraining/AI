

# EUTraining Test Evaluation using AI


## Introduction

EUTraining Test Evaluation using AI is an automated system designed to assess and evaluate online tests and exams. The project leverages artificial intelligence (AI) to streamline the evaluation process, making it more efficient, accurate, and scalable. 

## Features

- **Automated Evaluation**: The system uses AI algorithms to automatically evaluate and grade online tests and exams.

- **Efficiency**: Reduces the time and effort required for manual evaluation, allowing instructors to focus on other important tasks.

- **Scalability**: Capable of handling a large volume of test submissions, making it suitable for institutions with varying class sizes.

- **Accuracy**: AI-driven evaluation ensures consistent and accurate grading.


## Getting Started


### Clone the Repository

```bash
git clone https://github.com/axeomxyz/ax16-eutraining.git
cd your-repo
```
### Create and Activate a Virtual Environment
On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
On macOS and Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
## Install Requirements
Use the package manager [pip](https://pip.pypa.io/en/stable/installation/) to install.
```bash
pip install -r requirements.txt
```

## Usage
- ### Data Analysis
Extract Case Study, Review Guide and Evaluation Files Details and update the SQLite DataBase.
```bash
python3 -m data_analysis.main 
```

- ### OpenAI Training
1. Generate Training Files for Fine-tuning Clubbed Method with Summary inclusion parameter.
```bash
python3 -m openai_training.main clubbed -i YES/NO
```

2. Generate Training Files for Fine-tuning Singleton Method with Summary inclusion parameter.
```bash
python3 -m openai_training.main singleton -i YES/NO
```

3. Fine-tuning the OpenAI model for clubbed method with Summary inclusion.
```bash
python3 -m openai_training.main clubbed_finetune -i YES/NO
```

4. Fine-tuning the OpenAI model for clubbed method with Summary inclusion.
```bash
python3 -m openai_training.main singleton_finetune -i YES/NO
```

5. Generate Train/Test Files in CSV format for training and validation purpose.
```bash
python3 -m openai_training.main train_test -i YES/NO
```

- ### Evaluation Files
1. Evaluate the dataset using Clubbed Method with Summary inclusion parameter.
```bash
python3 -m evaluation_files.main clubbed -i YES/NO
```

2. Evaluate the dataset using Singleton Method with Summary inclusion parameter.
```bash
python3 -m evaluation_files.main singleton -i YES/NO
```