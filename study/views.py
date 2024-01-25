from django.shortcuts import render, get_object_or_404, redirect
from .models import Abstract
import subprocess
from django.http import JsonResponse, HttpResponse

# Create your views here.


def starting_page(request):
    latest_studies = Abstract.objects.all().order_by("-date")[:3]
    return render(request, "study/index.html", {"studies": latest_studies})


def search_study(request):
    pmid = request.GET.get("pmid")
    study, created = Abstract.objects.get_or_create(pmid=pmid)
    if created:
        try:
            print("Running shell script to fetch PMID...")
            subprocess.run(["./request.sh", pmid], timeout=5)
            print("Running Python script to process abstracts...")
            subprocess.run(["python3", "process_abstracts.py"])
        except subprocess.TimeoutExpired:
            print("Script timed out.")
            return HttpResponse("PMID not found and fetching process failed.")
        except Exception as e:
            print(f"An error occurred: {e}")
            return HttpResponse("An error occurred while processing the PMID.")
    return redirect("study-detail-page", slug=study.pmid)



def check_pmid_status(request):
    pmid = request.GET.get("pmid")
    try:
        Abstract.objects.get(pmid=pmid)
        return JsonResponse({"status": "found"})
    except Abstract.DoesNotExist:
        # You can also add a check here to distinguish between 'not found' and 'fetching failed'
        return JsonResponse({"status": "not found"})


def studies(request):
    all_studies = Abstract.objects.all().order_by("-date")
    return render(request, "study/all-studies.html", {"all_studies": all_studies})


def study_detail(request, slug):
    identified_study = get_object_or_404(Abstract, pmid=slug)
    return render(request, "study/study-detail.html", {"study": identified_study})


def doc(request):
    return render(request, "study/doc.html")
