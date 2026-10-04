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
