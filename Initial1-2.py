#!/usr/bin/env python
# coding: utf-8

# In[155]:


from music21 import *
from music21 import converter, instrument
import random
import networkx as nx
import numpy as np

"""
Attempt 1.2 at Music Genertion based off Midi Input
Difference from Attempt 1.1 : How notes are chosen and generated
Author: Lauren Casey 2022
"""

# In[156]:

"""
Function: 
Random choice of next note/duration
"""
def chooseNext (chosen, T):
    edges=[]
    edgeAr = T.edges(chosen)    #all edges related to current node
    for e in edgeAr:
        edges.append(e[1])
        
    temp = np.random.choice(edges, size = 1)
    return temp[0]


# In[321]:

"""
Parameters: 
N - stream for note generation
D - stream for duration generation
arr - array of notes in original music
arr2 - array of durations in original music
option - whether we are generating a duration or a note
first - boolean, true if generating the first note/duration in the stream

Returns: 
Note/Duration
"""
def etude(N, D, arr,arr2, option, first):
    noteToReturn = None
    dur = None
    notechosen = None
    rest = False
        
    if first:
        dur = arr2[random.randint(0, len(arr2)-1)]   #if first duration of etude
        notechosen = arr[random.randint(0, len(arr)-1)]    #if first note of etude
    else:
        dur = chooseNext(dur, D)    #if not the first note of etude, choose next based off edges
        notechosen = chooseNext(notechosen, N)
    
    
    if notechosen == 'rest':
        rest = True
        
    if type(option) == type(5.0):      #if we're generating a note, make quarterlength default to 1
        if rest == False:
        #we are adding by note name
            noteToReturn = note.Note(name = notechosen, quarterLength = 1)
        else:
            noteToReturn = note.Rest(quarterLength = 1)
    elif type(option) == type(""):     #if were generating a duration, make note name chosen
        if rest == False:
            noteToReturn = note.Note(name = 'B', quarterLength = dur)
        else:
            noteToReturn = note.Rest(quarterLength = dur)
    else:
        if rest == False: 
            noteToReturn = note.Note(name = notechosen, quarterLength = dur)
        else:
            noteToReturn = note.Rest(quarterLength = dur)
        
    return noteToReturn


# In[322]:

"""
Parameters: 
horn - horn part of inputted midi music
noteName - array/stream of pitches
durations - array/stream of durations
outputN - stream to generate notes
outputD - stream to generate durations
outputND - stream to generate notes and durations
beatsToGen - length of music to generate

Returns: 
All generated music

Function: 
Appends chosen notes/durations to streams
"""
def generate(horn, noteName, durations, outputN, outputD, outputND, beatsToGen):
    i = 0
    outputN.append(etude(noteTree(horn), durationTree(horn), noteName, durations, 1, True))
    outputD.append(etude(noteTree(horn), durationTree(horn), noteName, durations, "", True))
    outputND.append(etude(noteTree(horn), durationTree(horn), noteName, durations, None, True))
    
    while i < beatsToGen:
            outputN.append(etude(noteTree(horn), durationTree(horn), noteName, durations, 1, False))
            i += 1
            
    i = 0
    while i < beatsToGen:
        dur = etude(noteTree(horn), durationTree(horn), noteName, durations, "", False)
        if(i == beatsToGen-1):
            if(i + dur.duration.quarterLength > beatsToGen):
                dur.duration.quarterLength = beatsToGen - i
        i += dur.duration.quarterLength
        
        outputD.append(dur)
        
    i = 0
    while i < beatsToGen: 
        durNote = etude(noteTree(horn), durationTree(horn), noteName, durations, None, False)
        if(i == beatsToGen-1):
            if(i+durNote.duration.quarterLength > beatsToGen):
                durNote.duration.quarterLength = beatsToGen - i
        
        i += durNote.duration.quarterLength         
                
        outputND.append(durNote)
    
    outputN.notesAndRests.show()
    outputD.notesAndRests.show()
    outputND.notesAndRests.show()


# In[323]:

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
            
        if previous != None and NG.has_edge(previous.name, e.name):
            weight = NG.get_edge_data(previous.name, e.name)["weight"]
            NG.remove_edge(previous.name, e.name)
            NG.add_weighted_edges_from([(previous.name, e.name, (weight+1))])
            
        elif previous != None:
            NG.add_weighted_edges_from([(previous.name, e.name, 1)])
        previous = e
        
    return NG  


# In[324]:

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


# In[325]:

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
def breakApart(numer,horn, D,N,ND):
    #breaks apart songs durations & pitches
    durations = []
    noteName = []
    
    for e in horn.iter().notesAndRests:
        if  not e.isRest:
            durations.append(e.duration.quarterLength)
            noteName.append(e.name)
    

#Can be called to generate specified etude type - uncomment which etude to generate
 
    beatsToGen = input("How many beats do you want to generate?: ")
    generate(horn, noteName, durations,D,N,ND, int(beatsToGen))


# In[326]:

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
  


# In[327]:

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
    D = makeStream(originalClef, originalKeySig, originalTimeSig, "Rhythm : Style Etude")
    N = makeStream(originalClef, originalKeySig, originalTimeSig, "Pitch : Style Etude")
    ND = makeStream(originalClef, originalKeySig, originalTimeSig, "Rhythm & Pitch : Style Etude")
    
    
#use horn part of chosen Bach song
    horn = testSong.parts[0].recurse()
    
    #Uncomment to print original
    #horn.show()
    
#grab time sig - this is for counting up to the correct number of beats in measure when producing etude
    numer = horn.recurse().getElementsByClass(meter.TimeSignature)[0].numerator
    denom = horn.recurse().getElementsByClass(meter.TimeSignature)[0].denominator
#generate new etude
    breakApart(numer,horn, D,N, ND) 


# In[328]:


songGrab()

