import graphene
from graphene_django import DjangoObjectType

from .client_schema import ClientType, CreateClient, DeleteClient, UpdateClient
from .lawyer_schema import CreateLawyer, DeleteLawyer, LawyerType, UpdateLawyer
from .models import Case, Client, Lawyer, Speciality


class CaseType(DjangoObjectType):
    class Meta:
        model = Case
        fields = "__all__"


class SpecialityType(DjangoObjectType):
    class Meta:
        model = Speciality
        fields = "__all__"


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


class Mutation(graphene.ObjectType):
    create_lawyer = CreateLawyer.Field()
    create_client = CreateClient.Field()
    update_lawyer = UpdateLawyer.Field()
    update_client = UpdateClient.Field()
    delete_lawyer = DeleteLawyer.Field()
    delete_client = DeleteClient.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
