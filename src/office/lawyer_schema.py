import graphene
from graphene_django import DjangoObjectType

from .models import Lawyer


class LawyerType(DjangoObjectType):
    class Meta:
        model = Lawyer
        fields = "__all__"


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
            raise Exception("Lawyer does not exist")

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
            raise Exception("Lawyer is not exist")

        lawyer.delete()
        return DeleteLawyer(success=True)
