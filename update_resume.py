import pdfplumber
import re

def parse_pdf_to_html(pdf_path):
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    lines = [line.strip() for line in full_text.split('\n') if line.strip()]
    
    html_output = []
    current_section = None
    
    # Simple dynamic parser mapping text lines to your HTML structure
    # You can customize this logic depending on how your PDF layout outputs text
    html_output.append('<section>')
    html_output.append('    <h2>Resume Content Extracted from PDF</h2>')
    html_output.append('    <div class="item">')
    html_output.append('        <ul>')
    
    for line in lines:
        # Check if line looks like a bullet point
        if line.startswith('•') or line.startswith('-') or line.startswith('*'):
            clean_bullet = line.lstrip('•-* ').strip()
            html_output.append(f'            <li>{clean_bullet}</li>')
        else:
            # Regular text lines
            html_output.append(f'            <!-- Text line: {line} -->')
            
    html_output.append('        </ul>')
    html_output.append('    </div>')
    html_output.append('</section>')
    
    return "\n".join(html_output)

def update_resume():
    print("Reading vaibhav_satish.pdf...")
    dynamic_content = parse_pdf_to_html("vaibhav_satish.pdf")

    # Read Resume.html
    with open("Resume.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    # Replace content between markers
    pattern = re.compile(r'(<!-- AUTO-GENERATED-RESUME-START -->)(.*?)(<!-- AUTO-GENERATED-RESUME-END -->)', re.DOTALL)

    if pattern.search(html_content):
        updated_html = pattern.sub(f'\\1\n{dynamic_content}\n\\3', html_content)
        with open("Resume.html", "w", encoding="utf-8") as f:
            f.write(updated_html)
        print("Resume.html successfully updated dynamically from PDF!")
    else:
        print("Error: Automation markers not found in Resume.html")

if __name__ == "__main__":
    update_resume()