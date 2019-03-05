from django.shortcuts import redirect, render


def home(request):
    """
    Returns the home pag for non-users, score side for users.
    :param request:
    :return:
    """
    if request.user.is_authenticated is True:
        return redirect("Scores:score-list")
    return render(request, "index.html")


def about(request):
    """
    Returns the about page
    :param request:
    :return:
    """
    return render(request, "front/about.html")


def contact(request):
    """
    Returns the contact page
    :param request:
    :return:
    """
    return render(request, "front/contact.html")


def contribute(request):
    """
    Returns a contribution page.
    :param request:
    :return:
    """
    return render(request, "front/contribute.html")
