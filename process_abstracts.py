import re
import tensorflow as tf
from spacy.lang.en import English
from sklearn.preprocessing import LabelEncoder
import os
import django
from datetime import datetime

# Setting up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "abstract_site.settings")
django.setup()

# Importing Django database model
from study.models import Abstract


# Function to save abstract values to database
def django_functionality(abstract_dict):
    existing_abstract = Abstract.objects.filter(
        pmid=abstract_dict.get("pmid")
    ).first()  # Check if abstract already exists in database
    if (
        existing_abstract is None
    ):  # If abstract does not exist, create new abstract object and save values
        abstract = Abstract()
        abstract.pmid = abstract_dict.get("pmid")
        abstract.date = abstract_dict.get("date")
        abstract.doi = abstract_dict.get("doi")
        abstract.label = abstract_dict.get(
            "label", "Unknown"
        )  # Default to 'Unknown' if not provided
        abstract.title = abstract_dict.get("title")
        abstract.authors = abstract_dict.get("authors")
        abstract.author_info = abstract_dict.get("author_info")
        abstract.abstract = abstract_dict.get("abstract")
        abstract.background = abstract_dict.get("background")
        abstract.objective = abstract_dict.get("objective")
        abstract.method = abstract_dict.get("method")
        abstract.results = abstract_dict.get("results")
        abstract.conclusions = abstract_dict.get("conclusions")
        abstract.save()
    else:
        pass


# Function to load TensorFlow model
def load_model(model_filename):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    model_path = os.path.join(script_dir, model_filename)
    return tf.keras.models.load_model(model_path)


# Function to split sentences into characters
def split_chars(text):
    return " ".join(list(text))


# Function to remove pre-existing classification labels from abstracts
def remove_classifications(abstract):
    keywords = [  # List of keywords to remove which may need to be updated as necessary
        "PURPOSE",
        "METHODS",
        "RESULTS",
        "CONCLUSION",
        "CONCLUSIONS",
        "BACKGROUND",
        "OBJECTIVE",
        "DISCUSSION",
    ]
    pattern = r"(?:" + "|".join(keywords) + r"):\s*"
    return re.sub(pattern, "", abstract, flags=re.IGNORECASE)


# Function to parse dataset
def parse_dataset(file_paths):
    all_abstracts = []
    for file_path in file_paths:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_dir, file_path)
        # Skip empty files
        if os.path.getsize(file_path) == 0:
            continue
        else:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

            # Split studies into individual studies
            studies = text.strip().split("\n\n\n")

            for study in studies:
                # Extracting various components from the study using regex
                doi_pattern = r"doi:\s*(?:\n)?([^\s]+)"
                doi = re.search(doi_pattern, study, re.DOTALL)
                doi = doi.group(1) if doi else None
                pmid = (
                    re.search(r"PMID: ([^\s]+)", study).group(1)
                    if re.search(r"PMID: ([^\s]+)", study)
                    else None
                )
                date = datetime.now().strftime("%Y %b %d")
                title = (
                    re.search(r"\n\n(.*?)\n\n", study, re.DOTALL)
                    .group(1)
                    .strip()
                    .replace("\n", "")
                    if re.search(r"\n\n(.*?)\n\n", study, re.DOTALL)
                    else None
                )
                authors = (
                    re.search(r"(?:.*?\n\n){2}(.*?)\n\n", study, re.DOTALL)
                    .group(1)
                    .strip()
                    .replace("\n", "")
                    if re.search(r"(?:.*?\n\n){2}(.*?)\n\n", study, re.DOTALL)
                    else None
                )
                author_info = (
                    re.search(
                        r"Author information:\n(.*?)(?=\n\n|\Z)", study, re.DOTALL
                    )
                    .group(1)
                    .strip()
                    .replace("\n", "")
                    if re.search(
                        r"Author information:\n(.*?)(?=\n\n|\Z)", study, re.DOTALL
                    )
                    else None
                )
                abstract = (
                    re.search(
                        r"Author information:.*?\n\n(.*?)(?=\n\n|\Z)", study, re.DOTALL
                    )
                    .group(1)
                    .strip()
                    .replace("\n", "")
                    if re.search(
                        r"Author information:.*?\n\n(.*?)(?=\n\n|\Z)", study, re.DOTALL
                    )
                    else None
                )

                if abstract is None:
                    continue

                # Remove pre-existing classification labels from abstracts
                abstract = remove_classifications(abstract)

                # Label each study using keywords in the title
                label = "Unknown"
                if "meta-analys" in title.lower():
                    label = "Meta-Analysis"
                elif (
                    "randomized controlled" in title.lower()
                    or "randomised controlled" in title.lower()
                    or "randomised clinical" in title.lower()
                    or "randomized clinical" in title.lower()
                    or "randomised trial" in title.lower()
                    or "randomized, controlled" in title.lower()
                ):
                    label = "RCT"

                # Create dictionary for each study
                study_dict = {
                    "date": date,
                    "doi": doi,
                    "pmid": pmid,
                    "label": label,
                    "title": title,
                    "authors": authors,
                    "author_info": author_info,
                    "abstract": abstract,
                    "background": [],
                    "objective": [],
                    "method": [],
                    "results": [],
                    "conclusions": [],
                }
                all_abstracts.append(study_dict)

    return all_abstracts


