import graphene
from graphene_django import DjangoObjectType

from .models import Lawyer, Client, Case, Speciality


class LawyerType(DjangoObjectType):
    class Meta:
        model = Lawyer
        fields = '__all__'


class ClientType(DjangoObjectType):
    class Meta:
        model = Client
        fields = '__all__'


class CaseType(DjangoObjectType):
    class Meta:
        model = Case
        fields = '__all__'


class SpecialityType(DjangoObjectType):
    class Meta:
        model = Speciality
        fields = '__all__'


# Lawyer model mutations.
class CreateLawyer(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        surname = graphene.String(required=True)
        speciality = graphene.String(required=True)

    lawyer = graphene.Field(LawyerType)

    def mutate(self, info, first_name, surname, speciality):
        lawyer = Lawyer(first_name=first_name, surname=surname, speciality=speciality)
        lawyer.save()
        return CreateLawyer(lawyer=lawyer)


class UpdateLawyer(graphene.Mutation):
    class Arguments:
        speciality = graphene.String(required=True)

    lawyer = graphene.Field(LawyerType)

    def mutate(self, info, id, speciality=None):
        try:
            lawyer = Lawyer.objects.get(pk=id)
        except Lawyer.DoesNotExist:
            raise Exception('Lawyer does not exist')

        if speciality is not None:
            lawyer.speciality = speciality

        lawyer.save()
        return UpdateLawyer(lawyer=lawyer)


class DeleteLawyer(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            lawyer = Lawyer.objects.get(pk=id)
        except Lawyer.DoesNotExist:
            raise Exception('Lawyer is not exist')

        lawyer.delete()
        return DeleteLawyer(success=True)


# Client model mutations.
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
        client = Client(first_name=first_name, surname=surname, lawyer=lawyer, case=case)
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
            raise Exception('Objects does not exists.')

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
            raise Exception('Clients does not exists.')

        client.delete()
        return DeleteClient(success=True)


class Query(graphene.ObjectType):
    lawyers = graphene.List(LawyerType)
    lawyer = graphene.Field(LawyerType, id=graphene.Int())
    clients = graphene.List(ClientType)
    client = graphene.Field(ClientType, id=graphene.Int())
    cases = graphene.List(CaseType)
    case = graphene.Field(CaseType, id=graphene.Int())
    specialities = graphene.List(SpecialityType)

    def resolve_lawyers(self, info):
        return Lawyer.objects.all()

    def resolve_lawyer(self, info, id):
        return Lawyer.objects.get(pk=id)

    def resolve_clients(self, info):
        return Client.objects.all()

    def resolve_client(self, info, id):
        return Client.objects.get(pk=id)

    def resolve_cases(self, info):
        return Case.objects.all()

    def resolve_case(self, info, id):
        return Case.objects.get(pk=id)

    def resolve_specialities(self, info):
        return Speciality.objects.all()


