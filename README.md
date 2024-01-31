# COMP 495 - Abstract Condenser

This repo contains the progression and deliverable files involved in building my final project.

The objective of this project is not only to demonstrate what I have learned through my Bachelor's in Computing and Information Systems, but also to prove that I have the capacity to step outside the confines of academia and explore topics that are relevant and practical to corporate use cases.

**Steps to run locally:**

First, you will need to install necessary packages:

* Python 3.9-3.11 (Anything higher will **NOT** work with TensorFlow)
* scikit-learn
* spacy
* django
* numpy
* pandas
* tensorFlow 2.14
* tensorflow-hub

Next, you will need a SECRET_KEY to place in the settings.py file in the abstract_site folder:

> python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

If you have multiple versions of Python installed, you will need to run the following instead:

> python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

Then, in the project folder, run the following in a VS Code terminal:

> python manage.py makemigrations
>
> python manage.py migrate
>
> python manage.py runserver

Again, if you have multiple versions of Python installed, use "python3" instead of "python"

Development server will usually be found at http://127.0.0.1:8000/

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

The database management portion of this project consisted of choosing a database and implementing it appropriately. As such, I have chosen Django's default SQLite database for three reasons. First, SQLite is a great database engine for most low to medium traffic websites (as stated in their documentation) which fits the classification of my student project adequately. Second, SQLite can handle roughly 100k hits/day which is way more than my student project will ever see. Finally, with SQLite already being implemented in Django with no extra code or additional deployment options, SQLite seemed to be the perfect choice for accessibility and ease of deployment.

#### Front End Web Development

The front end portion consists of a large portion of this project. The front end is not just a portal to the database and API, it must employ and maintain a high standard of user experience. The front end had to be simple and present the necessary information immediately on the first page as that is where the majority of the web traffic will reach. Easy navigation and further information must also be present. As such, I have chosen the same color scheme and logo as PubMed to be consistent and familiar.

#### Back End Web Development

The backend consisted of Django which is a high-level Python web framework. Rather than complicating the project with a different programming language all together by using JavasScript or other frameworks, I wanted to continue to learn and expand my Python knowledge. I have used the MERN (MongoDB, Express, Angular, Node) stack before and with the many different frameworks, it can become difficult to track files and figure out where a bug may lie which increases debugging time significantly. For this reason, Django was a wonderful option that came together in a single package and made development so much simpler for such a small project.

## Progress Report

* Jan 8:  Conducted research on how to use Python (as I am coming from Java)
* Jan 9:  Conducted research on Python libraries that would assist for creating my project
* Jan 10: Conducted research on TensorFlow
* Jan 11: Conducted research on NLP and various methods
* Jan 12: Conducted research on similar problems which can be adapted to my own project
* Jan 13: Developed [various TensorFlow models](https://github.com/SinclairK602/495_NLP/blob/main/Abstract_Condenser.ipynb) for testing
* Jan 14: Began fine-tuning my successful TensorFlow model and began writing documentation
* Jan 15: Began running tests on the TensorFlow model and worked further on documentation
* Jan 16: Conducted research on Django and installed necessary packages
* Jan 17: Further research conducted on Django and its viability for my project
* Jan 18: Began developing the front end with Django
* Jan 19: Continued development with Django
* Jan 20: Continued development with Django
* Jan 21: Began integrating the admin panel and database model
* Jan 22: Integrated scripts to fetch Abstracts from PubMed and process them with my TensorFlow model
* Jan 23: Reworked my Django project settings to handle deployment
* Jan 24: Conducted research for deployment methods
* Jan 25: Trialled AWS EC2 which was over complicated and moved to deployment with GCP
* Jan 26: Continued setting up a VM instance and installing necessary libraries for my project
* Jan 27: Deployed and debugged numerous issue
* Jan 28: Debugged scheduled tasks and tweak any final settings
* Jan 29: Went through project files and cleaned up code while commenting for readability
* Jan 30: Continued extensive documentation
* Jan 31: Continued extensive documentation and uploaded documentation to website
* Feb 1: Reviewed documentation and submitted project
