"""
====================================================
MockMate AI - Question Generator
----------------------------------------------------
Generates personalized interview questions
based on extracted resume skills.

Author : Maithily Bhatt
====================================================
"""

import random

# ====================================================
# Question Bank
# ====================================================

QUESTION_BANK = {

    "python": [
        "What are the key features of Python?",
        "Explain List and Tuple with examples.",
        "What is the difference between a List and a Dictionary?",
        "Explain Object-Oriented Programming in Python.",
        "What are decorators in Python?"
    ],

    "flask": [
        "What is Flask?",
        "Explain Flask routing.",
        "What is Jinja2?",
        "How do sessions work in Flask?",
        "How do you upload files using Flask?"
    ],

    "html": [
        "What is HTML?",
        "Difference between HTML4 and HTML5.",
        "Explain semantic HTML.",
        "What are forms in HTML?",
        "Difference between id and class?"
    ],

    "css": [
        "What is the CSS Box Model?",
        "Difference between Flexbox and Grid.",
        "Explain Position properties.",
        "What are Media Queries?",
        "Difference between relative and absolute positioning?"
    ],

    "javascript": [
        "What are closures in JavaScript?",
        "Difference between var, let and const.",
        "Explain Promises.",
        "What is Event Bubbling?",
        "Explain Async/Await."
    ],

    "sql": [
        "What is SQL?",
        "Difference between DELETE, DROP and TRUNCATE.",
        "Explain JOINs.",
        "What is Normalization?",
        "Difference between Primary Key and Foreign Key."
    ],

    "dbms": [
        "What is DBMS?",
        "Explain ACID properties.",
        "Difference between SQL and NoSQL.",
        "What is Indexing?",
        "Explain Transactions."
    ],

    "machine learning": [
        "What is Machine Learning?",
        "Difference between Supervised and Unsupervised Learning.",
        "Explain Overfitting.",
        "What is Cross Validation?",
        "Explain Confusion Matrix."
    ],

    "deep learning": [
        "What is Deep Learning?",
        "Difference between CNN and RNN.",
        "What is Backpropagation?",
        "Explain Activation Functions.",
        "What is Transfer Learning?"
    ],

    "opencv": [
        "What is OpenCV?",
        "How do you read an image using OpenCV?",
        "Explain image preprocessing.",
        "Difference between RGB and BGR.",
        "What is contour detection?"
    ],

    "numpy": [
        "What is NumPy?",
        "Difference between List and NumPy Array.",
        "Explain Broadcasting.",
        "What is Vectorization?",
        "How is NumPy faster than Python Lists?"
    ],

    "pandas": [
        "What is Pandas?",
        "Difference between Series and DataFrame.",
        "How do you handle missing values?",
        "Explain merge() and join().",
        "How do you read CSV files?"
    ],

    "git": [
        "What is Git?",
        "Difference between Git and GitHub.",
        "Explain git clone.",
        "Explain git pull and git push.",
        "What is branching?"
    ]
}


# ====================================================
# Default HR Questions
# ====================================================

DEFAULT_QUESTIONS = [
    "Tell me about yourself.",
    "Introduce your final year project.",
    "Why should we hire you?",
    "What are your strengths?",
    "What are your weaknesses?",
    "Describe a challenging project you worked on.",
    "Where do you see yourself in 5 years?",
    "Why do you want to join our company?",
    "Explain one project from your resume.",
    "Do you have any questions for us?"
]


# ====================================================
# Generate Questions (DYNAMIC & RANDOMIZED)
# ====================================================

def generate_questions(skills):
    """
    Generates interview questions dynamically by sampling 
    randomly from both HR and technical categories.

    Parameters
    ----------
    skills : list

    Returns
    -------
    list
    """
    final_questions = []

    # 1. Dynamically select 3 random HR questions instead of the exact same 5
    final_questions.extend(random.sample(DEFAULT_QUESTIONS, min(len(DEFAULT_QUESTIONS), 3)))

    # 2. Extract technical questions based on parsing
    tech_questions_pool = []
    
    if skills:
        for skill in skills:
            skill = skill.lower().strip()
            if skill in QUESTION_BANK:
                # Shuffle the pool for that specific skill to prevent sequential picking
                available_questions = QUESTION_BANK[skill]
                # Pick 2 or 3 random questions out of the array for this matched category
                sampled = random.sample(available_questions, min(len(available_questions), 2))
                tech_questions_pool.extend(sampled)

    # Shuffle the aggregated technical questions so they appear randomly mixed
    random.shuffle(tech_questions_pool)
    final_questions.extend(tech_questions_pool)

    # 3. Structural safety check if no skills were matched or extracted
    if len(final_questions) <= 3:
        # Fallback to appending extra randomized general questions
        remaining_hr = [q for q in DEFAULT_QUESTIONS if q not in final_questions]
        extra_questions = random.sample(remaining_hr, min(len(remaining_hr), 4))
        final_questions.extend(extra_questions)

    # 4. Filter duplicates while maintaining visual order structure
    unique_questions = []
    for question in final_questions:
        if question not in unique_questions:
            unique_questions.append(question)

    # Optional: Keep the complete deck size balanced (e.g., limit to top 7-8 total questions per session)
    return unique_questions[:8]


# ====================================================
# Demo
# ====================================================

if __name__ == "__main__":
    skills = [
        "Python",
        "Flask",
        "SQL",
        "HTML",
        "CSS"
    ]

    print("--- RUN 1 ---")
    for i, q in enumerate(generate_questions(skills), 1):
        print(f"{i}. {q}")
        
    print("\n--- RUN 2 (Same Skills, New Questions) ---")
    for i, q in enumerate(generate_questions(skills), 1):
        print(f"{i}. {q}")