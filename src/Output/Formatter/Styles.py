from enum import Enum
import logging
import re


class Font(Enum):
    FIRA_SANS = "FiraSans"
    ROBOTO = "roboto"
    NOTO_SANS = "noto-sans"
    DEFAULT = "default"


class Color:
    def __init__(self, color: str = "#000000"):
        if not isinstance(color, str) or not re.match(
            r"^#(?:[0-9a-fA-F]{3}){1,2}$", color
        ):
            logging.warning(f"Invalid color {color}, defaulting to black")
            color = "#000000"

        self.color = color

    def getRed(self):
        return int(self.color[1:3], 16)

    def getGreen(self):
        return int(self.color[3:5], 16)

    def getBlue(self):
        return int(self.color[5:7], 16)

    def getHex(self):
        return self.color[1:]

    def __str__(self):
        return self.color[1:]


class ResumeStyle:
    VALID_FONT_SIZES = {9, 10, 11, 12}

    def __init__(
        self,
        font: Font = Font.DEFAULT,
        font_size: int = 11,
        header_color: str = "#000000",
        subheader_color: str = "#000000",
        section_header_color: str = "#000000",
        date_color: str = "#000000",
        location_color: str = "#000000",
        entry_title_color: str = "#000000",
        company_color: str = "#000000",
        project_title_color: str = "#000000",
        project_tools_color: str = "#000000",
        skills_color: str = "#000000",
        bullet_color: str = "#000000",
        single_entry_color: str = "#000000",
    ):
        self.set_font(font)
        self.set_font_size(font_size)
        self.header_color = Color(header_color)
        self.subheader_color = Color(subheader_color)
        self.section_header_color = Color(section_header_color)
        self.date_color = Color(date_color)
        self.location_color = Color(location_color)
        self.entry_title_color = Color(entry_title_color)
        self.company_color = Color(company_color)
        self.project_title_color = Color(project_title_color)
        self.bullet_color = Color(bullet_color)
        self.project_tools_color = Color(project_tools_color)
        self.skills_color = Color(skills_color)
        self.single_entry_color = Color(single_entry_color)

    def set_font(self, font: Font):
        if not isinstance(font, Font):
            logging.warning(
                f"Invalid font {font}, defaulting to {Font.DEFAULT}. Valid fonts are {Font}"
            )
            font = Font.DEFAULT
        self.font = font

    def set_font_size(self, font_size: int):
        if not isinstance(font_size, int) or font_size not in self.VALID_FONT_SIZES:
            logging.warning(
                f"Invalid font size {font_size}, defaulting to 11. Valid font sizes are {self.VALID_FONT_SIZES}"
            )
            font_size = 11
        self.font_size = font_size
