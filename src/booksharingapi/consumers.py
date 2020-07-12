# # import json
# from channels.generic.websocket import WebsocketConsumer
# # from booksharingapi.models import Book


# # class ChatConsumer(WebsocketConsumer):
# #     def connect(self):
# #         self.accept()
# #         Book.objects.all()

# #     def disconnect(self, close_code):
# #         pass

# #     def receive(self, text_data):
# #         text_data_json = json.loads(text_data)
# #         message = text_data_json['message']

# #         self.send(text_data=json.dumps({
# #             'message': message
# #         }))

# from channels.generic.websocket import AsyncJsonWebsocketConsumer
# from .models import Book
# from .serializers import BookSerializer
# from rest_framework.views import APIView
# from rest_framework import mixins, views
# from rest_framework.response import Response
# from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser
# from channels.layers import get_channel_layer


# class NotificationConsumer(WebsocketConsumer,AsyncJsonWebsocketConsumer):
#     async def connect(self):
#         # We're always going to accept the connection, though we may
#         # close it later based on other factors.
#         # print("connect")

#         await self.accept()

#     async def notify(self, event):
#         """
#         This handles calls elsewhere in this codebase that look
#         like:

#             channel_layer.group_send(group_name, {
#                 'type': 'notify',  # This routes it to this handler.
#                 'content': json_message,
#             })

#         Don't try to directly use send_json or anything; this
#         decoupling will help you as things grow.
#         """
#         # print("notify")
#         await self.send_json(event["content"])

#     async def receive_json(self, content, **kwargs):

#         serializer = self.get_serializer()
#         print(serializer)
#         if not serializer.is_valid():
#             return
#         # Define this method on your serializer:
#         group_name = serializer.get_group_name()
#         # The AsyncJsonWebsocketConsumer parent class has a
#         # self.groups list already. It uses it in cleanup.
#         self.groups.append(group_name)
#         # This actually subscribes the requesting socket to the
#         # named group:
#         await self.channel_layer.group_add(
#             group_name,
#             self.channel_name,
#         )

#     def get_serializer(self):
#         return Book.objects.all()
#         # pass

#         # serializer = BookSerializer(book, many=True)
#         # print(serializer.data)
#         # return serializer
#         # … omitted for brevity. See
#         # https://github.com/encode/django-rest-framework/blob/master/rest_framework/generics.py


# class ListAPIView(APIView):
#     parser_class = (FileUploadParser, MultiPartParser, JSONParser)
#     """
#     Concrete view for listing a queryset.
#     """

#     # def get(self, request):
#     #     book = Book.objects.all()
#     #     serializer = BookSerializer(book, many=True)

#     #     return Response(serializer.data)

#     async def get(self,request):
#         book = Book.objects.all()
#         serializer = BookSerializer(book,many=True)
#         group_name = serializer.get_group_name()
#         channel_layer = get_channel_layer()
#         content = {
#             # This "type" passes through to the front-end to facilitate
#             # our Redux events.
#             "type": "UPDATE_FOO",
#             "payload": serializer.data,
#         }
#         await channel_layer.group_send(group_name, {
#             # This "type" defines which handler on the Consumer gets
#             # called.
#             "type": "notify",
#             "content": content,
#         })
#         