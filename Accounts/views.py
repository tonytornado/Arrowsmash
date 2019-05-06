from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.views import generic

from Accounts.forms import ProfileForm, UserForm, UpdateUserForm, UpdateProfileForm, SearchForm
from Accounts.models import Profile, Follow, FollowManager


def logout_view(request):
    logout(request)


class ProfileView(generic.DetailView):
    model = Profile
    queryset = Profile.objects.all()
    template_name = 'profiles/profile-view.html'


class ProfileListing(generic.ListView):
    model = Profile
    template_name = 'profiles/view-all.html'
    paginate_by = 20
    searchstring = ''

    def get_context_data(self, **kwargs):
        context = super(ProfileListing, self).get_context_data(**kwargs)
        context['form'] = SearchForm(self.searchstring)
        from pytz import unicode
        context['search_request'] = ('searchstring=' + unicode(self.searchstring))
        return context

    def get(self, request, *args, **kwargs):
        self.searchstring = request.GET.get('searchstring', '')
        return super(ProfileListing, self).get(request, *args, **kwargs)

    def get_queryset(self):
        if not self.searchstring:
            listing = Profile.objects.all()
        else:
            listing = Profile.objects.filter(
                user__username__contains=self.searchstring
            )

        return listing.order_by('-id')


@transaction.atomic
def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()  # This will load the Profile created by the Signal
            profile_form = ProfileForm(request.POST, request.FILES,
                                       instance=user.profile)  # Reload the profile form with the profile instance
            profile_form.full_clean()
            profile_form.save()  # Gracefully save the form
            messages.success(request, "You're in. Now open that front door and take the first step.")
            return redirect('login')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Updated profile. Hope you dig the new you.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile-update.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def follower_add(request, pk):
    if request.method == 'POST':
        followee = Profile.objects.get(pk=pk)
        follower = request.user.profile
        try:
            FollowManager.follow(follower, followee)
            messages.success(request, "You're following them now.")
        except Follow.DoesNotExist:
            return False
        else:
            return redirect('Accounts:view-profile', pk=pk)

    return render(request, 'index.html')


@login_required
def follower_delete(request, pk):
    if request.method == 'POST':
        followee = Profile.objects.get(pk=pk)
        follower = request.user.profile
        try:
            FollowManager.remove_follow(follower, followee)
            messages.success(request, "You're no longer following them.")
        except Follow.DoesNotExist:
            return False
        else:
            return redirect('Accounts:view-profile', pk=pk)
    return render(request, 'index.html')
