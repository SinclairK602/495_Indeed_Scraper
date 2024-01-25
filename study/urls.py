from django.urls import path

from . import views

urlpatterns = [
    path("", views.starting_page, name="starting-page"),
    path("studies", views.studies, name="studies-page"),
    path("documentation", views.doc, name="doc"),
    path("study/<slug:slug>", views.study_detail, name="study-detail-page"),
    path("search", views.search_study, name="search-study"),
    path("check-pmid", views.check_pmid_status, name="check-pmid-status"),
]
