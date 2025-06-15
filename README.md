# 📈 Financial Navigator App

Welcome to **Financial Navigator**, your intelligent companion for smarter investment and financial planning decisions! This Streamlit-powered application leverages advanced LLMs to provide insights into stock analysis and personalized Systematic Investment Plan (SIP) recommendations.

---

## ✨ **Experience the App Live!**

Ready to explore? Click the link below to launch the Financial Navigator directly in your browser:

[![Launch Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-deployed-app-url.streamlit.app/)

**⬆️ IMPORTANT:** Once your app is deployed on Streamlit Cloud, **replace `https://your-deployed-app-url.streamlit.app/` with your actual live app URL!**

---

## 🌟 **Features**

* **🤖 AI-Powered Stock Analysis Chatbot:** Get instant insights on various stocks. Ask about fundamental analysis, price predictions, buy/sell/hold recommendations, or sector-specific analysis.

* **💰 Personalized SIP Planner:** Receive tailored Systematic Investment Plan (SIP) recommendations. Input your financial goals and risk appetite to get a personalized plan.

* **✨ Multi-LLM Flexibility:** Choose your preferred AI powerhouse! The app supports various Large Language Model providers including **Gemini, OpenAI, Groq, HuggingFace, and Cohere**, giving you diverse analytical perspectives.

* **🎯 Intuitive & Responsive UI:** A clean, user-friendly interface built with Streamlit and custom CSS for a seamless experience across devices.

---

## 🛠️ **Technologies Used**

* [**Streamlit**](https://streamlit.io/): For building interactive web applications quickly with Python.

* [**LangChain**](https://www.langchain.com/): For orchestrating powerful LLM chains and agent interactions.

* **Python 3.x**: The core programming language.

* **Custom CSS**: For enhancing the visual appeal and layout.

---

## 🚀 **Getting Started (Run Locally)**

Follow these steps to set up and run the Financial Navigator app on your local machine.

1.  **Clone the Repository:**

    ```bash
    git clone [https://github.com/YourGitHubUsername/financial-navigator-app.git](https://github.com/YourGitHubUsername/financial-navigator-app.git)
    cd financial-navigator-app
    ```

    (Remember to replace `YourGitHubUsername` with your actual GitHub username.)

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**

    * **Windows:**

        ```bash
        .\venv\Scripts\activate
        ```

    * **macOS/Linux:**

        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Streamlit App:**

    ```bash
    streamlit run app.py
    ```

    Your app will open in your default web browser (usually at `http://localhost:8501`).

---

## ☁️ **Deployment (Streamlit Cloud)**

This app is designed for easy deployment on [Streamlit Cloud](https://share.streamlit.io/).

1.  Push your code to a **public** GitHub repository (which you've already done!).

2.  Go to [Streamlit Cloud](https://share.streamlit.io/).

3.  Click "New app", select your `financial-navigator-app` repository, choose the `main` branch, and set the "Main file path" to `app.py`.

4.  Click "Deploy!". Streamlit Cloud will handle the rest, including installing dependencies from `requirements.txt`.

---

## 🤝 **Contributing**

Contributions are welcome! If you have suggestions, bug reports, or want to add new features, please feel free to:

1.  Fork the repository.

2.  Create a new branch (`git checkout -b feature/your-feature-name`).

3.  Make your changes.

4.  Commit your changes (`git commit -m 'Add new feature X'`).

5.  Push to the branch (`git push origin feature/your-feature-name`).

6.  Open a Pull Request.

---
