import re
from typing import List, Tuple
from src.Output.Formatter.Styles import ResumeStyle
from src.Output.Formatter.Utils import l


class JakesFormatter:
    def __init__(self, styles: ResumeStyle):
        self.styles = styles

    def getSetup(self):
        setup = """%-------------------------
% Resume in Latex
% Thanks for using ATSify
% If the tool helped, consider donating a star at the GitHub repo
% https://github.com/Zhou-Ziheng/resume-converter
% Based off of: https://github.com/sb2nov/resume
% License : MIT
%------------------------

\\documentclass[letterpaper,11pt]{article}
\\usepackage[T1]{fontenc}
\\usepackage{lmodern}
\\usepackage{latexsym}
\\usepackage[empty]{fullpage}
\\usepackage{titlesec}
\\usepackage{marvosym}
\\usepackage[usenames,dvipsnames]{color}
\\usepackage{verbatim}
\\usepackage{enumitem}
\\usepackage[hidelinks]{hyperref}
\\usepackage{fancyhdr}
\\usepackage{fontawesome}
\\usepackage{xcolor,soul,lipsum}
\\usepackage[english]{babel}
\\usepackage{tabularx}
\\input{glyphtounicode}
% \\makeatletter
% \\def\\UTFviii@undefined@err#1{}
% \\makeatother
"""
        setup += "\\definecolor{header}{HTML}{%s}\n" % self.styles.header_color.getHex()
        setup += (
            "\\definecolor{subheaderColor}{HTML}{%s}\n"
            % self.styles.subheader_color.getHex()
        )
        setup += (
            "\\definecolor{sectionHeaderColor}{HTML}{%s}\n"
            % self.styles.section_header_color.getHex()
        )
        setup += (
            "\\definecolor{dateColor}{HTML}{%s}\n" % self.styles.date_color.getHex()
        )
        setup += (
            "\\definecolor{locationColor}{HTML}{%s}\n"
            % self.styles.location_color.getHex()
        )
        setup += (
            "\\definecolor{entryTitleColor}{HTML}{%s}\n"
            % self.styles.entry_title_color.getHex()
        )
        setup += (
            "\\definecolor{companyColor}{HTML}{%s}\n"
            % self.styles.company_color.getHex()
        )
        setup += (
            "\\definecolor{projectTitleColor}{HTML}{%s}\n"
            % self.styles.project_title_color.getHex()
        )
        setup += (
            "\\definecolor{bulletColor}{HTML}{%s}\n" % self.styles.bullet_color.getHex()
        )

        setup += (
            "\\definecolor{projectToolsColor}{HTML}{%s}\n"
            % self.styles.project_tools_color.getHex()
        )
        setup += (
            "\\definecolor{skillsColor}{HTML}{%s}\n" % self.styles.skills_color.getHex()
        )

        setup += (
            "\\definecolor{singleEntryColor}{HTML}{%s}\n"
            % self.styles.single_entry_color.getHex()
        )

        setup += """
        %----------FONT OPTIONS----------
% sans-serif
% \\usepackage[sfdefault]{FiraSans}
% \\usepackage[sfdefault]{roboto}
% \\usepackage[sfdefault]{noto-sans}
% \\usepackage[default]{sourcesanspro}

% serif
% \\usepackage{CormorantGaramond}
% \\usepackage{charter}


\\pagestyle{fancy}
\\fancyhf{} % clear all header and footer fields
\\fancyfoot{}
\\renewcommand{\\headrulewidth}{0pt}
\\renewcommand{\\footrulewidth}{0pt}

% Adjust margins
\\addtolength{\\oddsidemargin}{-0.5in}
\\addtolength{\\evensidemargin}{-0.5in}
\\addtolength{\\textwidth}{1in}
\\addtolength{\\topmargin}{-.5in}
\\addtolength{\\textheight}{1.0in}

\\urlstyle{same}

\\raggedbottom
\\raggedright
\\setlength{\\tabcolsep}{0in}

% Sections formatting
\\titleformat{\\section}{
  \color{sectionHeaderColor}\\vspace{-4pt}\\scshape\\raggedright\\large
}{}{0em}{}[\\titlerule \\vspace{-5pt}]

% Ensure that generate pdf is machine readable/ATS parsable
\\pdfgentounicode=1

%-------------------------
% Custom commands
\\newcommand{\\resumeItem}[1]{
  \\item\\small{
    {\color{bulletColor}#1 \\vspace{-2pt}}
  }
}

\\newcommand{\\resumeSubheading}[4]{
  \\vspace{-2pt}\\item
    \\begin{tabular*}{0.97\\textwidth}[t]{l@{\\extracolsep{\\fill}}r}
      \color{entryTitleColor}\\textbf{#1} & \color{dateColor}#2 \\\\
      \color{companyColor}\\textit{\\small#3} & \color{locationColor}\\textit{\\small #4} \\\\
    \\end{tabular*}\\vspace{-7pt}
}


\\newcommand{\\resumeSingleSubheading}[2]{
  \\vspace{-2pt}\item
    \\begin{tabular*}{0.97\\textwidth}[t]{l@{\extracolsep{\\fill}}r}
      \color{singleEntryColor}#1 & \color{dateColor}#2 \\\\
    \\end{tabular*}\\vspace{-7pt}
}

\\newcommand{\\resumeSubSubheading}[2]{
    \\item
    \\begin{tabular*}{0.97\\textwidth}{l@{\\extracolsep{\\fill}}r}
      \color{sectionTitleColor}\\textit{\\small#1} & \\textit{\\small #2} \\\\
    \\end{tabular*}\\vspace{-7pt}
}

\\newcommand{\\resumeProjectHeading}[2]{
    \\item
    \\begin{tabular*}{0.97\\textwidth}{l@{\\extracolsep{\\fill}}r}
      \\small#1 & #2 \\\\
    \\end{tabular*}\\vspace{-7pt}
}

\\newcommand{\\resumeSubItem}[1]{\\resumeItem{#1}\\vspace{-4pt}}

\\renewcommand\\labelitemii{$\\vcenter{\\hbox{\\tiny$\\bullet$}}$}

\\newcommand{\\resumeSingleSubHeadingListStart}{
\\begin{itemize}[leftmargin=0.15in, label={}]
\\setlength\\itemsep{-10pt} 
}

\\newcommand{\\resumeSubHeadingListStart}{\\begin{itemize}[leftmargin=0.15in, label={}]}
\\newcommand{\\resumeSubHeadingListEnd}{\\end{itemize}}
\\newcommand{\\resumeItemListStart}{\\begin{itemize}}
\\newcommand{\\resumeItemListEnd}{\\end{itemize}\\vspace{-5pt}}

%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%


\\begin{document}
"""

        return setup

    def getCleanup(self):
        return """\\end{document}\n"""

    def getHeaderStart(self):
        return "\\begin{center}\n"

    def getHeaderEnd(self):
        return "\\end{center}\n"

    def getHeader(self, name):
        return """\\textbf{\\Huge \color{header} \\scshape %s} \\\\ \\vspace{1pt}
    """ % l(
            name
        )

    def getSubHeader(self, dict):
        arr = []
        # (value, isLink, isEmail, linkName)
        if "number" in dict:
            stringNumber = dict["number"]
            # numbers = re.findall(r"\d+", stringNumber)
            # formatted_number = (
            #     f"+{numbers[0]} ({numbers[1]}) {numbers[2]} {numbers[3]}{numbers[4]}"
            # )
            arr.append((stringNumber, False, False))

        if "email" in dict:
            arr.append((dict["email"], False, True))

        if "linkedin" in dict:
            arr.append((dict["linkedin"], True, False, "\\faicon{linkedin} LinkedIn"))

        if "github" in dict:
            arr.append((dict["github"], True, False, "\\faicon{github} Github"))

        if len(arr) == 0:
            return ""
        text = ""

        for i in arr:
            if i[1]:
                text += " $|$ \\small \\href{%s}{%s}" % (l(i[0]), l(i[3]))
            elif i[2]:
                text += " $|$ \\small \\href{mailto:%s}{\\underline{%s}}" % (
                    l(i[0]),
                    l(i[0]),
                )
            else:
                text += " $|$ \\small %s" % l(i[0])
        return "\color{subheaderColor}" + text[4:] + "\n"

    def getSectionStart(self, section):
        return "\\section{%s}\n" % l(section)

    def singleEntryListStart(self):
        return "\\resumeSingleSubHeadingListStart\n"

    def entryListStart(self):
        return "\\resumeSubHeadingListStart\n"

    def entryListEnd(self):
        return "\\resumeSubHeadingListEnd\n"

    def entryListItem(self, item1, item2, item3, item4):
        return "\n\\resumeSubheading\n{%s}{%s}\n{%s}{%s}\n" % (
            l(item1),
            l(item2),
            l(item3),
            l(item4),
        )

    def entryListDescription(self, descriptions):
        if len(descriptions) == 0:
            return ""
        text = """\\resumeItemListStart
            """
        for desc in descriptions:
            text += "\\resumeItem{%s}\n" % l(desc)
        text += "\\resumeItemListEnd\n"
        return text

    def getProjectEntryListItemStart(self, name, dates, tools):
        text = "\\resumeProjectHeading\n"
        text += "{\color{projectToolsColor}{\color{projectTitleColor}\\textbf{%s}}" % l(
            name
        )

        if len(tools) > 0:
            text += " $|$"
        text += " \\emph{" ""

        text += "%s" % ", ".join(map(l, tools))

        text += "}}"
        text += "{%s}\n" % l(dates)

        return text

    def getSkills(self, languages, frameworks, tools):
        text = """\\begin{itemize}[leftmargin=0.15in, label={}]
            \small{\item{
            """
        if len(languages) > 0:
            text += "\color{skillsColor}{\\textbf{Languages}}{: %s} \\\\\n" % ", ".join(
                map(l, languages)
            )

        if len(frameworks) > 0:
            text += (
                "\color{skillsColor}{\\textbf{Frameworks}}{: %s} \\\\\n"
                % ", ".join(map(l, frameworks))
            )

        if len(tools) > 0:
            text += "{\color{skillsColor}\\textbf{Tools}}{: %s} \n" % ", ".join(
                map(l, tools)
            )

        text += """}}
        \\end{itemize}
        """
        return text

    def getResumeSingleSubheadings(self, items: List[Tuple[str, str]]):
        text = ""
        for item in items:
            text += "\\resumeSingleSubheading{%s}{%s}\n" % (l(item[0]), l(item[1]))
        return text

    def getResumeSingleSubheadingsSection(self, section, items):
        text = self.getSectionStart(section)
        text += self.singleEntryListStart()
        text += self.getResumeSingleSubheadings(items)
        text += self.entryListEnd()
        return text
