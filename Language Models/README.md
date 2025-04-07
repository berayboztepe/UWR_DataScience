This information has been fetched from the university's system.

# Item description:

Language Models (LM) seems to be a rather technical concept – it is a probability distribution modeling sequences of symbols from a finite set. Nevertheless, due to, among other things, the great successes of contemporary (large) generative models (ChatGPT, DALLE, Copilot, ...), language models have recently become one of the most important topics related to technologies, with the absolutely dominant way of implementing language models in recent years being Transformer-type neural networks, which will also be the basic (though not the only) tool used in our subject.

We will deal with both the basic field in which LMs operate, i.e. natural language processing, and neural networks modeling other modalities (including images, music, sound), as well as multimodal systems.

An important thread of our lecture will also be examining the extent to which language models are/can become the basic “engine” of artificial intelligence – whether such traditional AI tasks as playing games, searching state spaces, reinforcement learning, solving problems, proving theorems can be solved (and to what extent) using language models.

The additional classes for the subject will be a combination of exercises and workshops. We are planning 5 exercise lists, four workshops and a mini-project instead of the last fifth and part of the fourth workshop list (each workshop is planned for two weeks). During the exercises, some tasks will require reading a fragment of a scientific publication (sometimes a popular summary/video summary will be enough). We will use Python, pytorch and the 🤗 Transformers library (huggingface transformers) among others. The mini-project will be a team project and will involve learning an average language model from scratch, or training a larger one - and we will work in multiple stages: first, each student and each instructor will be able to submit a project topic(s), after which the Democratic Grant Committee, consisting of students and instructors, will select a subset of projects to be implemented (and teams will be created for these projects, and teaching will be carried out at the Institute of Computer Science as needed and possible).

The subject assumes initial knowledge of issues related to neural networks and machine learning. Each student should have previously completed one (and preferably two) subjects from the set: Artificial Intelligence, Neural networks + X, Machine Learning, Data mining, Project: Deep Learning, Text mining, Project: conversational bots and answering questions, etc.

Detailed list of topics:
* Introduction to language modeling using neural networks
* Transformer network operation in variants: encoder only (BERT, …), encoder-decoder (T5, …) and decoder only (GPT-*, …)
* Pre-training and re-training models (including Reinforcement Learning with Human Feedback)
* Transfer learning and working with multilingual models
* Tokenization algorithms and their impact on model performance
* Introduction to Natural Language Processing (NLP)
* Classic NLP tasks solved with pre-trained models: sequence classification (e.g. hate speech detection), token classification (e.g. Named Entity Recognition, Part-of-Speech tagging), seq2seq task (machine translation, generative summarization)
* Probing technique and investigating what transformers learn
* Conversational bots and question answering (Reader+Retrieval model, Dense Passage Retrieval, Retrieval-Augmented Generation), methods of obtaining vector representation of a sentence, the problem of hallucinations
* Modeling images and sounds with transformers (e.g. Vision Transformer, wave2vec-2.0, and others)
* Multimodal models combining an image with a text description
* Issues of efficiency and compression of models (knowledge distillation, model quantization, weight pruning) Combining transformers with other tools (including Toolformer) Going beyond standard applications: transformers implementing strategies in board games (including OthelloGPT), modeling reinforcement learning with transformers, modeling computation
* Possibilities of large language models (Zero Shot Learning, Few Shot Learning, and others)
* Prompt engineering, methods of automatic prompt generation (Chain-of-Thoughts and related), algorithms evolutionary in creating prompts
* Variants of the attention mechanism and attempts to search for successors of the transformer (e.g. Linformer, Performer, Reformer, …)
* Strength of transformers/weakness of transformers (transformers as General Artificial Intelligence, limitations in modeling certain issues, formal-linguistic models of transformers (e.g. RASP), or "emerging abilities" of large models are something real or an illusion.

The final project presentation can be reached from [here](https://github.com/berayboztepe/UWR_DataScience/blob/main/Language%20Models/Project/Travel%20assistant.pptx)

The final project for this course can be reach from [here](https://github.com/AnujJhunjhunwala/TravelAssistant)
