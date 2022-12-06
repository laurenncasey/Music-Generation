#!/usr/bin/env python
# coding: utf-8

# In[1]:


from music21 import *
from music21 import converter, instrument
import random
import networkx as nx

"""
Attempt 1.0 at Music Generation based off Midi Input
Difference from Inital: Probability random choice of next note/duration
Author: Lauren Casey 2022
"""

# In[2]:

"""
Function: 
Random choice of next note/duration
"""
def chooseNext(prev, chosen, T):
    #need to assign next note
    randomProb = random.random()
    edgeAr = T.edges
    previSub = None
    previE = None
                    
    #for each edge
    for i in edgeAr:
        weightOfNow = T.get_edge_data(i[0], i[1])['weight']
        totalNumOfEdges = T.number_of_edges()
        currentW = weightOfNow/totalNumOfEdges
                        
    #if the probability that edge holds is the biggest - this is the edge we want
        subt = abs(randomProb - currentW)
        if(previSub != None) and (subt <= previSub) and (i[0] == prev):
            if(subt == previSub):
                #if probs are the same
                if(random.random() < .5):
                    previSub = subt
                    previE = i
            else:
                previE = i
                previSub = subt
                                    
                                    
        if(previSub == None):
            previE = i
            previSub = subt
#set the next duration to the second index of the chosen edge (next note played)
    chosen = previE[1]
    
    return chosen


# In[49]:

"""
Parameters: 
horn - horn part of inputted music
numer - numerator in time signature of inputted music
output - stream to append notes to, to generate song
durations - array of durations to use in generated song

Returns:
ouput.notesAndRests.show() - stream of generated durations as a song

Function: 
Randomly chooses next duration of note from array of available note/durations in original music - Based on Tree
"""

def generateNoteAndDurationFromTree(horn, numer, noteName, durations, output):
    DT = durationTree(horn)
    NT = noteTree(horn)
    prevNote = None
    prevDur = None
    measures = 0
    
    while measures < 21:
        beats = 0
        while beats < numer:
            
            
            if(prevNote == None) and (prevDur == None):
                durationIndex = random.randint(0, len(durations)-1)
                chosenDuration = durations[durationIndex]
                noteIndex = random.randint(0, len(noteName)-1)
                chosenNote = noteName[noteIndex]
                beats += chosenDuration
                addNote = note.Note(name = chosenNote, quarterLength = chosenDuration)
                output.append(addNote)
################################################################
            #select following note based on randomly selecting probability, and then chosing the weight that is closest to that
            if (prevDur != None) and (prevNote != None):
                #finishes off beats in measure
                if (beats + chosenDuration > numer):
                    chosenDuration = numer - beats
                else:
                    chosenDuration = chooseNext(prevDur, chosenDuration, DT)
                chosenNote = chooseNext(prevNote, chosenNote, NT)
                try:
                    addNote = note.Note(name = chosenNote, quarterLength = chosenDuration)
                except:
                    addNote = note.Rest(quarterLength = chosenDuration)
                beats += chosenDuration
                output.append(addNote)
                
            prevDur = chosenDuration
            prevNote = chosenNote
                
            
            
        measures+=1
    output.notesAndRests.show()


# In[50]:

"""
Parameters: 
horn - horn part of inputted music
numer - numerator in time signature of inputted music
output - stream to append notes to, to generate song
noteName - array of pitches to use in generated song

Returns:
ouput.notesAndRests.show() - stream of generated notes as a song

Function: 
Randomly chooses next pitch from array of available note in original music - Based on Tree
"""
def generateNotesFromTree(horn, numer, noteName, output):
    NT = noteTree(horn)
    prevNote = None
    measures = 0
    while measures < 21:
        beats = 0
        while beats < numer:
            
            
            if prevNote == None:
                noteIndex = random.randint(0, len(noteName)-1)
                chosenNote = noteName[noteIndex]
                beats += 1
                addNote = note.Note(name = chosenNote, quarterLength = 1)
                output.append(addNote)
################################################################
            #select following note based on randomly selecting probability, and then chosing the weight that is closest to that
            if (prevNote != None):
                chosenNote = chooseNext(prevNote, chosenNote, NT)
################################################################
                
                beats += 1
                addNote = note.Note(name = chosenNote, quarterLength = 1)
                output.append(addNote)
                
            prevNote = chosenNote
                
            
            
        measures+=1
    output.notesAndRests.show()
    


# In[51]:

"""
Parameters: 
horn - horn part of inputted music
numer - numerator in time signature of inputted music
output - stream to append notes to, to generate song
durations - array of durations to use in generated song
noteName - array of notes to use in generated song

Returns:
ouput.notesAndRests.show() - stream of generated notes and durations as a song

Function: 
Randomly chooses next duration of note from array of available note/durations in original music - Based on Tree
"""
def generateDurationFromTree(horn, numer, durations, output):
    DT = durationTree(horn)
    previousDur = None
    measures = 0
    while measures < 21:
        beats = 0
        while beats < numer:
            
            #select beginning note
            if previousDur == None:
                durationIndex = random.randint(0, len(durations)-1)
                chosenDuration = durations[durationIndex]
                beats += chosenDuration
                addNote = note.Note(quarterLength = chosenDuration)
                output.append(addNote)
