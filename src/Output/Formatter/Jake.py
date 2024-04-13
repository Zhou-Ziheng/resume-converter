from typing import List, Tuple
from src.Output.Formatter.Utils import l


class JakesFormatter():
    def getSetup(self):
        return """%-------------------------
% Resume in Latex
% Author : Jake Gutierrez
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
\\usepackage[english]{babel}
\\usepackage{tabularx}
\\input{glyphtounicode}


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
  \\vspace{-4pt}\\scshape\\raggedright\\large
}{}{0em}{}[\\color{black}\\titlerule \\vspace{-5pt}]

% Ensure that generate pdf is machine readable/ATS parsable
\\pdfgentounicode=1

%-------------------------
% Custom commands
\\newcommand{\\resumeItem}[1]{
  \\item\\small{
    {#1 \\vspace{-2pt}}
  }
}

\\newcommand{\\resumeSubheading}[4]{
  \\vspace{-2pt}\\item
    \\begin{tabular*}{0.97\\textwidth}[t]{l@{\\extracolsep{\\fill}}r}
      \\textbf{#1} & #2 \\\\
      \\textit{\\small#3} & \\textit{\\small #4} \\\\
    \\end{tabular*}\\vspace{-7pt}
}


\\newcommand{\\resumeSingleSubheading}[2]{
  \\vspace{-2pt}\item
    \\begin{tabular*}{0.97\\textwidth}[t]{l@{\extracolsep{\\fill}}r}
      \\textbf{#1} & #2 \\\\
    \\end{tabular*}\\vspace{-7pt}
}

\\newcommand{\\resumeSubSubheading}[2]{
    \\item
    \\begin{tabular*}{0.97\\textwidth}{l@{\\extracolsep{\\fill}}r}
      \\textit{\\small#1} & \\textit{\\small #2} \\\\
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

    def getCleanup(self):
        return """\\end{document}\n"""
    
    def getHeaderStart(self):
        return "\\begin{center}\n"
    
    def getHeaderEnd(self):
        return "\\end{center}\n"
    
    def getHeader(self, name):
        return """\\textbf{\\Huge \\scshape %s} \\\\ \\vspace{1pt}
    """ % l(name)

         
    def getSubHeader(self, dict):
        arr=[]
        if 'number' in dict:
            arr.append((dict['number'], False, False))

        if 'email' in dict:
            arr.append((dict['email'], False, True))
        
        if 'linkedin' in dict:
            arr.append((dict['linkedin'], True, False))
        
        if 'github' in dict:
            arr.append((dict['github'], True, False))

        if len(arr) == 0:
            return ""
        text = ""

        for i in arr:
            if i[1]:
                text += " $|$ \\small \\href{%s}{\\underline{%s}}" % (l(i[0]), l(i[0]))
            elif i[2]:
                text += " $|$ \\small \\href{mailto:%s}{\\underline{%s}}" % (l(i[0]), l(i[0]))
            else:
                text += " $|$ \\small %s" % l(i[0])
        
        return text[4:] + "\n"

    def getSectionStart(self, section):
        return "\\section{%s}\n" % l(section)
    

    def singleEntryListStart(self):
        return "\\resumeSingleSubHeadingListStart\n"

    def entryListStart(self):
        return "\\resumeSubHeadingListStart\n"

    def entryListEnd(self):
        return "\\resumeSubHeadingListEnd\n"
    
    def entryListItem(self, item1, item2, item3, item4):
        return "\n\\resumeSubheading\n{%s}{%s}\n{%s}{%s}\n" % (l(item1), l(item2), l(item3), l(item4))
    
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
        text +="{\\textbf{%s}" % l(name)

        if len(tools) > 0:
            text += " $|$"
        text += " \\emph{"""

        text += "%s" % ", ".join(map(l, tools))

        text += "}}"
        text += "{%s}\n" % l(dates)

        return text
    
    def getSkills(self, languages, frameworks, tools):
        text =  """\\begin{itemize}[leftmargin=0.15in, label={}]
            \small{\item{
            """
        if len(languages) > 0:
            text += "{\\textbf{Languages}}{: %s} \\\\\n" % ", ".join(map(l, languages))
        
        if len(frameworks) > 0:
            text += "{\\textbf{Frameworks}}{: %s} \\\\\n" % ", ".join(map(l, frameworks))
        
        if len(tools) > 0:
            text += "{\\textbf{Tools}}{: %s} \n" % ", ".join(map(l, tools))

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









    


            



