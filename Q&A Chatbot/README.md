# Deep Learning Question & Answers Chatbot

An implementation of a Q&A Chatbot based on the following paper:
- Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, Rob Fergus,
  "End-To-End Memory Networks",
  https://arxiv.org/pdf/1503.08895.pdf

The chatbot can answer questions based on a "story" (one or more sentences for context). It currently returns a binary answer (yes or no). 

I hope (if I have time) to incoporate a NLG component so the chatbot could return answers outside of yes or no. I also hope to include a real time speech to text
component because why not haha. That way you'd actually be able to talk to the chatbot. 

A job posting really sparked my interest for this project, so I am trying to implement something related to their job description. 

## TODOs

  * Analyze results. 
  * Make own stories and questions and test model on that. 
  * Clean up notebook.
  * Look into other notes

## Other Notes
Some other todos for myself to extend the model.

Algo wants to build a Chatbot to allow business executive to talk to their data by asking natural English questions. They also expects their chatbot to understanding questions, and personalize the question prediction for each user according
to its question history.

I could extend the training and test set so the chat bot could answer questions more related to busines and data.

I will brain storm the rest after finishing some commitments. Its finals week :/
