from django.urls import path
from . import views
urlpatterns = [
    path("", views.messages_view, name="messages"),
    path("send/", views.send_message, name="send_message"),
    path("<int:pk>/detail/", views.get_message_detail, name="message_detail"),
    path("<int:pk>/reply/", views.reply_message, name="reply_message"),
    path("<int:pk>/delete/", views.delete_message, name="delete_message"),
]
