import json

from graphene_django.utils.testing import GraphQLTestCase


class LawOfficeTestCase(GraphQLTestCase):
    def test_lawyer_query(self):
        response = self.query(
            """
            query {
              lawyers {
                firstName
                surname
              }
            }
            """,
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
