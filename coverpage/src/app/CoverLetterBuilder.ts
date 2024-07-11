interface User {
    name: string;
    email: string;
    phone: string;
    github: string;
    linkedin: string;
}

interface Job {
    companyName: string;
    role: string;
}

interface Application {
    bullets: string[];
}

export class CoverLetterBuilder {
    user: User;
    job: Job;
    application: Application;

    constructor(user: User, job: Job, application: Application) {
        this.user = user;
        this.job = job;
        this.application = application;
    }

    generateLaTeX(): string {
        return `
\\documentclass[letterpaper,12pt]{article}
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
\\usepackage{ulem}
\\usepackage[hidelinks]{hyperref}
\\usepackage{xcolor,soul,lipsum}
\\newcommand{\\myul}[2][black]{\\setulcolor{##1}\\ul{##2}\\setulcolor{black}}
\\usepackage[T1]{fontenc}
\\definecolor{darkblue}{RGB}{0,0,238}
\\hypersetup{colorlinks,breaklinks,linkcolor=darkblue,urlcolor=darkblue,anchorcolor=darkblue,citecolor=darkblue}
\\usepackage{setspace} % Add this package for line spacing control
\\setstretch{1.2} % Set line spacing to double
\\addtolength{\\oddsidemargin}{-0.25in}
\\addtolength{\\evensidemargin}{-0.25in}
\\addtolength{\\textwidth}{0.5in}
\\addtolength{\\topmargin}{-0.5in}
\\addtolength{\\textheight}{1.0in}
\\setlength{\\parindent}{0pt}

\\newcommand{\\greeting}{To whom it may concern,} % The greeting to use (e.g. "Dear")
\\newcommand{\\myname}{${this.user.name}} % Your name
\\newcommand{\\position}{${this.job.role}} % The position you are applying for
\\newcommand{\\closer}{Kind Regards} % The closer to use (e.g. "Kind Regards")
% Company information
\\newcommand{\\company}{${this.job.companyName}} % The company you are applying to

\\begin{document}

\\begin{center}
    \\textbf{\\Huge ${this.user.name}} \\\\ \\vspace{5pt} 
    \\small  ${this.user.phone} $|$ \\href{mailto:${this.user.email}}{ ${this.user.email}}  $|$
    \\href{https://${this.user.github}}{${this.user.github}} $|$ \\href{https://${this.user.linkedin}}{${this.user.linkedin}}
\\end{center} 

\\vspace{-12.5pt}

\\vspace{0.2in}

% Opening block
\\hfill\\today\\\\

\\company\\\\

\\vspace{-0.1in}\\greeting\\,\\\\

% Body
\\vspace{-0.1in}\\setlength\\parindent{24pt}
I am writing to express my interest in the \\position{} position at \\company. With a background in full-stack web development, I am confident in my ability to contribute effectively to your team. The following is a list of skills that I possess relevant to your job posting:
\\begin{itemize}[itemsep=0pt]
${this.application.bullets.map(bullet => `\\item ${bullet}`).join('\n')}
\\end{itemize}
\\vspace{0.15in}

Thank you for considering my application. I am enthusiastic about the possibility of joining \\company{} and contributing to its mission. I look forward to the opportunity to discuss how my skills and experiences align with the needs of your team.
% Closer
\\vspace{0.1in}
% \\vfill

\\begin{flushright}
\\closer,

\\myname
\\end{flushright}

\\end{document}
        `;
    }
}
