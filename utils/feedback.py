"""
====================================================
MockMate AI - Answer Feedback Module
----------------------------------------------------
Evaluates interview answers and generates
dynamic feedback with a randomized phrasing pool.

Author : Maithily Bhatt
====================================================
"""

import re
import random

# ====================================================
# Positive Keywords
# ====================================================

POSITIVE_KEYWORDS = {
    "python", "flask", "sql", "database", "api", "oop", "object", "class",
    "function", "algorithm", "data", "machine", "learning", "artificial",
    "intelligence", "project", "team", "leadership", "problem", "solution",
    "experience", "development", "testing", "deployment", "git", "github",
    "html", "css", "javascript"
}

# ====================================================
# Helper Functions
# ====================================================

def count_words(answer):
    return len(answer.split())

def keyword_score(answer):
    words = re.findall(r"\w+", answer.lower())
    return sum(1 for word in words if word in POSITIVE_KEYWORDS)

# ====================================================
# Evaluate Answer (DYNAMIC PHRASINGS)
# ====================================================

def evaluate_answer(question, answer):
    answer = answer.strip()

    if not answer:
        return {
            "score": 0,
            "feedback": "No answer submitted.",
            "strengths": [],
            "improvements": ["Please provide a response before submitting."]
        }

    score = 0
    strengths = []
    improvements = []

    # -----------------------------------------
    # Word Count Analysis
    # -----------------------------------------
    words = count_words(answer)
    if words >= 80:
        score += 40
        strengths.append(random.choice([
            "Comprehensive and highly detailed explanation.",
            "Strong depth of coverage; provided plenty of context.",
            "Elaborate answer demonstrating robust articulation."
        ]))
    elif words >= 40:
        score += 30
        strengths.append(random.choice([
            "Good level of detail and structural clarity.",
            "Substantial explanation meeting standard depth.",
            "Solid delivery of clear core points."
        ]))
    elif words >= 20:
        score += 20
    else:
        score += 10
        improvements.append(random.choice([
            "Answer is a bit brief. Try adding examples or background.",
            "Consider expanding on your thought process to sound comprehensive.",
            "Elaborate further to give the interviewer more context."
        ]))

    # -----------------------------------------
    # Keyword & Technical Terminology
    # -----------------------------------------
    keyword_points = keyword_score(answer)
    score += min(keyword_points * 4, 30)

    if keyword_points >= 3:
        strengths.append(random.choice([
            "Successfully integrated relevant industry terminology.",
            "Demonstrated domain knowledge using core technical keywords.",
            "Good use of domain-specific concepts in context."
        ]))
    else:
        improvements.append(random.choice([
            "Incorporate more technical keywords related to the stack.",
            "Try utilizing precise framework terminology.",
            "Weave in foundational technical words to sound more seasoned."
        ]))

    # -----------------------------------------
    # Sentence Structure
    # -----------------------------------------
    if "." in answer:
        score += 10
        strengths.append("Logical sentence structure and readability.")
    else:
        improvements.append("Use complete, well-punctuated sentences.")

    # -----------------------------------------
    # Action Verbs / Confidence Metrics
    # -----------------------------------------
    confidence_words = [
        "implemented", "developed", "created", "designed", 
        "improved", "optimized", "built", "achieved", "managed"
    ]
    
    lower = answer.lower()
    found = sum(1 for word in confidence_words if word in lower)

    if found:
        score += min(found * 5, 20)
        strengths.append(random.choice([
            "Displays high ownership through impactful action verbs.",
            "Strong tone of execution and practical contribution.",
            "Conveys crisp confidence regarding project delivery."
        ]))
    else:
        improvements.append(random.choice([
            "Incorporate strong execution verbs (e.g., 'Optimized', 'Designed').",
            "Framing answers using active ownership words boosts credibility.",
            "Use metrics or direct verbs to state your explicit contributions."
        ]))

    # -----------------------------------------
    # Final Normalization & Feedback
    # -----------------------------------------
    if score > 100:
        score = 100

    if score >= 90:
        feedback = "🌟 Outstanding Answer"
    elif score >= 75:
        feedback = "🎉 Excellent Answer"
    elif score >= 60:
        feedback = "👍 Good Answer"
    elif score >= 40:
        feedback = "🙂 Average Answer"
    else:
        feedback = "📚 Needs Improvement"

    return {
        "score": score,
        "feedback": feedback,
        "strengths": list(set(strengths)),  # Clean unique variants
        "improvements": list(set(improvements))
    }