#!/usr/bin/env python
# coding: utf-8

# In[49]:


from music21 import *
from music21 import converter, instrument
import random
import networkx as nx


# In[ ]:
"""
Initial Attempt at Music Generation based off Midi Input
Author: Lauren Casey 2022

"""





# In[50]:

"""
Parameters: 
numer - numerator in time signature of inputted music
output - stream to append notes to, to generate song
noteName - array of note pitches to use in generated song
durations - array of durations to use in generated song

Returns:
ouput.notesAndRests.show() - stream of generated pitches and durations as a song
"""

#Randomly chooses next duration of note from array of available note/durations in original song
def generatePitchAndDurationEtude(numer, output, noteName, durations):
    
    measures = 0
    while measures < 21:
        beats = 0
        while beats < numer:
            
            durationIndex = random.randint(0, len(durations)-1)
            chosenDuration = durations[durationIndex]
            noteIndex = random.randint(0, len(noteName)-1)
            chosenNote = noteName[noteIndex]
            
            if(beats + chosenDuration > numer):
                chosenDuration = numer - beats
                
            beats += chosenDuration
            addNote = note.Note(name = chosenNote, quarterLength = chosenDuration)
            output.append(addNote)
        measures+=1
        
#Uncomment if you want to print this music out

    #output.notesAndRests.show()


# In[51]:

"""
Parameters: 
numer - numerator in time signature of inputted music
output - stream to append notes to, to generate song
durations - array of durations to use in generated song

Returns:
ouput.notesAndRests.show() - stream of generated durations as a song
"""
#Randomly chooses next duration of note from array of available durations in original song
def generateDurationEtude(numer, output, durations): 
    measures = 0
    while measures < 21:
        beats = 0
        while beats < numer:
            
            #generate duration etude
            durationIndex = random.randint(0, len(durations)-1)
            chosenDuration = durations[durationIndex]
            if (beats + chosenDuration > numer):
                chosenDuration = numer - beats
                
            beats += chosenDuration
            addNote = note.Note(quarterLength = chosenDuration)
            output.append(addNote)
        measures+=1
        
        
#Uncomment if you want to print this music out

    #output.notesAndRests.show()


# In[52]:

"""
Parameters: 
numer - numerator in time signature of inputted music
output - stream to append notes to, to generate song
noteName - array of note pitches to use in generated song

Returns:
ouput.notesAndRests.show() - stream of generated pitches as a song
"""
#Randomly chooses next note from array of available notes in original song
def generateNoteEtude(numer, output, noteName):
    
    measures = 0
    while measures < 21:
        beats = 0
        while beats < numer:
            noteIndex = random.randint(0, len(noteName)-1)
            chosenNote = noteName[noteIndex]
            beats += 1
            addNote = note.Note(name = chosenNote, quarterLength = 1)
            output.append(addNote)
            
        measures+=1
        
#Uncomment if you want to print this music out

    #output.notesAndRests.show()


# In[53]:

"""
Parameters: 
horn - horn part of inputted music
numer - numerator in time signature of inputted music
output - stream to append notes to, to generate song
durations - array of durations to use in generated song

Returns:
ouput.notesAndRests.show() - stream of generated durations as a song
"""
#Randomly chooses next duration of note from array of available note/durations in original music - Based on Tree
def generateDurationFromTree(horn, numer, durations, output):
    DT = durationTree(horn)
    previousDur = None
    measures = 0
    while measures < 21:
        beats = 0
        while beats < numer:
            
            #generate duration etude
            durationIndex = random.randint(0, len(durations)-1)
            chosenDuration = durations[durationIndex]
            
            if previousDur == None:
                beats += chosenDuration
                addNote = note.Note(quarterLength = chosenDuration)
                output.append(addNote)
                
            
            if (previousDur != None) and (previousDur in DT.predecessors(chosenDuration)):
                if (beats + chosenDuration > numer):
                    chosenDuration = numer - beats
                
                beats += chosenDuration
                addNote = note.Note(quarterLength = chosenDuration)
                output.append(addNote)
                
            previousDur = chosenDuration
                
            
            
        measures+=1
        
#Uncomment if you want to print this music out
    #output.notesAndRests.show()
    


# In[54]:

"""
Parameters: 
horn - horn part of inputted music
numer - numerator in time signature of inputted music
output - stream to append notes to, to generate song
noteName - array of pitches to use in generated song

Returns:
ouput.notesAndRests.show() - stream of generated notes as a song
"""
#Randomly chooses next pitch from array of available note in original music - Based on Tree
def generateNotesFromTree(horn, numer, noteName, output):
    NT = noteTree(horn)
    prevNote = None
    measures = 0
    while measures < 21:
        beats = 0
        while beats < numer:
            
            noteIndex = random.randint(0, len(noteName)-1)
            chosenNote = noteName[noteIndex]
            
            if prevNote == None:
                beats += 1
                addNote = note.Note(name = chosenNote, quarterLength = 1)
                output.append(addNote)
                
                
            if (prevNote != None) and (prevNote in NT.predecessors(chosenNote)):
                beats += 1
                addNote = note.Note(name = chosenNote, quarterLength = 1)
                output.append(addNote)
                
            prevNote = chosenNote
            
        measures+=1
#Uncomment if you want to print this music out

    #output.notesAndRests.show()


