
# 🎓 Omni-AI Learning Assistant

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-v1.32%2B-ff4b4b.svg)
![LangChain](https://img.shields.io/badge/LangChain-LCEL-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**A next-generation, interactive AI tutor powered by Large Language Models and Modern LangChain.**

The **Omni-AI Learning Assistant** is a sophisticated educational tool designed to adapt to various learning styles and academic disciplines. Built with **Streamlit** for a responsive UI and **LangChain Expression Language (LCEL)** for robust orchestration, it offers a seamless, personalized learning experience.

---

## ✨ Key Features

### 🧠 Adaptive Domain Expertise

Specialized prompt engineering allows the assistant to switch roles instantly:

* **STEM Focus**: Optimized for **Physics**, **Mathematics**, and **Biology**, with built-in support for **LaTeX** formula rendering and chemical equation formatting.
* **Humanities Focus**: Deep knowledge base for **Literature** and **History**.

### 🎨 Customizable Pedagogical Styles

Users can control *how* they learn:

* **Concise**: Direct answers for quick reference.
* **Detailed**: Comprehensive explanations with real-world analogies and step-by-step breakdowns.
* **Socratic Method**: A guided inquiry mode where the AI asks leading questions to foster critical thinking rather than giving away the answer.

### ⚡ Modern User Experience

* **Real-time Streaming**: Implements typewriter-style streaming responses for low-latency interaction.
* **Context Awareness**: robust session management ensures the AI remembers the entire conversation history.
* **Creativity Control**: Adjustable "Temperature" slider to balance between scientific rigor (low temp) and creative exploration (high temp).
* **One-Click Reset**: Instantly clear context to switch subjects without interference.

---

## 🏗️ Technical Architecture

This project demonstrates a modern implementation of LLM applications, moving away from legacy chains to the **LCEL (LangChain Expression Language)** standard.

* **Frontend**: [Streamlit](https://streamlit.io/) (Pure Python UI).
* **Orchestration**: [LangChain](https://www.langchain.com/) (Runnables, Prompts, Output Parsers).
* **Memory Management**: `ChatMessageHistory` coupled with Streamlit's `session_state`.
* **Model Compatibility**: Supports OpenAI GPT-3.5/4 and compatible APIs (e.g., DeepSeek).

---

## 🚀 Quick Start

Follow these steps to set up the project locally.

### 1. Clone the Repository

```bash
git clone [https://github.com/YourUsername/Omni-AI-Learning-Assistant.git](https://github.com/YourUsername/Omni-AI-Learning-Assistant.git)
cd Omni-AI-Learning-Assistant
```


### 2. Set Up Virtual Environment

It is recommended to use a virtual environment.

**Bash**

```
# MacOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

**Bash**

```
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add your API key:

**Code snippet**

```markdown
# .env file
OPENAI_API_KEY=sk-your-api-key-here

# Optional: If using a non-OpenAI provider (e.g., DeepSeek)
OPENAI_BASE_URL=[https://api.deepseek.com](https://api.deepseek.com)
```

### 5. Run the Application

**Bash**

```
streamlit run app.py
```

---

## 📂 Project Structure

**Plaintext**

```markdown
Omni-AI-Learning-Assistant/
├── app.py               # Main application entry point (Streamlit + LCEL logic)
├── .env.example         # Template for environment variables
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## 📸 Demo Scenarios

* **Physics Scenario** :
* *Input* : "Calculate the kinetic energy of a 2kg object moving at 3m/s."
* *Style* : Concise.
* *Output* : Returns the calculation using proper LaTeX formatting (**$E_k = \frac{1}{2}mv^2$**).
* **History Scenario** :
* *Input* : "What were the causes of the Industrial Revolution?"
* *Style* : Socratic Method.
* *Output* : "What changes in agriculture do you think might have freed up a workforce to move to cities?" (Guides user to the answer).

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
