# 6.00 Problem Set 5
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

# TODO: NewsStory

class NewsStory(object):
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_subject(self):
        return self.subject
    def get_summary(self):
        return self.summary
    def get_link(self):
        return self.link
        
        

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# TODO: WordTrigger
class WordTrigger(Trigger):
    def __init__(self, word):
        self.word = word
    def is_word_in(self, text):
        updated = ""
        for index in range(len(text)):
            found = False
            for char in string.punctuation:
                if char == text[index]:
                    found = True
            if found == True:
                updated += " "
            else:
                updated += text[index]
        updated = updated.lower().split(' ')
        if self.word.lower() in updated:
            return True
        return False
# TODO: TitleTrigger
# TODO: SubjectTrigger
# TODO: SummaryTrigger

class TitleTrigger(WordTrigger):
    def __init__(self, word):
        self.word = word
    def getWord(self):
        return self.word
    def evaluate(self, story):
        if self.is_word_in(story.get_title()) == True:
            return True
        return False

class SubjectTrigger(WordTrigger):
    def __init__(self, word):
        self.word = word
    def getSubject(self):
        return self.word
    def evaluate(self, story):
        if self.is_word_in(story.get_subject()) == True:
            return True
        return False
class SummaryTrigger(WordTrigger):
    def __init__(self, word):
        self.word = word
    def getSummary(self):
        return self.word
    def evaluate(self, story):
        if self.is_word_in(story.get_summary()) == True:
            return True
        return False



# Composite Triggers
# Problems 6-8

# TODO: NotTrigger
# TODO: AndTrigger
# TODO: OrTrigger

class NotTrigger(Trigger):
    def __init__(self, other):
        self.other = other
    def evaluate(self, x):
        return not self.other.evaluate(x)
    def getTrigger(self):
        return self.other

class AndTrigger(Trigger):
    def __init__(self, other1, other2):
        self.other1 = other1
        self.other2 = other2
    def evaluate(self, x):
        if(self.other1.evaluate(x) and self.other2.evaluate(x)) == True:
           return True
        return False
    def getOther1(self):
        return self.other1
    def getOther2(self):
        return self.other2

class OrTrigger(Trigger):
    def __init__(self, other1, other2):
        self.other1 = other1
        self.other2 = other2
    def evaluate(self, x):
        if(self.other1.evaluate(x) or self.other2.evaluate(x)) == True:
           return True
        return False
    def getOther1(self):
        return self.other1
    def getOther2(self):
        return self.other2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase
    def evaluate(self, story):
        if self.phrase in story.get_subject() or self.phrase in story.get_title() or self.phrase in story.get_summary():
            return True
        return False
    def getPhrase(self):
        return self.phrase


            
    
           
            


# Phrase Trigger
# Question 9

# TODO: PhraseTrigger


#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder (we're just returning all the stories, with no filtering) 
    # Feel free to change this line!
    fired = []
    for trigger in triggerlist:
        for story in stories:
            if trigger.evaluate(story) == True:
                fired.append(story)
    return fired

#======================
# Part 4
# User-Specified Triggers
#======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    # TODO: Problem 11
    # 'lines' has a list of lines you need to parse
    # Build a set of triggers from it and
    # return the appropriate ones
    dic = {}
    triggers = []
    for line in lines:
        words = line.split(' ')
        definitions = []
        for index in range(len(words) - 1):
            definitions.append(words[index + 1])
        dic[words[0]] = definitions

    added = dic["ADD"]
    for trig in added:
        case = dic[trig][0]
        if case == "TITLE":
            titleTrigger = TitleTrigger(dic[trig][1])
            triggers.append(titleTrigger)
        if case == "SUMMARY":
            summaryTrigger = SummaryTrigger(dic[trig][1])
            triggers.append(summaryTrigger)
        if case == "PHRASE":
            phraseTrigger = PhraseTrigger(dic[trig][1])
            triggers.append(phraseTrigger)
        if case == "SUBJECT":
            subjectTrigger = SubjectTrigger(dic[trig][1])
            triggers.append(subjectTrigger)
        if case == "NOT":
            notTrigger = SubjectTrigger(dic[trig][1])
            triggers.append(notTrigger)
        if case == "AND":
            andTrigger = AndTrigger(dic[trig][1], dic[trig][2])
            triggers.append(andTrigger)
        if case == "OR":
            orTrigger = OrTrigger(dic[trig][1], dic[trig][2])
            triggers.append(orTrigger)
    print(triggers)
    return triggers
        
            
            
        
        
                    
                

            
            
    
    
import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    t1 = SubjectTrigger("Obama")
    t2 = SummaryTrigger("MIT")
    t3 = PhraseTrigger("Supreme Court")
    t4 = OrTrigger(t2, t3)
    triggerlist = [t1, t4]
    
    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line 
    triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

