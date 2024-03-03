import io
import json
from Convert.GoogleGeminiWrapper import GoogleGenimiWrapper
from Output.Resume import Resume
from Output.Formatter.Jake import JakesFormatter
from Parse.ParserController import ParserController;
import subprocess

file = open("../prototypes/test/CV.pdf", "rb")

def get_text(file):
    parsed = ParserController.get_one().parse(file)
    return parsed

def format_text_to_json(text):
    return GoogleGenimiWrapper.get_one().format_text(text)

def json_to_tex(json):
    return Resume(json, JakesFormatter()).output()

def compile_latex(latex_code):
    process = subprocess.Popen(['pdflatex', '-interaction', 'nonstopmode'],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

    stdout, stderr = process.communicate(latex_code.encode())
    if process.returncode == 0:
        return io.BytesIO(stdout), None
    else:
        return None, stderr.decode()


# text = get_text(file)
# json_resume = format_text_to_json(text)

json_resume = json.loads(open('test.json', 'r').read())
tex = json_to_tex(json_resume)

pdf = compile_latex(tex)


with open('output.tex', 'w') as file:
    # Write the string to the file
    file.write(tex)

with open('output.pdf', 'w') as file:
    # Write the string to the file
    file.write(pdf)
