import graphene

import office.schema


class Query(office.schema.Query, graphene.ObjectType):
    pass


class Mutation(office.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
