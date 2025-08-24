def extract_skills_from_resume(file):
    resume_text = file.read().decode("utf-8", errors="ignore").lower()
    common_skills = [
        "python", "java", "sql", "html", "css", "javascript", "machine learning",
        "data analysis", "flask", "django", "pandas", "numpy", "react", "node.js",
        "deep learning", "communication", "problem solving", "teamwork"
    ]
    found_skills = [skill for skill in common_skills if skill in resume_text]
    return list(set(found_skills))
