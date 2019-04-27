"""informationExtracter.py: Extracts relevant information from syllabuses/schedules"""
"""Paper: https://www.cs.cmu.edu/~bishan/papers/joint_event_naacl16.pdf"""

__author__      = "Alberto Mejia"
__copyright__   = "Copyright 2019, GNU Affero General Public License"

# Perform standard imports
import spacy
nlp = spacy.load('en_core_web_sm')
import pdftotext
import os
import re
import subprocess
import pprint
from spacy import displacy

# class PDFSyllabusParser:
#     """"""
#     def __init__(syllabus):
#         self.syllabus = syllabus

# class EventExtractor:
#     """The following are adopted from the ACE definition for entities and events:

#     • Entity mention: An entity is an object or set
#     of objects in the world. An entity mention is
#     a reference to an entity in the form of a noun
#     phrase or a pronoun.

#     • Event trigger: the word or phrase that clearly
#     expresses its occurrence. Event triggers can be
#     verbs, nouns, and occasionally adjectives like
#     “dead” or “bankrupt”.

#     • Event argument: event arguments are entities
#     that fill specific roles in the event. They mainly
#     include participants (i.e., the entities that are involved in the event) and general event attributes
#     such as place and time, and some event-type specific attributes that have certain values (e.g.,
#     JOB-TITLE, CRIME)"""

#     def __init__(document):
#         self.rules = ['exam', 'quiz', 'homework', 'project', 'presentation']
#         pass


# class InfoExtractor:
#     def __init__():
#         pass


class SyllabusParser:
    """"""
    def __init__(self, syllabus):
        
#         with open(syllabus, "rb") as file:
#             self.pdf = pdftotext.PDF(file)
#         self.pdf = pdftotext.PDF(open(syllabus, 'rb'))
        self.syllabus = syllabus # Path to syllabus
        self.pages = {} #{Page: [Sentences]}
        #self.numPages = len(pdf)
    
    def parse(self, end = None):
        """
        Method for extracting text from pdf files
        Parameters: 
            file (PDF): pdf file
            end (0-n): Parse up to this page
        Returns: 
            text (String): extracted text of document line by line       
        """
        #if end is None: end = self.numPages
        pdf = pdftotext.PDF(open(self.syllabus, 'rb'))
        end = len(pdf)
        
        allText = []
        for i in range(end):
            sentences = []
            lines = []
            page = pdf[i].splitlines()
            for sentence in page:
                # Remove all extra spacing 
                lines.append(sentence.split())
                
            for line in lines:
                # Add appropriate spacing
                sentences.append(" ".join(line))
                allText.append(" ".join(line))
            self.pages[i] = sentences   
            
        return allText
    
    def getInstructorInfo(self):
        pdf = pdftotext.PDF(open(self.syllabus, 'rb'))
        # Instructor 
        pg1 = pdf[0]
        pass
    
    def addEventsPg(self, num):
        """
        TODO: Add support for quizzes, hw, etc. 
        """
        # Adds exam to date
        toAdd = {} #"{Event: Time}"
        exs = {'exam', 'Exam', 'Test', 'test'}
        pdf = pdftotext.PDF(open(self.syllabus, 'rb'))
        text = self.pages[num]
        aText = " ".join(self.pages[num])
        doc = nlp(aText)
        for sentence in text:
            doc = nlp(sentence)
            ents = [ent for ent in doc.ents]
            for ent in ents:
                if ent.label_ == 'DATE':
                    if 'Exam' in sentence:
                        # print(sentence)
                        # print(ents,"ents", "ENT:", ent)
                        toAdd[ent] = ('Exam', sentence)
                        # print(toAdd, "TO")
                    
        return toAdd

class extractInfo:
    @classmethod
    def professorName(cls, text):
        # Using __ to extract the professor's name from text 
        salutations = ["Prof.", "Prof", "Dr.", "Dr"]
        doc = nlp(u"{}".format(text))
        for ent in doc.ents:
            name = ent.text.split()
            if ent.label_ == "PERSON" and name[0] in salutations:
                return ent.text
            
    @classmethod
    def phoneNumbers(cls, text):
        phoneNbrs = []
        # Regex pattern to extract phone numbers from text 
        #pattern = r'\s*\({0,1}(\d{3})-*\s*\){0,1}\s*(\d{3})-*\s*(\d{4})\n{0,1}'
        pattern = r'\({0,1}(\d{3})-*\s*\){0,1}\s*(\d{3})-*\s*(\d{4})\n{0,1}'
        found = re.findall(pattern, text)
        for nbr in found:
            group1, group2, group3 = nbr
            phoneNbrs.append(" ".join([group1, group2, group3]))
        return phoneNbrs
            
    @classmethod
    def emailAddresses(cls, text):
        """
        Finds phone numbers of the form:
            111-111-1111, 111 111 1111, (111)111-1111, (111) 111-111, (111) 111 111
        """
        # Regex pattern to extract email addresses from text 
        pattern = r'[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+'
        return re.findall(pattern, str(text))
    
    @classmethod
    def exams(cls, text):
        #pattern = r"Exam\s*\:*[0-9]+"
        events = []
        pattern = r"Exam\s*[A-Za-z0-9_-]*$"
#         return re.findall(pattern, str(text))
        words = text.split()
        # print("Split", words)
        for word in words:
            x = re.findall(pattern, str(text))
            if len(x) > 0: events.append(x[0])
        return events

def expand_person_entities(doc):
    new_ents = []
    #print(doc)
    for ent in doc.ents:
        # print(ent.text)
        if ent.label_ == "PERSON" and ent.start != 0:
            prev_token = doc[ent.start - 1]
            if ent.start.text in ("Dr", "Dr.", "Mr", "Mr.", "Ms", "Ms.", "Mrs", "Mrs.","Prof", "Prof.", "Instructor:"):
                new_ent = Span(doc, ent.start - 1, ent.end, label=ent.label)
                new_ents.append(new_ent.text)
        else:
            new_ents.append(ent)
    doc.ents = new_ents
    return doc

# Add the component after the named entity recognizer
#nlp.add_pipe(expand_person_entities, after='ner')

def show_ents(doc):
    if doc.ents:
        for ent in doc.ents:
            print(ent.text+' - '+ent.label_+' - '+str(spacy.explain(ent.label_)))
    else:
        print('No named entities found.')

def get_ents(doc, entType = None):
    allEntities = []
    if doc.ents:
        for ent in doc.ents:
            if ent.label_ != entType and entType is not None:
                continue
            else:
                allEntities.append((ent.text, ent.label_+' - '+str(spacy.explain(ent.label_))))
        return allEntities
    else:
        return 'No named entities found.'

def cleanMe(html):
    soup = BeautifulSoup(html) 
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    # Split text into lines and remove the leading and trailing space on each 
    lines = (line.strip() for line in text.splitlines())
    # Seperate multi-headlines into a single line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Remove blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def run(file):
    #bio = "./Syllabuses/BIOL 1107 Fall 2016 Syllabus.pdf"
    mys = SyllabusParser(file)
    mys.parse()
    #print(mys.addEventsPg(1))
    return mys.addEventsPg(1)

# nlph = "Natural Language Processing with Watson.html"
# f = open(nlph, "r")
# f_lines = list(f)
# for line in f_lines:
#     line = BeautifulSoup(line)

# f = open(nlph, "r")
# x = cleanMe(f)


