# COMP 495 - Abstract Condenser

This repo contains the progression and deliverable files involved in building my final project.

The objective of this project is not only to demonstrate what I have learned through my Bachelor's in Computing and Information Systems, but also to prove that I have the capacity to step outside the confines of academia and explore topics that are relevant and practical to corporate use cases.

## Outline

This project is composed of **5** parts.

#### Research:

A major portion of this project consists of research. Specifically, the research involved in this project is composed of legal and ethical considerations which play a major role in directing this project. Initially, this project was oriented to be an Indeed web scraper that would scrape career requirements and monitor trends over time and in geographical locations. However, upon reviewing the robots.txt file of Indeed, it appears they do not allow web-scraping whatsoever (despite the numerous datasets found elsewhere). 

As such, I had to pivot my project towards a topic within legal guidelines. As someone who loves science and medicine, I ended up deciding on a project that utilizes NLP to condense Abstracts from trending research papers over the last 24 hours and host them on a website.

#### Deep Learning:

NLP would be utilized with the help from TensorFlow to create a many-to-one classification to determine which sentence belongs to a specific topic (Results, Conclusion, etc.). With the help of the following research papers, I was able to replicate a similar model:

[Neural Networks for Joint Sentence Classification in Medical Paper Abstracts](https://arxiv.org/pdf/1612.05251.pdf)

[PubMed 200k RCT](https://arxiv.org/pdf/1710.06071.pdf)

The authors of these papers graciously made their dataset publicly available which allowed me to skip the cumbersome task of collecting a large dataset that is already classified and begin processing it myself.

#### Database Management:


#### Front End Web Development


#### Back End Web Development


## Progress Report

* Jan 8:  Conducted research on how to use Python (as I am coming from Java)
* Jan 9:  Conducted research on Python libraries that would assist for creating my project
* Jan 10: Conducted research on TensorFlow
* Jan 11: Conducted research on NLP and various methods
* Jan 12: Conducted research on similar problems which can be adapted to my own project
* Jan 13: Developed [various TensorFlow models](https://github.com/SinclairK602/495_NLP/blob/main/Abstract_Condenser.ipynb) for testing
* Jan 14: Began fine-tuning my successful TensorFlow model and began writing documentation
