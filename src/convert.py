import json
import logging

from src.Convert.GoogleGeminiWrapper import GoogleGenimiWrapper
from src.Output.Formatter.Styles import Color, Font, ResumeStyle
from src.Output.Resume import Resume
from src.Output.Formatter.Jake import JakesFormatter
from src.Parse.ParserController import ParserController
from latex import build_pdf
import re
from ddtrace import tracer


@tracer.wrap()
def get_text(file):
    parsed = ParserController.get_one().parse(file)
    filtered = re.sub(r"[^\x00-\x7f]", r"", parsed)
    return filtered


@tracer.wrap()
def format_text_to_json(text):
    return GoogleGenimiWrapper.get_one().format_text(text)


@tracer.wrap()
def json_to_tex(jsonData, style):
    logging.debug(f"json: {jsonData}")
    logging.debug(f"style: {style}")
    if style is None:
        style = ResumeStyle()
    else:
        styleData = json.loads(style)
        font = styleData.get("font")
        if font is None:
            styleData["font"] = Font.DEFAULT.value
        style = ResumeStyle(
            font_size=styleData.get("font_size"),
            font=Font(styleData.get("font")),
            header_color=styleData.get("header_color"),
            subheader_color=styleData.get("subheader_color"),
            section_header_color=styleData.get("section_header_color"),
            date_color=styleData.get("date_color"),
            location_color=styleData.get("location_color"),
            entry_title_color=styleData.get("entry_title_color"),
            company_color=styleData.get("company_color"),
            project_title_color=styleData.get("project_title_color"),
            bullet_color=styleData.get("bullet_color"),
            project_tools_color=styleData.get("project_tools_color"),
            skills_color=styleData.get("skills_color"),
            single_entry_color=styleData.get("single_entry_color"),
        )
    return Resume(jsonData, JakesFormatter(style)).output()


@tracer.wrap()
def compile_tex(tex_content):
    try:
        pdf = build_pdf(tex_content, builder="pdflatex")
    except Exception as e:
        logging.error(f"Error compiling tex: {e} {tex_content}")
        raise e

    return bytes(pdf)


def logTex(tex):
    with open("output.tex", "w") as f:
        f.write(tex)


def convert_resume_handler(file, style):
    text = get_text(file)
    json = format_text_to_json(text)
    tex = json_to_tex(json, style)
    pdf = compile_tex(tex)

    return tex.encode(), pdf
