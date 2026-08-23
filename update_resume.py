import json
import re

def update_resume_from_json():
    print("1. Reading resume.json...")
    with open("resume.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    html_builder = []

    # 1. Education Section
    html_builder.append('<section>')
    html_builder.append('    <h2>Education</h2>')
    for edu in data.get("education", []):
        html_builder.append('    <div class="item">')
        html_builder.append('        <div class="item-header">')
        html_builder.append(f'            <span class="item-title">{edu.get("studyType", "")} in {edu.get("area", "")}</span>')
        html_builder.append(f'            <span class="item-meta">{edu.get("startDate", "")} - {edu.get("endDate", "")}</span>')
        html_builder.append('        </div>')
        html_builder.append(f'        <div class="item-subtitle">{edu.get("institution", "")}</div>')
        if edu.get("gpa"):
            achievements = " | ".join(edu.get("achievements", []))
            html_builder.append(f'        <div class="item-meta" style="margin-top: 0.3rem;">GPA: {edu.get("gpa")} | Achievements: {achievements}</div>')
        html_builder.append('    </div>')
    html_builder.append('</section>')

    # 2. Work Experience Section
    html_builder.append('<section>')
    html_builder.append('    <h2> Experience</h2>')
    for exp in data.get("experience", []):
        html_builder.append('    <div class="item" style="margin-top: 1.5rem;">')
        html_builder.append('        <div class="item-header">')
        html_builder.append(f'            <span class="item-title">{exp.get("position", "")}</span>')
        html_builder.append(f'            <span class="item-meta">{exp.get("startDate", "")} - {exp.get("endDate", "")}</span>')
        html_builder.append('        </div>')
        html_builder.append(f'        <div class="item-subtitle">{exp.get("company", "")} &bull; {exp.get("location", "")}</div>')
        if exp.get("highlights"):
            html_builder.append('        <ul>')
            for bullet in exp["highlights"]:
                html_builder.append(f'            <li>{bullet}</li>')
            html_builder.append('        </ul>')
        html_builder.append('    </div>')
    html_builder.append('</section>')

    # 3. Technical Skills Section
    html_builder.append('<section>')
    html_builder.append('    <h2>Technical Skills</h2>')
    html_builder.append('    <div class="skills-grid">')
    skills = data.get("skills", {})
    category_labels = {
        "languagesAndFrameworks": "Languages/Frameworks",
        "aiMl": "AI/ML Skills",
        "databasesAndCloudInfrastructure": "Databases/Cloud Infrastructure",
        "other": "Other Skills"
    }
    for key, val_list in skills.items():
        cat_name = category_labels.get(key, key.title())
        val_str = ", ".join(val_list)
        html_builder.append('        <div class="skill-category">')
        html_builder.append(f'            <h3>{cat_name}</h3>')
        html_builder.append(f'            <p>{val_str}</p>')
        html_builder.append('        </div>')
    html_builder.append('    </div>')
    html_builder.append('</section>')

    dynamic_html = "\n".join(html_builder)

    # 4. Inject into Resume.html using markers
    print("2. Injecting structured content into Resume.html...")
    with open("Resume.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    pattern = re.compile(r'(<!-- AUTO-GENERATED-RESUME-START -->)(.*?)(<!-- AUTO-GENERATED-RESUME-END -->)', re.DOTALL)

    if pattern.search(html_content):
        updated_html = pattern.sub(f'\\1\n{dynamic_html}\n\\3', html_content)
        with open("Resume.html", "w", encoding="utf-8") as f:
            f.write(updated_html)
        print("3. Resume.html successfully updated from JSON source!")
    else:
        print("Error: Automation markers not found in Resume.html")

if __name__ == "__main__":
    update_resume_from_json()