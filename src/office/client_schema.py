import graphene
from graphene_django import DjangoObjectType

from .models import Case, Client, Lawyer


class ClientType(DjangoObjectType):
    class Meta:
        model = Client
        fields = "__all__"


class CreateClient(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        surname = graphene.String(required=True)
        lawyer = graphene.ID(required=True)
        case = graphene.ID(required=True)

    client = graphene.Field(ClientType)

    def mutate(self, info, first_name, surname, lawyer, case):
        lawyer = Lawyer.objects.get(pk=lawyer)
        case = Case.objects.get(pk=case)
        client = Client(
            first_name=first_name, surname=surname, lawyer=lawyer, case=case
        )
        client.save()
        return CreateClient(client=client)


class UpdateClient(graphene.Mutation):
    class Arguments:
        lawyer = graphene.ID(required=True)

    client = graphene.Field(ClientType)

    def mutate(self, info, id, lawyer=None):
        try:
            lawyer = Lawyer.objects.get(pk=lawyer)
            client = Client.objects.get(pk=id)
        except Client.DoesNotExist or Lawyer.DoesNotExist:
            raise Exception("Objects does not exists.")

        if lawyer is not None:
            client.lawyer.id = lawyer

        client.save()
        return UpdateClient(client=client)


class DeleteClient(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            client = Client.objects.get(pk=id)
        except Client.DoesNotExist:
            raise Exception("Clients does not exists.")

        client.delete()
        return DeleteClient(success=True)