# Function to postprocess abstracts by joining sentences in each category
def postprocess_abstracts(abstracts):
    for abstract in abstracts:
        for key in ["background", "objective", "method", "results", "conclusions"]:
            if key in abstract:
                abstract[key] = " ".join(abstract[key])
    return abstracts


# Function to classify sentences in abstracts
def categorize_sentences(abstracts, model, label_encoder, nlp):
    # Iterate through each abstract and split into sentences
    for abstract_dict in abstracts:
        doc = nlp(abstract_dict["abstract"])
        abstract_lines = [str(sent) for sent in doc.sents]
        total_lines_in_sample = len(abstract_lines)

        # Create features for each line
        sample_lines = []
        for i, line in enumerate(abstract_lines):
            sample_dict = {
                "text": line,
                "line_number": i,
                "total_lines": total_lines_in_sample - 1,
            }
            sample_lines.append(sample_dict)

        # One-hot encoding for line numbers and total lines
        test_abstract_line_numbers = [line["line_number"] for line in sample_lines]
        test_abstract_line_numbers_one_hot = tf.one_hot(
            test_abstract_line_numbers, depth=15
        )

        test_abstract_total_lines = [line["total_lines"] for line in sample_lines]
        test_abstract_total_lines_one_hot = tf.one_hot(
            test_abstract_total_lines, depth=20
        )

        # Split abstract lines into characters
        abstract_chars = [split_chars(sentence) for sentence in abstract_lines]

        # Predict using the model
        test_abstract_pred_probs = model.predict(
            x=(
                test_abstract_line_numbers_one_hot,
                test_abstract_total_lines_one_hot,
                tf.constant(abstract_lines),
                tf.constant(abstract_chars),
            )
        )
        test_abstract_preds = tf.argmax(test_abstract_pred_probs, axis=1)

        # Append sentences to the corresponding category
        for i, line in enumerate(abstract_lines):
            category = label_encoder.classes_[test_abstract_preds[i]]
            if category.lower() in abstract_dict:
                abstract_dict[category.lower()].append(line)
            else:
                print(f"Unrecognized category: {category}")

    return abstracts


def main():
    # Load model and label encoder
    model = load_model("token_char_pos_model")
    label_encoder = LabelEncoder()

    # Establish order of classes
    label_encoder.classes_ = [
        "background",
        "objective",
        "method",
        "results",
        "conclusions",
    ]

    # Setup NLP for sentence splitting
    nlp = English()
    nlp.add_pipe("sentencizer")

    # Load files and parse dataset
    files = ["rct_dataset.txt", "meta_dataset.txt", "request.txt"]
    abstracts = parse_dataset(files)

    # Initialize categories in each abstract dict
    for abstract in abstracts:
        for category in label_encoder.classes_:
            abstract[category.lower()] = []

    # Process abstracts
    processed_abstracts = categorize_sentences(abstracts, model, label_encoder, nlp)
    processed_abstracts = postprocess_abstracts(processed_abstracts)

    # Save abstracts to database
    for abstracts in processed_abstracts:
        django_functionality(abstracts)


if __name__ == "__main__":
    main()
