from django.contrib import admin
from django.urls import path
from student_clubs.views import CreateEventAPI, EventAPIView, UpdateEventView, UpdateClubView, MyLogin, StudentDash, EventCreateView, EventListView, EventUpdateView, ListEvent, CreateEvent, UpdateEvent, ListActivity, UpdateEventAdmin, ListActivityAdmin, ListActivityAdminDashboard, UpdateEventAdminDashboard, ClubListView, ClubCreateView, StudentProfile, ClubUpdateView, StudentClubs, About, StudentEvent, AdminActivityPost, sign_up_student
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from student_clubs.views import CustomLogoutView  # Import your custom view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MyLogin.as_view(), name="homepage"),
    path('student-dashboard/',StudentDash.as_view() , name="StudentDashboard"),
    path('manager_dashboard/', EventListView.as_view(), name='manager_dashboard'),
    path('create_event/', EventCreateView.as_view(), name='create_event'),
    path('update_event/<int:pk>/', UpdateEventView.as_view(), name='update_event'),
    path('manager_events/', ListEvent.as_view(), name='manager_dashboard_manager'),
    path('manager_create_event/', CreateEvent.as_view(), name='create_event_manager'),
    path('manager_activity/', ListActivity.as_view(), name='manager_activity'),
    path('admin_events/', ListActivityAdmin.as_view(), name='admin_activity'),
    path('admin_dashboard/', ListActivityAdminDashboard.as_view(), name='admin_dashboard'),
    path('admin_activity', AdminActivityPost.as_view(), name="admin_activitypost"),
    path('create_club/', ClubCreateView.as_view(), name='create_club'),
    path('update_club/<int:pk>/', UpdateClubView.as_view(), name='update_club'),
    path('admin_clubs/', ClubListView.as_view(), name='admin_club'),
    path('about/', About.as_view(), name="about"),
    path('student/clubs/', StudentClubs.as_view(), name="student_clubs"),
    path('student/profile/', StudentProfile.as_view(), name="student_profile"),
    path('student/event', StudentEvent.as_view(), name="student_event"),
    path('api/create_event/', CreateEventAPI.as_view(), name='api_create_event'),
    path('api/events/', EventAPIView.as_view(), name='event_api'),
    path('Student/CreateAccount', sign_up_student ,name='signup'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)