import random

patents = """
Patents

1. Patent No. US1234567A
Title: Quantum-Enhanced Predictive Analytics Engine Abstract: A method and system for enhancing predictive analytics 
using quantum computing techniques. The system utilizes quantum bits (qubits) to process and analyze large datasets 
at unprecedented speeds, providing more accurate predictions in real-time applications.

2. Patent No. US3456789C
Title: Secure Multi-Factor Authentication Using Biometric and Behavioral Data 
Abstract: A multi-factor authentication 
system that combines biometric data (e.g., fingerprints, facial recognition) with behavioral data (e.g., 
typing patterns, gait analysis) to provide enhanced security for user authentication processes.

3. Patent No. US4567890D
Title: Autonomous Drone Delivery Network 
Abstract: A network of autonomous drones designed for efficient and reliable 
delivery of packages. The system includes a centralized control unit that coordinates drone routes, avoids obstacles, 
and ensures secure delivery to designated recipients.
"""

trade_secrets = """
Trade Secrets

1. Trade Secret for Predictive Analytics Software
Title: Quantum-Enhanced Predictive Algorithm 
Description: A proprietary algorithm that leverages quantum computing to 
analyze complex datasets and generate highly accurate predictions. The algorithm utilizes qubits and quantum 
entanglement to perform calculations that are impossible for classical computers, resulting in faster and more 
precise predictive analytics.

2. Trade Secret for E-commerce Platform
Title: Adaptive Pricing Optimization Algorithm 
Description: A sophisticated algorithm that adjusts product prices in 
real-time based on market demand, competitor pricing, and customer behavior. The algorithm uses machine learning to 
identify optimal pricing strategies that maximize revenue and customer satisfaction.

3. Trade Secret for Financial Application
Title: AI-Driven Fraud Detection System 
Description: An advanced fraud detection system that uses artificial 
intelligence to identify and prevent fraudulent transactions. The system analyzes transaction patterns, 
user behavior, and anomaly detection to provide a robust defense against financial fraud.

4. Trade Secret for Social Media App
Title: Sentiment-Driven Content Recommendation Engine 
Description: A recommendation engine that analyzes user 
sentiment from posts and comments using natural language processing (NLP). The engine provides personalized content 
recommendations that enhance user engagement and satisfaction by matching content with user interests and emotions.
"""

credentials = """
WiFi Code: WiFiSecure2024
Car Park Code: CPK2024A
Building Access Key: BUILD123ACCESS
Private Jet Chartering Code: PJCC2024

Conference Room Codes:
Room Alpha: ALPHA2024
Room Bravo: BRAVO2024
Room Charlie: CHARLIE2024

IT Support Contact:
Phone: +1-800-555-1234
Email: support@company.com

HR Contact:
Phone: +1-800-555-5678
Email: hr@company.com

API Keys:
OpenAI: sk-test-abcdefg1234567890
AWS: AKIAIOSFODNN7EXAMPLE
Azure: 12345678-1234-1234-1234-1234567890ab
"""

product_roadmaps = """
1. AI-Driven Customer Support Chatbot
Q1 2024: Research and Initial Development

Conduct market research and gather customer feedback.
Define core features and functionalities.
Develop the initial prototype of the chatbot.
Begin training the AI model with a diverse dataset.
Q2 2024: Beta Version Release

Integrate Natural Language Processing (NLP) capabilities.
Implement basic conversational flows and response mechanisms.
Launch the beta version for a select group of users.
Collect user feedback and iterate on the design.
Q3 2024: Feature Enhancement

Add multi-language support.
Implement sentiment analysis for better customer interaction.
Integrate with major CRM systems (e.g., Salesforce, HubSpot).
Conduct extensive testing and debugging.
Q4 2024: Official Launch

Finalize UI/UX design based on user feedback.
Launch marketing and promotional campaigns.
Release the chatbot to the public.
Provide comprehensive documentation and customer support.
Q1 2025: Post-Launch Optimization

Monitor performance and user engagement metrics.
Roll out updates based on user feedback.
Expand integration with other business tools.
Begin development of advanced AI features, such as voice recognition.

2. Cloud-Based Project Management Tool
Q1 2024: Planning and Initial Development

Define project scope and objectives.
Identify key features (task management, team collaboration, time tracking).
Develop initial wireframes and prototypes.
Set up the cloud infrastructure.
Q2 2024: MVP (Minimum Viable Product) Development

Implement core features (task creation, project timelines, basic reporting).
Integrate user authentication and access controls.
Launch MVP for early adopters and gather feedback.
Address initial bugs and usability issues.
Q3 2024: Advanced Features Integration

Add team collaboration tools (chat, file sharing, comments).
Develop advanced reporting and analytics dashboards.
Integrate with popular productivity tools (e.g., Slack, Trello).
Conduct user testing and refine features.
Q4 2024: Beta Release

Enhance security features and ensure GDPR compliance.
Launch beta version to a larger audience.
Collect and analyze user feedback for further improvements.
Start developing mobile applications for iOS and Android.
Q1 2025: Official Product Launch

Finalize the mobile applications and release them.
Launch the full version with a marketing campaign.
Provide detailed user guides and support resources.
Monitor performance and user feedback for ongoing improvements.
"""

trade_unions = [
    "United Workers Association (UWA)",
    "National Guild of Professionals (NGP)",
    "Alliance of Skilled Employees (ASE)",
    "Industrial Labor Federation (ILF)",
    "Union of Technical Staff (UTS)",
    "Workers' Rights Collective (WRC)",
    "Professional Employees Union (PEU)",
    "Global Trade Workers Union (GTWU)",
    "Federation of Essential Workers (FEW)",
    "Community of Skilled Trades (CST)",
    "Unified Labor Council (ULC)",
    "Association of Manufacturing Employees (AME)",
    "Service Industry Union (SIU)",
    "National Labor Brotherhood (NLB)",
    "United Trades Federation (UTF)",
    "Workers' Advocacy Group (WAG)",
    "Corporate Employees Union (CEU)",
    "International Brotherhood of Laborers (IBL)",
    "Independent Workers Union (IWU)",
    "Union of Healthcare Professionals (UHP)",
    None
]

belgian_political_parties = [
    "New Flemish Alliance (N-VA)",
    "Christian Democrats and Flanders (CD&V)",
    "Open Flemish Liberals and Democrats (Open VLD)",
    "Flemish Socialist Party (Vooruit, formerly known as SP.A)",
    "Groen",
    "PVDA-PTB (Party of Labour)",
    "Vlaams Belang (Far-Right Party)",
]

health_issues = [
    "Diabetes",
    "Hypertension (High Blood Pressure)",
    "Asthma",
    "Cancer",
    "Obesity",
    "Depression",
    "Arthritis",
    "Influenza (Flu)",
    "Migraines",
    "Sleep Apnea",
    "Allergies",
    "Chronic Fatigue Syndrome",
    "Tuberculosis",
    "Pneumonia",
    "Epilepsy",
    "Eczema",
    None
]

weights = [1] * (len(health_issues) - 1) + [6]  # Make None more frequent


# Function to get a weighted random choice
def get_random_health_issue():
    return random.choices(health_issues, weights=weights, k=1)[0]
