import pdfplumber
import json
import re

def parse_pdf_and_update():
    print("1. Reading vaibhav_satish.pdf...")
    full_text = ""
    with pdfplumber.open("vaibhav_satish.pdf") as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    lines = [line.strip() for line in full_text.split('\n') if line.strip()]

    # 2. Structure into JSON format
    resume_data = {
        "education": [],
        "experience": [],
        "skills": {}
    }

    current_section = None
    current_item = None

    for line in lines:
        upper_line = line.upper()
        if "EDUCATION" in upper_line:
            current_section = "education"
            continue
        elif "WORK EXPERIENCE" in upper_line or "EXPERIENCE" in upper_line:
            current_section = "experience"
            continue
        elif "TECHNICAL SKILLS" in upper_line or "SKILLS" in upper_line:
            current_section = "skills"
            continue

        if current_section == "education":
            resume_data["education"].append({"details": line})
        elif current_section == "experience":
            if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                if current_item:
                    current_item["bullets"].append(line.lstrip('•-* ').strip())
            else:
                current_item = {"title": line, "bullets": []}
                resume_data["experience"].append(current_item)
        elif current_section == "skills":
            if ":" in line:
                key, val = line.split(":", 1)
                resume_data["skills"][key.strip()] = val.strip()

    # Save backup JSON
    with open("resume.json", "w", encoding="utf-8") as f:
        json.dump(resume_data, f, indent=4)
    print("2. Successfully generated resume.json!")

    # 3. Generate dynamic HTML sections from the parsed data
    html_builder = []
    
    # Education Section
    html_builder.append('<section>')
    html_builder.append('    <h2>Education</h2>')
    for edu in resume_data["education"]:
        html_builder.append('    <div class="item">')
        html_builder.append(f'        <div class="item-title">{edu.get("details", "")}</div>')
        html_builder.append('    </div>')
    html_builder.append('</section>')

    # Experience Section
    html_builder.append('<section>')
    html_builder.append('    <h2>Work Experience</h2>')
    for exp in resume_data["experience"]:
        html_builder.append('    <div class="item" style="margin-top: 1.5rem;">')
        html_builder.append(f'        <div class="item-title">{exp.get("title", "")}</div>')
        if exp.get("bullets"):
            html_builder.append('        <ul>')
            for bullet in exp["bullets"]:
                html_builder.append(f'            <li>{bullet}</li>')
            html_builder.append('        </ul>')
        html_builder.append('    </div>')
    html_builder.append('</section>')

    # Skills Section
    html_builder.append('<section>')
    html_builder.append('    <h2>Technical Skills</h2>')
    html_builder.append('    <div class="skills-grid">')
    for cat, val in resume_data["skills"].items():
        html_builder.append('        <div class="skill-category">')
        html_builder.append(f'            <h3>{cat}</h3>')
        html_builder.append(f'            <p>{val}</p>')
        html_builder.append('        </div>')
    html_builder.append('    </div>')
    html_builder.append('</section>')

    dynamic_html = "\n".join(html_builder)

    # 4. Inject into Resume.html using your markers
    with open("Resume.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    pattern = re.compile(r'(<!-- AUTO-GENERATED-RESUME-START -->)(.*?)(<!-- AUTO-GENERATED-RESUME-END -->)', re.DOTALL)

    if pattern.search(html_content):
        updated_html = pattern.sub(f'\\1\n{dynamic_html}\n\\3', html_content)
        with open("Resume.html", "w", encoding="utf-8") as f:
            f.write(updated_html)
        print("3. Resume.html successfully updated via automated pipeline!")
    else:
        print("Error: Automation markers not found in Resume.html")

if __name__ == "__main__":
    parse_pdf_and_update()