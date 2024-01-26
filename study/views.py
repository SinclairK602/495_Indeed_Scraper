from django.shortcuts import render, get_object_or_404, redirect
from .models import Abstract
import subprocess
from django.http import Http404
import os

# Create your views here.


def starting_page(request):
    latest_studies = Abstract.objects.all().order_by("-date")[:3]
    return render(request, "study/index.html", {"studies": latest_studies})


def search_study(request):
    pmid = request.GET.get("pmid")
    if not pmid or not pmid.isdigit():
        raise Http404("No PMID provided.")
    study = Abstract.objects.filter(pmid=pmid).first()
    if study:
        return redirect("study-detail-page", slug=study.pmid)
    else:
        try:
            print("Running shell script to fetch PMID...")
            subprocess.run(["./request.sh", pmid], timeout=5)
            file_path = "reuqest.txt"
            if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
                raise Http404("PMID Does not exist.")
            print("Running Python script to process abstract...")
            subprocess.run(["python3", "process_abstracts.py"])
            study = Abstract.objects.filter(pmid=pmid).first()
        except subprocess.TimeoutExpired:
            print("Script timed out.")
            raise Http404("PMID not found and fetching process failed.")
        except Exception as e:
            print(f"An error occurred: {e}")
            raise Http404("An error occurred while processing the PMID request.")
    return redirect("study-detail-page", slug=study.pmid)


def studies(request):
    all_studies = Abstract.objects.all().order_by("-date")
    return render(request, "study/all-studies.html", {"all_studies": all_studies})


def study_detail(request, slug):
    identified_study = get_object_or_404(Abstract, pmid=slug)
    return render(request, "study/study-detail.html", {"study": identified_study})


def doc(request):
    return render(request, "study/doc.html")
