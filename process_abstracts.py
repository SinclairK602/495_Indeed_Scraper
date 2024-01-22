import re
import tensorflow as tf
from spacy.lang.en import English
from sklearn.preprocessing import LabelEncoder
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "abstract_site.settings")
django.setup()

from study.models import Abstract


def django_functionality(abstract_dict):
    existing_abstract = Abstract.objects.filter(pmid=abstract_dict.get("pmid")).first()
    if existing_abstract is None:
        abstract = Abstract(**abstract_dict)
        abstract.save()
    else:
        pass


def load_model(model_filename):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    model_path = os.path.join(script_dir, model_filename)
    return tf.keras.models.load_model(model_path)


def split_chars(text):
    return " ".join(list(text))


def remove_classifications(abstract):
    keywords = [
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


def parse_dataset(file_paths):
    all_abstracts = []
    for file_path in file_paths:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_dir, file_path)
        if os.path.getsize(file_path) == 0:
            continue
        else:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

            studies = text.strip().split("\n\n\n")

            for study in studies:
                # Extracting various components from the study
                doi = (
                    re.search(r"doi: ([^\s]+)", study).group(1)
                    if re.search(r"doi: ([^\s]+)", study)
                    else None
                )
                pmid = (
                    re.search(r"PMID: ([^\s]+)", study).group(1)
                    if re.search(r"PMID: ([^\s]+)", study)
                    else None
                )
                date = (
                    re.search(r"(\d{4} \w{3} \d{1,2})", study).group(1)
                    if re.search(r"(\d{4} \w{3} \d{1,2})", study)
                    else None
                )
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
                abstract = remove_classifications(abstract)

                label = "Unknown"

                if "meta-analys" in title.lower():
                    label = "Meta-Analysis"
                elif (
                    "randomized controlled trial" in title.lower()
                    or "randomised controlled trial" in title.lower()
                    or "randomised clinical trial" in title.lower()
                    or "randomised trial" in title.lower()
                ):
                    label = "RCT"

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


def postprocess_abstracts(abstracts):
    for abstract in abstracts:
        for key in ["background", "objective", "method", "results", "conclusions"]:
            if key in abstract:
                abstract[key] = " ".join(abstract[key])
    return abstracts


def classify_sentence(sentence, model, label_encoder):
    prediction = model.predict([sentence])
    category = label_encoder.classes_[tf.argmax(prediction)]
    return category.lower()


def categorize_sentences(abstracts, model, label_encoder, nlp):
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

    # Load and parse dataset
    files = ["rct_dataset.txt", "meta_dataset.txt", "request.txt"]
    abstracts = parse_dataset(files)

    # Initialize categories in each abstract dict
    for abstract in abstracts:
        for category in label_encoder.classes_:
            abstract[category.lower()] = []

    # Process abstracts
    processed_abstracts = categorize_sentences(abstracts, model, label_encoder, nlp)
    processed_abstracts = postprocess_abstracts(processed_abstracts)

    for abstracts in processed_abstracts:
        django_functionality(abstracts)
        # print("Date:", abstracts["date"])
        # print("DOI:", abstracts["doi"])
        # print("PMID:", abstracts["pmid"])
        # print("Label:", abstracts["label"])
        # print("Title:", abstracts["title"])
        # print("Authors:", abstracts["authors"])
        # print("Author Info:", abstracts["author_info"])
        # print("Background:", abstracts["background"])
        # print("Objective:", abstracts["objective"])
        # print("Method:", abstracts["method"])
        # print("Results:", abstracts["results"])
        # print("Conclusions:", abstracts["conclusions"])


if __name__ == "__main__":
    main()
