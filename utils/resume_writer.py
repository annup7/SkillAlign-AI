from fpdf import FPDF
import os

def generate_resume(user_name, user_skills, job_title, matched_skills, missing_skills):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"{user_name}'s Resume", ln=True, align='C')

    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Target Job Role: {job_title}", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt="Current Skills:", ln=True)
    pdf.multi_cell(0, 10, user_skills)

    pdf.ln(5)
    pdf.cell(200, 10, txt="Matched Skills with JD:", ln=True)
    pdf.multi_cell(0, 10, ", ".join(matched_skills) if matched_skills else "None")

    pdf.ln(5)
    pdf.cell(200, 10, txt="Skills to Improve (Skill Gap):", ln=True)
    pdf.multi_cell(0, 10, ", ".join(missing_skills) if missing_skills else "None")

    # Output
    output_path = "Optimized_Resume.pdf"
    pdf.output(output_path)
    return output_path
