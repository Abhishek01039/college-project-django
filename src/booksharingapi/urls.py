
from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
# router = routers.DefaultRouter()
# router.register(r'student', UserViewSet)

urlpatterns = [

    path('', views.index, name='index'),
    # path('', include(router.urls)),
    # path('booksharing/rest-auth/', include('rest_auth.urls')),
    path('student/', views.StudentList.as_view()),  # get, post
    path('student/<int:pk>/', views.StudentDetail.as_view()),  # get, delete, put
    path('book/', views.BookList.as_view()),  # get, post
    path('book/<int:pk>/', views.BookDetail.as_view()),  # get, delete, put
    path('purchasedbook/', views.PurchasedBookList.as_view()),  # get, post
    # get, delete, put
    path('purchasedbook/<int:pk>/', views.PurchasedBookDetail.as_view()),
    path('bookimage/', views.BookImageList.as_view()),  # get, post
    # get, delete, put
    path('bookimage/<int:pk>/', views.BookImageDetail.as_view()),
    path('feedback/', views.FeedBackList.as_view()),  # get, post
    path('feedback/<int:pk>/', views.FeedBackDetail.as_view()),  # get, delete, put
    path('login/', views.LogIn.as_view()),  # post
    # path('login/', obtain_auth_token),
    path('purchasedByStud/', views.GetPurchasedByStud.as_view()),  # post
    path('imagebyid/<int:pk>/', views.BookImageById.as_view()),  # get
    path('postbook/', views.BookPost.as_view()),  # post
    path('bookbyposted/<int:pk>/', views.BookByPosted.as_view()),  # get
    path('changepass/<int:pk>/', views.ChangePassword.as_view()),  # post
    path('latestbook/', views.BookLatestList.as_view()),  # get
    path('homelist/', views.HomeList.as_view()),  # get
    path('updatestudentphoto/<int:pk>/',
         views.UpdateStudentPhoto.as_view()),  # put
    path('purchasedbookbyuser/<int:pk>/',
         views.PurchasedBookByUser.as_view()),  # get
    path('updatebookimage/', views.BookImageUpdate.as_view()),  # put
    path('addimagelist/', views.AddImageList.as_view()),  # post
    path('sendemail/', views.SendEmail.as_view()),  # post
    path('updatepassword/', views.UpdatePassword.as_view()),  # put
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
