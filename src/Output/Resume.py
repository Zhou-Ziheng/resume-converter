def get_or_none(json, key):
    if key in json:
        return json[key]
    return None

def get_or_empty(json, key):
    if key in json:
        return json[key]
    return ""

def get_or_empty_arr(json, key):
    if key in json:
        return json[key]
    return []

class Skills:
    def __init__(self, skills, formatter):
        self.languages = get_or_empty_arr(skills, 'languages')
        self.frameworks = get_or_empty_arr(skills, 'frameworks')
        self.tools = get_or_empty_arr(skills, 'tools')
        self.formatter = formatter

    def output(self):
        output = self.formatter.getSectionStart("Skills")
        output += self.formatter.getSkills(self.languages, self.frameworks, self.tools)
        return output
    
class Project:
    def __init__(self, projects, formatter):
        self.projects = projects
        self.formatter = formatter

    def output(self):
        output = self.formatter.getSectionStart("Projects")
        output += self.formatter.entryListStart()
        for item in self.projects:
            name = get_or_empty(item, 'name')
            dates = get_or_empty(item, 'dates')
            tools = get_or_empty(item, 'tools')
            output += self.formatter.getProjectEntryListItemStart(name, dates, tools)
            if 'description' in item:
                output += self.formatter.entryListDescription(item['description'])
        output += self.formatter.entryListEnd()
        return output

class Experience:
    def __init__(self, exprience, formatter):
        self.experience = exprience
        self.formatter = formatter
    
    def output(self):
        output = self.formatter.getSectionStart("Experience")
        output += self.formatter.entryListStart()
        for item in self.experience:
            title = get_or_empty(item, 'title')
            company = get_or_empty(item, 'company')
            location = get_or_empty(item, 'location')
            dates = get_or_empty(item, 'dates')
            output += self.formatter.entryListItem(title, dates, company, location)
            if 'description' in item:
                output += self.formatter.entryListDescription(item['description'])
        output += self.formatter.entryListEnd()
        return output

class Education:
    def __init__(self, education, formatter):
        self.education = education
        self.formatter = formatter

    def output(self):
        output = self.formatter.getSectionStart("Education")
        output+= self.formatter.entryListStart()
        
        for item in self.education:
            school = get_or_empty(item, 'school')
            degree = get_or_empty(item, 'degree')
            location = get_or_empty(item, 'location')
            grad_dates = get_or_empty(item, 'grad_dates')
            output += self.formatter.entryListItem(school, location, degree, grad_dates)
            if 'description' in item:
                output += self.formatter.entryListDescription(item['description'])

        output += self.formatter.entryListEnd()
        return output

class Header:
    def __init__(self, json, formatter):
        self.name = get_or_none(json, 'name')
        self.number = get_or_none(json, 'number')
        self.email = get_or_none(json, 'email')
        self.address = get_or_none(json, 'address')
        self.linkedin = get_or_none(json, 'linkedin')
        self.github = get_or_none(json, 'github')
        self.formatter = formatter

    def output(self):
        dict = {}
        if self.number is not None:
            dict['number'] = self.number
        if self.email is not None:
            dict['email'] = self.email
        if self.linkedin is not None:
            dict['linkedin'] = self.linkedin
        if self.github is not None:
            dict['github'] = self.github

        text = self.formatter.getHeaderStart()
        text += self.formatter.getHeader(self.name) 
        text += self.formatter.getSubHeader(dict)
        text += self.formatter.getHeaderEnd()
        return text


class Resume:
    def __init__(self, 
                 json, formatter):
        self.header = Header(json['header'], formatter)
        self.education = Education(json['education'], formatter)
        self.experience = Experience(json['experience'], formatter)
        self.projects = Project(json['projects'], formatter)
        self.skills = Skills(json['skills'], formatter)
        self.formatter = formatter

    def output(self):
        output = self.formatter.getSetup()
        output += self.header.output()
        output += self.education.output()
        output += self.experience.output()
        output += self.projects.output()
        output += self.skills.output()
        output += self.formatter.getCleanup()

        return output

    