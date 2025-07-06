# 🧠 Personality Prediction System using Resume Parsing & Psychometric Inputs

This project is a desktop application that predicts an individual's personality type based on both structured inputs (like gender, age, psychometric traits) and unstructured data (resume content). It uses machine learning, resume parsing, and natural language processing to determine a personality category based on the Big Five model.

---

## 🎯 Key Features

- 📄 Resume parsing using `pyresparser` and `spaCy`
- 📊 ML model trained on a custom dataset (Logistic Regression with multinomial classification)
- 🧠 Predicts personality based on the Big Five traits:
  - Openness
  - Conscientiousness
  - Extraversion
  - Agreeableness
  - Neuroticism
- 💻 GUI built with `Tkinter`
- 📥 Allows users to input:
  - Name
  - Age
  - Gender
  - Big Five psychometric scale (1–10 each)
  - Resume file upload (.pdf / .docx)
- 📈 Custom-trained model using `training_dataset.csv`

