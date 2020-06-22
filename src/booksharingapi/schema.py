from .models import Book, Stud
from graphene import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType


# Graphene will automatically map the Category model's fields onto the Book Node.
# This is configured in the BookNode's Meta class (as you can see below)

# exapmle of one graphQL query
# query hello{
#   allIngredients {
#     edges {
#       node {
#         id
#         bookName
#         authorName
#       }
#     }
#   }
# }

class StudNode(DjangoObjectType):
    class Meta:
        model = Stud
        # Allow for some more advanced filtering here

        filter_fields = [
            "id",

            "firstName",
            "lastName",
            "email",
            "age",

            "password",
            "address",
            "contactNo",
            "student",
        ]

        interfaces = (Node,)


class IngredientNode(DjangoObjectType):
    class Meta:
        model = Book
        # Allow for some more advanced filtering here

        filter_fields = {

            "bookId": ["exact"],
            "bookName": ["exact"],
            "isbnNo": ["exact"],
            "authorName": ["exact"],
            "pubName": ["exact"],
            "originalPrice": ["exact"],
            "price": ["exact"],
            "bookCatgName": ["exact"],
            "postedBy": ["exact"],
            "postedBy__firstName": ["exact"],
            "postedDate": ["exact"],

        }
        interfaces = (Node,)


class Query(object):
    stud = Node.Field(StudNode)
    all_stud = DjangoFilterConnectionField(StudNode)

    ingredient = Node.Field(IngredientNode)

    all_ingredients = DjangoFilterConnectionField(IngredientNode)

    # book=graphene.List(IngredientNode)
# class BookInput(graphene.InputObjectType):
#     id = graphene.ID()
#     bookId=graphene.String()
#     bookName
#     isbnNo
#     authorName
#     pubName
#     originalPrice
#     price
#     bookCatgName
#     postedBy
#     postedDate
