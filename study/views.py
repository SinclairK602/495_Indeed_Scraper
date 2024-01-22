from django.shortcuts import render, get_object_or_404
from .models import Abstract

# Create your views here.


def starting_page(request):
    latest_studies = Abstract.objects.all().order_by("-date")[:3]
    return render(request, "study/index.html", {"studies": latest_studies})


def studies(request):
    all_studies = Abstract.objects.all().order_by("-date")
    return render(request, "study/all-studies.html", {"all_studies": all_studies})


def study_detail(request, slug):
    identified_study = get_object_or_404(Abstract, pmid=slug)
    return render(request, "study/study-detail.html", {"study": identified_study})


def doc(request):
    return render(request, "study/doc.html")
