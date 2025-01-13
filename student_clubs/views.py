import json
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import RedSeaUser, Event, Club
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import  DetailView , ListView , CreateView , DeleteView , UpdateView
from .forms import RegisterForm
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class CustomLogoutView(LogoutView):
    next_page = '/'  # This ensures redirection after logout

    def dispatch(self, request, *args, **kwargs):
        # Clear specific cookies
        response = super().dispatch(request, *args, **kwargs)
        response.delete_cookie('csrftoken')
        response.delete_cookie('messages')
        response.delete_cookie('sessionid')
        return response
    
    def get_next_page(self):
        return self.next_page

class MyLogin(LoginView):
    redirect_authenticated_user = True
    template_name='loginpages.html'
    def get_success_url(self):      
        if self.request.user.is_student: 
                student = self.request.user
                return reverse_lazy('StudentDashboard')
           
        if self.request.user.is_club_manager:
               club_manager = self.request.user
               return reverse_lazy('manager_dashboard')

        if self.request.user.is_sks_admin:
             sks_manager = self.request.user
             return reverse_lazy('admin_dashboard')

    def form_invalid(self, form):
        messages.error(self.request , 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))
    

class StudentDash(ListView, LoginRequiredMixin):
     template_name="student_home.html"
     context_object_name = 'events'

     def get_queryset(self): 
        return Event.objects.all()

class EventListView(ListView, LoginRequiredMixin):
    model = Event
    template_name = 'manager_dashboard.html'
    context_object_name = 'events'

    def get_queryset(self): 
        return Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_clubs'] = Club.objects.count()
        context['total_users'] = RedSeaUser.objects.count()
        return context

class EventCreateView(CreateView, LoginRequiredMixin):
    model = Event
    template_name = 'manager_dashboard.html'
    fields = ['event_name', 'event_type', 'event_date','event_hall','event_description']
    
    success_url = reverse_lazy('manager_dashboard')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
     

class EventUpdateView(UpdateView, LoginRequiredMixin):
    model = Event
    template_name = 'events.html'
    fields = ['event_name', 'event_type', 'event_date','event_hall','event_description']
    context_object_name = "eventupdate"
    
    def get_success_url(self):
        return reverse('manager_dashboard')


class ListEvent(ListView, LoginRequiredMixin):
    model = Event
    template_name = 'manager_events.html'
    context_object_name = 'events'

    def get_queryset(self): 
        return Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_clubs'] = Club.objects.count()
        context['total_users'] = RedSeaUser.objects.count()
        return context
    
class CreateEvent(CreateView, LoginRequiredMixin):
    model = Event
    template_name = 'manager_events.html'
    fields = ['event_name', 'event_type', 'event_date','event_hall','event_description']
    
    success_url = reverse_lazy('manager_dashboard')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class UpdateEvent(UpdateView, LoginRequiredMixin):
    model = Event
    template_name = 'events.html'
    fields = ['event_name', 'event_type', 'event_date','event_hall','event_description']

    context_object_name = "eventupdate"
    def get_success_url(self):
        return reverse('manager_dashboard')
    
