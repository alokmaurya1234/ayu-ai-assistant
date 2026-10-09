## Ayu version 1.0

1. My first logical understanding how we can load the data from json file to main.py program.

this is my basic understanding about this concept.

STEPS

1 : we will check weather the file exixt or not
2 : load the file by using open() and their is read method which use for read the data from the josn file.
3 : what ever converstion we will have we will append those conversation into the jon file by using write method.
4 : when user ask aagin that question we will send that file along with the question to LLM. 
5: so it will return the answeer according to the context.

## First Blank-Sheet Win

I initially didn't know how to pass memory and conversation
together to the LLM.

I tried different approaches, got API errors, understood
that memory and conversation are different data structures,
and eventually created a context string using an f-string.

The important thing I learned:

I don't need to know the exact syntax immediately.
I need to understand the problem, break it down, and then
find the syntax required to implement my logic.

I can solve problems from a blank file.


## save memory.json 

Problem : how do i save python memory permanently?

Input:
A Python dictionary containing memory.

output:
Updated memory.json file.

step:
1. Create save_memory(memory).

2. Open memory.json in write mode.

3. Convert the Python memory dictionary into JSON.

4. Write the JSON data into memory.json.

5. Call save_memory() only when our application
   decides that a new memory should be stored.


## updating the memory 

Input:
    existing memory
    new important memory

Output:
    updated memory

steps 
1. if some covertion happend in  between the load and save memory we simply upadte the importent data into the file

## Jev
Jev is a decision model designed for structured decisions such as classification, yes/no judgments, routing, and scoring. It complements generative models rather than replacing them.


## rough idea about ayu v0.1

# Feature: Automatic Memory Detection

## Problem

Ayu currently has persistent memory, but new memories are manually defined.

## Goal

Automatically determine whether information from a conversation is worth storing as long-term memory.

## First decision

Is this information worth remembering?

## Input

Recent conversation

## Output

Yes / No

## Decision model

Jev

## Flow

Conversation
    ↓
Jev
    ↓
Worth remembering?
    ↓
Yes / No


## Feature: Memory Decision

### Function
should_remember()

### Input
conversation

### Output
yes/no

### Responsibility
Decide whether the conversation contains information
that is valuable enough to store as persistent user memory.

### If YES
Send the conversation to the memory extraction step.

### If NO
Continue the conversation without creating a memory.