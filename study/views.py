from django.shortcuts import render, get_object_or_404, redirect
from .models import Abstract
import subprocess
from django.http import Http404
import os


# Index page for the study app
def starting_page(request):
    latest_studies = Abstract.objects.all().order_by("-date")[
        :3
    ]  # Get the 3 most recent studies
    return render(request, "study/index.html", {"studies": latest_studies})


# Search for a study by PMID
def search_study(request):
    pmid = request.GET.get("pmid")
    if not pmid or not pmid.isdigit():  # Check if the PMID is a valid digit format
        raise Http404("No PMID provided.")
    study = Abstract.objects.filter(
        pmid=pmid
    ).first()  # Check if the PMID exists in the database
    if study:
        return redirect("study-detail-page", slug=study.pmid)
    else:  # If the PMID does not exist in the database, fetch it from PubMed
        try:
            print("Running shell script to fetch PMID...")
            subprocess.run(
                ["./request.sh", pmid], timeout=5
            )  # Run the shell script to fetch the PMID utilizing timeout incase of API hang
            file_path = "reuqest.txt"
            if (
                os.path.exists(file_path) and os.path.getsize(file_path) == 0
            ):  # Validation for erroneous PMIDs
                raise Http404("PMID Does not exist.")
            print("Running Python script to process abstract...")
            subprocess.run(
                ["python3", "process_abstracts.py"]
            )  # Run the Python script to process the abstract
            study = Abstract.objects.filter(pmid=pmid).first()
        except subprocess.TimeoutExpired:
            print("Script timed out.")
            raise Http404("PMID not found and fetching process failed.")
        except Exception as e:
            print(f"An error occurred: {e}")
            raise Http404("An error occurred while processing the PMID request.")
    return redirect(
        "study-detail-page", slug=study.pmid
    )  # Redirect to the study-detail-page with the PMID


# Display 50 most recent studies studies in the database in case database gets too large
def studies(request):
    all_studies = Abstract.objects.all().order_by("-date")[:50]
    return render(request, "study/all-studies.html", {"all_studies": all_studies})


# Display the details of a study
def study_detail(request, slug):
    identified_study = get_object_or_404(Abstract, pmid=slug)
    return render(request, "study/study-detail.html", {"study": identified_study})


# Display the documentation page
def doc(request):
    return render(request, "study/doc.html")
