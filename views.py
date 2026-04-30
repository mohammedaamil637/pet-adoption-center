from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.urls import path
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from users.models import User 
from pets.models import Pet 


class StyledFormMixin:
    """Helper to apply consistent Tailwind CSS classes to form fields."""
    def apply_tailwind_styles(self):
        style_classes = 'w-full px-6 py-4 rounded-2xl border border-slate-100 bg-slate-50/50 focus:bg-white focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500 outline-none transition-all'
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': style_classes})



class PetlyLoginForm(AuthenticationForm, StyledFormMixin):
    """Styled login form for the Petly.ai interface."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind_styles()
  
        self.fields['username'].label = "Username"
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter your username'})
        self.fields['password'].widget.attrs.update({'placeholder': '••••••••'})

class PetlySignupForm(UserCreationForm, StyledFormMixin):
    """Styled signup form for new users/shelters."""
    location = forms.CharField(max_length=255, required=False)
    is_shelter = forms.BooleanField(required=False, label="I am a Shelter/Rescue", widget=forms.CheckboxInput(attrs={
        'class': 'w-4 h-4 text-indigo-600 rounded border-slate-300 focus:ring-indigo-500'
    }))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "location", "is_shelter")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind_styles()
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email Address'})
        self.fields['location'].widget.attrs.update({'placeholder': 'Your City, State'})



def login_view(request):
    """
    Handles user login using username.
    """
    if request.method == "POST":
        form = PetlyLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = PetlyLoginForm()
    return render(request, 'login.html', {'form': form, 'title': 'Log In'})

def signup_view(request):
    """
    Handles user registration and automatic login.
    """
    if request.method == "POST":
        form = PetlySignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = PetlySignupForm()
    return render(request, 'signup.html', {'form': form, 'title': 'Sign Up'})



class PetListView(ListView):
    model = Pet
    template_name = 'pet_list.html'
    context_object_name = 'pets'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Pet.objects.filter(name__icontains=query)
        return Pet.objects.all()

class PetDetailView(DetailView):
    model = Pet
    template_name = 'pet_detail.html'
    context_object_name = 'pet'

@login_required
def add_pet(request):
    """
    Handles creating a new pet listing via the modal in base.html.
    Matches field names from the provided Model (Pet).
    """
    if request.method == 'POST':
       
        pet = Pet(
            owner=request.user,
            name=request.POST.get('name'),
            species=request.POST.get('species'),
            breed=request.POST.get('breed'),
            age_years=request.POST.get('age_years'),
            description=request.POST.get('description'),
            image=request.FILES.get('image')
        )
        pet.save()
        return redirect('home')
    return redirect('home')

def ai_assistant(request):
    return render(request, 'ai_assistant.html')