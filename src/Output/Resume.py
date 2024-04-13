from abc import abstractmethod
import logging
from typing import List, Tuple

def get_or_none(json, key):
    if key in json and json[key] is not None:
        return json[key]
    return None

def get_or_empty(json, key):
    if key in json and json[key] is not None:
        return json[key]
    return ""

def get_or_empty_arr(json, key):
    if key in json and json[key] is not None:
        return json[key]
    return []

class SingleRowList():
    @abstractmethod
    def getContent(self) -> List[Tuple[str, str]]:
        pass
    
    @abstractmethod
    def getHeader(self) -> str:
        pass

    def output(self):
        header = self.getHeader()
        content = self.getContent()
        if not content or content==[]:
            return ""
        return self.formatter.getResumeSingleSubheadingsSection(header, content)
        
class Achievements(SingleRowList):
    def __init__(self, achievements, formatter):
        self.achievements = achievements
        self.formatter = formatter

    def getContent(self) -> List[Tuple[str, str]]:
        content = []
        for item in self.achievements:
            title = get_or_empty(item, 'title')
            if (title == ""):
                continue
            date = get_or_empty(item, 'dates')
            content.append((title, date))
        return content

    def getHeader(self) -> str:
        return "Achievements"

class Certifications(SingleRowList):
    def __init__(self, certifications, formatter):
        self.certifications = certifications
        self.formatter = formatter

    def getContent(self) -> List[Tuple[str, str]]:
        content = []
        for item in self.certifications:
            title = get_or_empty(item, 'title')
            if (title == ""):
                continue
            date = get_or_empty(item, 'dates')
            content.append((title, date))
        return content

    def getHeader(self) -> str:
        return "Certifications"


class Skills:
    def __init__(self, skills, formatter):
        self.languages = get_or_empty_arr(skills, 'languages')
        self.frameworks = get_or_empty_arr(skills, 'frameworks')
        self.tools = get_or_empty_arr(skills, 'tools')
        self.formatter = formatter

    def output(self):
        if self.languages == [] and self.frameworks == [] and self.tools == []:
            return ""
        output = self.formatter.getSectionStart("Skills")
        output += self.formatter.getSkills(self.languages, self.frameworks, self.tools)
        return output
    
class Project:
    def __init__(self, projects, formatter):
        self.projects = projects
        self.formatter = formatter

    def output(self):
        if self.projects is None or self.projects == []:
            return ""
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
        if self.experience is None or self.experience == []:
            return ""
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
        if self.education is None or self.education == []:
            return ""
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
        self.name = get_or_empty(json, 'name')
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
        self.json = json
        try:
            self.header = Header(json['header'], formatter)
            self.education = Education(json['education'], formatter)
            self.experience = Experience(json['experience'], formatter)
            self.projects = Project(json['projects'], formatter)
            if 'awards-achievements' in json:
                self.achievements = Achievements(json['awards-achievements'], formatter)
            if 'certificates' in json:
                self.certifications = Certifications(json.get('certificates'), formatter)
                
            self.skills = Skills(json.get('skills'), formatter)
            self.formatter = formatter
        except KeyError as e:
            logging.error(f"Error parsing resume: {e} {json}")
            raise Exception(f"Error parsing resume: {e}")

    def output(self):
        try:
            output = self.formatter.getSetup()
            output += self.header.output()
            output += self.education.output()
            output += self.experience.output()
            output += self.projects.output()
            if hasattr(self, 'achievements'):
                output += self.achievements.output()
            if hasattr(self, 'certifications'):
                output += self.certifications.output()
            output += self.skills.output()
            output += self.formatter.getCleanup()
        except Exception as e:
            logging.error(f"Error formatting resume: {e}")
            raise Exception(f"Error formatting resume: {e}")

        return output

    