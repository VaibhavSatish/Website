import pdfplumber
import json
import re

def pdf_to_json(pdf_path="vaibhav_satish.pdf", output_json="resume.json"):
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    lines = [line.strip() for line in full_text.split('\n') if line.strip()]

    # Structure template
    resume_data = {
        "education": [],
        "experience": [],
        "skills": {}
    }

    current_section = None
    current_item = None

    for line in lines:
        upper_line = line.upper()
        
        # Detect sections based on your resume headings
        if "EDUCATION" in upper_line:
            current_section = "education"
            continue
        elif "WORK EXPERIENCE" in upper_line or "EXPERIENCE" in upper_line:
            current_section = "experience"
            continue
        elif "TECHNICAL SKILLS" in upper_line or "SKILLS" in upper_line:
            current_section = "skills"
            continue

        # Parse content based on active section
        if current_section == "education":
            resume_data["education"].append({"details": line})
        elif current_section == "experience":
            # Simple heuristic: bullet points vs titles
            if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                if current_item:
                    current_item["bullets"].append(line.lstrip('•-* ').strip())
            else:
                # New job entry title/subtitle mock
                current_item = {"title": line, "bullets": []}
                resume_data["experience"].append(current_item)
        elif current_section == "skills":
            # Store skill text categories
            if ":" in line:
                key, val = line.split(":", 1)
                resume_data["skills"][key.strip()] = val.strip()

    # Save to JSON file
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(resume_data, f, indent=4)
    
    print(f"Successfully converted PDF structure into {output_json}!")

if __name__ == "__main__":
    pdf_to_json()