# In[55]:

"""
Parameters: 
horn - horn part of inputted music
numer - numerator in time signature of inputted music
output - stream to append notes to, to generate song
durations - array of durations to use in generated song
noteName - array of notes to use in generated song

Returns:
ouput.notesAndRests.show() - stream of generated notes and durations as a song
"""
#Randomly chooses next duration of note from array of available note/durations in original music - Based on Tree
def generateNoteAndDurationFromTree(horn, numer, noteName, durations, output):
    DT = durationTree(horn)
    NT = noteTree(horn)
    prevNote = None
    prevDur = None
    measures = 0
    
    while measures < 21:
        beats = 0
        while beats < numer:
            
            durationIndex = random.randint(0, len(durations)-1)
            chosenDuration = durations[durationIndex]
            noteIndex = random.randint(0, len(noteName)-1)
            chosenNote = noteName[noteIndex]
            
            if(prevNote == None) and (prevDur == None):
                beats += chosenDuration
                addNote = note.Note(name = chosenNote, quarterLength = chosenDuration)
                output.append(addNote)
                
            if ((prevNote != None) and (prevDur != None) and (prevNote in NT.predecessors(chosenNote)) and (prevDur in DT.predecessors(chosenDuration))):
                if(beats + chosenDuration > numer):
                    chosenDuration = numer - beats
                
                beats += chosenDuration
                addNote = note.Note(name = chosenNote, quarterLength = chosenDuration)
                output.append(addNote)
                
            prevNote = chosenNote
            prevDur = chosenDuration
            
            
        measures+=1
        
#Uncomment if you want to print this music out

    #output.notesAndRests.show()


# In[56]:

"""
Parameters: 
clef - Clef of Generated Music
key - Key of Generated Music
time - Time of Generated Music
title - Title of Generated Music

Returns:
Stream
"""

#Creates a stream to append note/durations to, to create generated music
def makeStream(clef, key, time, title):
    name = stream.Stream()
    name.append(clef)
    name.append(key)
    name.append(time)
    name.insert(0, metadata.Metadata())
    name.metadata.title = title
    
    return name
  


# In[57]:

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
def breakApart(numer, output, pitchOutput,pdOutput, horn, treeDurations, treeNotes, treeND):
    #breaks apart songs durations & pitches
    durations = []
    noteName = []
    
    for e in horn.iter().notesAndRests:
        if  not e.isRest:
            durations.append(e.duration.quarterLength)
            noteName.append(e.name)
    

#Can be called to generate specified etude type - uncomment which etude to generate
#You will HAVE TO uncomment output (last line) in method being called as well


    #generateDurationEtude(numer, output, durations)
    #generateNoteEtude(numer, pitchOutput, noteName)
    #generatePitchAndDurationEtude(numer,pdOutput , noteName, durations)
    
    #generateDurationFromTree(horn, numer, durations, treeDurations)
    #generateNotesFromTree(horn, numer, noteName, treeNotes)
    #generateNoteAndDurationFromTree(horn, numer, noteName, durations, treeND)


# In[58]:

"""
Function: 
Takes in horn part of music and creates a tree of notes/pitches
"""
def noteTree(horn):
    NG = nx.DiGraph()
    previous = None
    for e in horn.iter().notesAndRests:
        if e.name not in NG:
            NG.add_node(e.name)
        if previous != None:
            NG.add_edge(previous.name, e.name)
        previous = e
    return NG   


# In[59]:

"""
Function: 
Takes in horn part of music and creates a tree of durations
"""
def durationTree(horn):
    DG = nx.DiGraph()
    previous = None
    for e in horn.iter().notesAndRests:
        if e.duration.quarterLength not in DG:
            DG.add_node(e.duration.quarterLength)
        if previous != None:
            DG.add_edge(previous.duration.quarterLength, e.duration.quarterLength)
        previous = e
    return DG   


# In[60]:

"""
Function: Gets the song inputted and breaks it apart for song generation
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
    output = makeStream(originalClef, originalKeySig, originalTimeSig, "Rhythm Etude")
    pitchOutput = makeStream(originalClef, originalKeySig, originalTimeSig, "Pitch Etude")
    pdOutput = makeStream(originalClef, originalKeySig, originalTimeSig, "Pitch & Rhythm Etude")
    treeD = makeStream(originalClef, originalKeySig, originalTimeSig, "Rhythm : Style Etude")
    treeP = makeStream(originalClef, originalKeySig, originalTimeSig, "Pitch : Style Etude")
    treeDP = makeStream(originalClef, originalKeySig, originalTimeSig, "Rhythm & Pitch : Style Etude")
    
    
#use horn part of chosen Bach song
    horn = testSong.parts[0].recurse()
    
#grab time sig - this is for counting up to the correct number of beats in measure when producing etude
    numer = horn.recurse().getElementsByClass(meter.TimeSignature)[0].numerator
    denom = horn.recurse().getElementsByClass(meter.TimeSignature)[0].denominator
    
#generate new etude
    breakApart(numer,output,pitchOutput,pdOutput, horn, treeD, treeP, treeDP) 
    
#separates notes into digraph by name
    noteTree(horn)
#separates rhythm into digraph by duration.quarterLength
    durationTree(horn)


# In[61]:

#Initiate Process
songGrab()