################################################################
            #select following note based on randomly selecting probability, and then chosing the weight that is closest to that
            if (previousDur != None):
                #finishes off beats in measure
                if (beats + chosenDuration > numer):
                    chosenDuration = numer - beats
                else:
                    chosenDuration = chooseNext(previousDur, chosenDuration, DT)


################################################################
                    beats += chosenDuration
                    addNote = note.Note(quarterLength = chosenDuration)
                    output.append(addNote)
                
            previousDur = chosenDuration
                
            
            
        measures+=1
    output.notesAndRests.show()
    


# In[52]:

"""Function: 
Takes in horn part of music and creates a tree of notes/pitches
"""
def noteTree(horn):
    NG = nx.DiGraph()
    previous = None
    for e in horn.iter().notesAndRests:
        if e.name not in NG:
            NG.add_node(e.name)
            
        if previous != None and NG.has_edge(previous.name, e.name):
            weight = NG.get_edge_data(previous.name, e.name)["weight"]
            NG.remove_edge(previous.name, e.name)
            NG.add_weighted_edges_from([(previous.name, e.name, (weight+1))])
            
        elif previous != None:
            NG.add_weighted_edges_from([(previous.name, e.name, 1)])
        previous = e
        
    return NG   


# In[53]:

"""
Function: 
Takes in horn part of music and creates a tree of durations
"""
def durationTree(horn):
    DG = nx.DiGraph()
    durArray = []
    previous = None
    weight = 0
    for e in horn.iter().notesAndRests:
        if e.duration.quarterLength not in DG:
            DG.add_node(e.duration.quarterLength)
            
        if previous != None and DG.has_edge(previous.duration.quarterLength, e.duration.quarterLength):
            weight = DG.get_edge_data(previous.duration.quarterLength, e.duration.quarterLength)["weight"]
            DG.remove_edge(previous.duration.quarterLength, e.duration.quarterLength)
            DG.add_weighted_edges_from([(previous.duration.quarterLength, e.duration.quarterLength, (weight+1))])
            
        elif previous != None:
            DG.add_weighted_edges_from([(previous.duration.quarterLength, e.duration.quarterLength, 1)])
        previous = e
        
    return DG  


# In[54]:


"""
Parameters: 
numer - Numerator of Time signature of inputted music
output - stream to append note/durations to
pitchOutput - Stream of pitches
durations - stream of durations
pdOutput - stream of pitches and durations
horn - horn part of inputted music 
treeDurations - tree of durations
treeNotes - tree of pitches
treeND - tree of pitches and durations

Returns:
Generated Music

Function: 
Takes in a part (horn) from inputted music and breaks apart features
"""
def breakApart(numer,horn, treeDurations, treeNotes, treeND):
    #breaks apart songs durations & pitches
    durations = []
    noteName = []
    
    for e in horn.iter().notesAndRests:
        if  not e.isRest:
            durations.append(e.duration.quarterLength)
            noteName.append(e.name)
    

#Can be called to generate specified etude type - uncomment which etude to generate
 
    #generateDurationFromTree(horn, numer, durations, treeDurations)
    #generateNotesFromTree(horn, numer, noteName, treeNotes)
    generateNoteAndDurationFromTree(horn, numer, noteName, durations, treeND)


# In[55]:

"""
Parameters: 
clef - Clef of Generated Music
key - Key of Generated Music
time - Time of Generated Music
title - Title of Generated Music

Returns:
Stream

Function: 
Creates a stream to append note/durations to, to create generated music
"""
def makeStream(clef, key, time, title):
    name = stream.Stream()
    name.append(clef)
    name.append(key)
    name.append(time)
    name.insert(0, metadata.Metadata())
    name.metadata.title = title
    
    return name
  


# In[56]:

"""
Function:
Gets the song inputted and breaks it apart for song generation
"""
def songGrab():

#get Bach song
    chorals = corpus.search('bach', fileExtensions = 'xml')
    testSong = chorals[0].parse()
    
#grab time sig, key sig, and clef
    originalTimeSig = testSong.recurse().getElementsByClass(meter.TimeSignature)[0]
    originalKeySig = testSong.recurse().getElementsByClass(key.KeySignature)[0]
    originalClef = testSong.recurse().getElementsByClass(clef.Clef)[0]
    
#make some extra streams for etude output with the originals time sig, key sig, and clef
    treeD = makeStream(originalClef, originalKeySig, originalTimeSig, "Rhythm : Style Etude")
    treeP = makeStream(originalClef, originalKeySig, originalTimeSig, "Pitch : Style Etude")
    treeDP = makeStream(originalClef, originalKeySig, originalTimeSig, "Rhythm & Pitch : Style Etude")
    
    
#use horn part of chosen Bach song
    horn = testSong.parts[0].recurse()
    
    #Uncomment to print original
    #horn.show()
    
#grab time sig - this is for counting up to the correct number of beats in measure when producing etude
    numer = horn.recurse().getElementsByClass(meter.TimeSignature)[0].numerator
    denom = horn.recurse().getElementsByClass(meter.TimeSignature)[0].denominator
#generate new etude
    breakApart(numer,horn, treeD, treeP, treeDP) 
  


# In[58]:

"""Initiate Process"""
songGrab()


# In[ ]:




