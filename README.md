# MockMate
MockMate AI – An AI-powered mock interview platform that generates personalized interview questions from resumes, supports speech-to-text responses, provides NLP-based feedback, and helps students prepare for placement interviews.

________________________________________________________________________________________________________________________________________

# MockMate AI
Your Personal Placement Preparation Notebook.

MockMate AI is a comprehensive web-based platform designed to help students and job seekers streamline their placement preparation. It combines interactive learning, AI-powered mock interviews, and performance tracking into one unified, notebook-style interface.

________________________________________________________________________________________________________________________________________

## Key Features

*   **AI Mock Interviews**: Practice your interview skills with real-time analysis and feedback.
*   **Structured Learning Hubs**: Dedicated sections for:
    *   **Python** 
    *   **HTML** 
    *   **CSS** 
    *   **JavaScript** 
    *   **Data Structures & Algorithms (DSA)** 
*   **Interactive Flashcards**: Improve retention with built-in, flip-style flashcards for every topic.
*   **Preparation Dashboard**: Visualize your progress with dynamic bars and track your interview accuracy over time.
*   **Notebook Aesthetic**: A unique, clean, and engaging design that makes studying feel like working in a personal notebook.

________________________________________________________________________________________________________________________________________

## Tech Stack

*   **Backend**: Flask (Python)
*   **Frontend**: HTML5, CSS3, JavaScript
*   **AI Integration**: Google Generative AI
*   **Data Handling**: PDF parsing and interview history tracking

________________________________________________________________________________________________________________________________________

## How to Run Locally

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/Maithily04/MockMate.git](https://github.com/Maithily04/MockMate.git)
   cd MockMate
Create a virtual environment:
Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:
Bash
pip install -r requirements.txt
Run the application:
Bash
python app.py
Open http://127.0.0.1:5000 in your browser.
## Preview
(Feel free to add a screenshot of your dashboard here to make it more visually appealing!)
Built with ❤️ for better placements.

________________________________________________________________________________________________________________________________________

### How to add this to your GitHub:
1.  In your terminal, inside the `MockMate` folder, run: `touch README.md`
2.  Open the newly created `README.md` file in your code editor, paste the content above, and save it.
3.  Commit and push it to your repository:
    ```bash
    git add README.md
    git commit -m "Add readable README"
    git push origin main

 ________________________________________________________________________________________________________________________________________
 ## Project Structure

Understanding how the application is organized:

MockMate/
├── app.py                # Server logic & routes
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML files
│   ├── dashboard.html    # Main dashboard
│   ├── login.html        # Authentication
│   ├── interview.html    # Mock interview
│   ├── *_hub.html        # Subject hubs
│   └── *_flashcards.html # Learning tools
├── static/               # Assets
│   ├── css/              # Stylesheets
│   ├── js/               # Frontend logic
│   └── images/           # Backgrounds & icons
├── utils/                # Backend logic
│   ├── feedback.py       # AI feedback
│   ├── question_generator.py # Question logic
│   └── resume_parser.py  # PDF analysis
└── uploads/              # User resume storage

 ________________________________________________________________________________________________________________________________________

# Developer:
Name: Maithily Bhatt
B.Tech CSE student passionate about Web Development, Artificial Intelligence, and Software Engineering. Dedicated to creating innovative, user-friendly applications while continuously expanding technical skills and industry knowledge.

________________________________________________________________________________________________________________________________________
 

