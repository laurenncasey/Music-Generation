# Music Generation Project

This project was conducted as part of research at the **University of Wisconsin–Eau Claire**.

## Overview

This code generates music that closely resembles a given input piece using predefined weight matrices. The goal is to create practice music that is stylistically similar to the original, aiding in music rehearsal and study.

## How It Works

The system uses data streams to log various musical attributes from the input—such as pitch, notes, durations, and their combinations. These streams are then analyzed and used to generate new music based on different strategies.

## File Descriptions

- **Initial**  
  Demonstrates how to extract and break apart features of the input music.

- **Initial1-1**  
  Notes are generated based on the probability of each stream occurring.

- **Initial1-2**  
  Notes are generated at random.

- **Initial1-3**  
  Notes are generated using a probability transition matrix for Note/Duration pairs and similarity metrics.

- **CercaEdit**  
  Builds upon previous methods with additional similarity metrics for more refined music generation.

---

Feel free to explore each version to understand how different generation techniques affect the output!