class CreateEventAPI(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            event_name = data.get("event_name")
            event_date = data.get("event_date")
            event_type = data.get("event_type", "General")
            event_hall = data.get("event_hall", "Main Hall")
            event_description = data.get("event_description", "No description provided.")

            if not event_name or not event_date:
                return JsonResponse({'error': 'Event name and date are required.'}, status=400)

            Event.objects.create(
                event_name=event_name,
                event_date=event_date,
                event_type=event_type,
                event_hall=event_hall,
                event_description=event_description
            )
            return JsonResponse({'message': 'Event created successfully.'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class UpdateEventView(View):
    def post(self, request, *args, **kwargs):
        try:
            event_id = request.POST.get('event_id')
            event_name = request.POST.get('event_name')
            event_type = request.POST.get('event_type')
            event = Event.objects.get(pk=event_id)
            event.event_name = event_name
            event.event_type = event_type
            event.save()
            return JsonResponse({'message': 'Event updated successfully'}, status=200)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class UpdateClubView(View):
    def post(self, request, *args, **kwargs):
        club_id = request.POST.get('club_id')
        club_name = request.POST.get('club_name')
        
        try:
            club = get_object_or_404(Club, pk=club_id)
            club.club_name = club_name
            club.save()

            return JsonResponse({'message': 'Club updated successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class ListActivity(ListView, LoginRequiredMixin):
    model = Event
    template_name = 'manager_activitypost.html'
    context_object_name = 'events'

    def get_queryset(self): 
        return Event.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_clubs'] = Club.objects.count()
        context['total_users'] = RedSeaUser.objects.count()
        return context

class UpdateEventAdmin(UpdateView, LoginRequiredMixin):
    model = Event
    template_name = 'admin_events.html'
    fields = ['event_name', 'event_type', 'event_date','event_hall','event_description']

    context_object_name = "eventupdate"
    def get_success_url(self):
        return reverse('manager_dashboard')


class ListActivityAdmin(ListView, LoginRequiredMixin):
    model = Event
    template_name = 'admin_events.html'
    context_object_name = 'events'

    def get_queryset(self): 
        return Event.objects.all()

class UpdateEventAdminDashboard(UpdateView, LoginRequiredMixin):
    model = Event
    template_name = 'admin_dashboard.html'
    fields = ['event_name', 'event_type', 'event_date','event_hall','event_description']

    context_object_name = "eventupdate"
    def get_success_url(self):
        return reverse('admin_dashboard')


class ListActivityAdminDashboard(LoginRequiredMixin,ListView,  PermissionRequiredMixin):
    model = Event
    template_name = 'admin_dashboard.html'
    context_object_name = 'events'

    def get_queryset(self): 
        return Event.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_events'] = Event.objects.count()
        context['total_users'] = RedSeaUser.objects.count()
        return context
    
    def has_permission(self):
        return super().has_permission() and self.request.user.is_authenticated and self.request.user.is_sks_admin


class ClubListView(ListView, LoginRequiredMixin):
    model = Club
    template_name = 'admin_clubs.html'
    context_object_name = 'clubs'

    def get_queryset(self): 
        return Club.objects.all()

class ClubCreateView(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Club
    template_name = 'create_club.html'
    fields = ['club_name']
    
    success_url = reverse_lazy('admin_dashboard')
    def form_valid(self, form):
        form.instance.user = self.request.user
        club_manager = self.request.user.get_email_field_name
        return super().form_valid(form)
    
     

class ClubUpdateView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Club
    template_name = 'admin_clubs.html'
    fields = ['club_name', 'club_manager']
    context_object_name = "clubupdate"
    
    def get_success_url(self):
        return reverse('manager_dashboard')
    
    def has_permission(self):
        return super().has_permission() and self.request.user.is_authenticated and self.request.user.is_club_manager


class About(TemplateView):
    template_name="about.html"

class StudentClubs(TemplateView):
    template_name="clubs.html"

class StudentProfile(TemplateView):
    template_name="student_profile.html"


class StudentEvent(ListView, LoginRequiredMixin):
    model = Event
    template_name = 'student_events.html'
    context_object_name = 'events'

    def get_queryset(self): 
        return Event.objects.all()
    
class EventAPIView(View):
    def get(self, request, *args, **kwargs):
        try:
            events = Event.objects.all().order_by('event_date')

            event_data = [
                {
                    "event_name": event.event_name,
                    "event_date": event.event_date.strftime("%Y-%m-%d"),
                    "event_type": event.event_type,
                    "event_hall": event.event_hall,
                    "event_description": event.event_description,
                }
                for event in events
            ]

            return JsonResponse(event_data, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



class AdminActivityPost(TemplateView):
    template_name="admin_activitypost.html"


def sign_up_student(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'signup_student.html', {'form': form})    
   
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.is_student= True
            user.save()
            messages.success(request, 'You have singed up successfully.')
   
            return redirect('homepage')
        else:
            return render(request, 'signup_student.html', {'form': form})
