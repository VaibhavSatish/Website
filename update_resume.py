import pdfplumber
import json
import re

def parse_pdf_and_update():
    print("1. Reading vaibhav_satish.pdf...")
    full_text = ""
    with pdfplumber.open("vaibhav_satish.pdf") as pdf:
        for page in pdf.pages:
            # x_tolerance=1 forces the parser to recognize smaller gaps as spaces
            text = page.extract_text(x_tolerance=1, y_tolerance=3)
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
        
        # Detect Headers
        if "EDUCATION" in upper_line:
            current_section = "education"
            continue
        elif "WORK EXPERIENCE" in upper_line or "EXPERIENCE" in upper_line:
            current_section = "experience"
            continue
        elif "TECHNICAL SKILLS" in upper_line or "SKILLS" in upper_line:
            current_section = "skills"
            continue

        # Parse Data with Sentence Stitching
        if current_section == "education":
            resume_data["education"].append({"details": line})
            
        elif current_section == "experience":
            # If it starts with any common bullet character
            if line.startswith('•') or line.startswith('-') or line.startswith('*') or line.startswith('\u2022'):
                if current_item is None:
                    current_item = {"title": "Experience", "bullets": []}
                    resume_data["experience"].append(current_item)
                # Clean the bullet character and add as a new bullet
                current_item["bullets"].append(line.lstrip('•-* \u2022').strip())
            else:
                # LINE STITCHING LOGIC:
                # If we are already inside a list of bullets, this line is a continuation of the previous broken sentence!
                if current_item and len(current_item["bullets"]) > 0:
                    current_item["bullets"][-1] += " " + line
                # If we have no bullets yet, this line is part of the Job Title / Dates
                elif current_item:
                    current_item["title"] += " | " + line
                else:
                    current_item = {"title": line, "bullets": []}
                    resume_data["experience"].append(current_item)
                    
        elif current_section == "skills":
            if ":" in line:
                key, val = line.split(":", 1)
                resume_data["skills"][key.strip()] = val.strip()

    # Save structured JSON
    with open("resume.json", "w", encoding="utf-8") as f:
        json.dump(resume_data, f, indent=4)
    print("2. Successfully generated resume.json!")

    # 3. Generate dynamic HTML sections
    html_builder = []
    
    # Education
    html_builder.append('<section>')
    html_builder.append('    <h2>Education</h2>')
    for edu in resume_data["education"]:
        html_builder.append('    <div class="item">')
        html_builder.append(f'        <div class="item-title">{edu.get("details", "")}</div>')
        html_builder.append('    </div>')
    html_builder.append('</section>')

    # Experience
    html_builder.append('<section>')
    html_builder.append('    <h2>Work Experience</h2>')
    for exp in resume_data["experience"]:
        html_builder.append('    <div class="item" style="margin-top: 1.5rem;">')
        # We split by our added pipe "|" to style the title and date separately if needed
        parts = exp.get("title", "").split(" | ")
        main_title = parts[0]
        sub_title = " | ".join(parts[1:]) if len(parts) > 1 else ""
        
        html_builder.append('        <div class="item-header">')
        html_builder.append(f'            <span class="item-title">{main_title}</span>')
        html_builder.append(f'            <span class="item-meta">{sub_title}</span>')
        html_builder.append('        </div>')
        
        if exp.get("bullets"):
            html_builder.append('        <ul>')
            for bullet in exp["bullets"]:
                html_builder.append(f'            <li>{bullet}</li>')
            html_builder.append('        </ul>')
        html_builder.append('    </div>')
    html_builder.append('</section>')

    # Skills
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

    # 4. Inject into Resume.html
    with open("Resume.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    pattern = re.compile(r'(<!-- AUTO-GENERATED-RESUME-START -->)(.*?)(<!-- AUTO-GENERATED-RESUME-END -->)', re.DOTALL)

    if pattern.search(html_content):
        updated_html = pattern.sub(f'\\1\n{dynamic_html}\n\\3', html_content)
        with open("Resume.html", "w", encoding="utf-8") as f:
            f.write(updated_html)
        print("3. Resume.html successfully updated!")
    else:
        print("Error: Automation markers not found in Resume.html")

if __name__ == "__main__":
    parse_pdf_and_update()