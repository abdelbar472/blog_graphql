import json
from django.test import TestCase
from graphene.test import Client
from .models import TestModel
from .schema import schema


class TestModelGraphQLTests(TestCase):
    def setUp(self):
        # Create test records
        self.test_model1 = TestModel.objects.create(title="Test Item 1")
        self.test_model2 = TestModel.objects.create(title="Test Item 2")
        self.client = Client(schema)

    def test_get_single_test_model(self):
        query = """
        query {
            testModel(id: %s) {
                id
                title
            }
        }
        """ % self.test_model1.id

        result = self.client.execute(query)
        self.assertIsNone(result.get('errors'))
        self.assertEqual(result['data']['testModel']['id'], str(self.test_model1.id))
        self.assertEqual(result['data']['testModel']['title'], self.test_model1.title)

    def test_get_all_test_models(self):
        query = """
        query {
            allTestModels {
                id
                title
            }
        }
        """

        result = self.client.execute(query)
        self.assertIsNone(result.get('errors'))
        self.assertEqual(len(result['data']['allTestModels']), 2)

    def test_create_test_model(self):
        mutation = """
        mutation {
            createTestModel(title: "New Test Item") {
                testModel {
                    id
                    title
                }
                success
                message
            }
        }
        """

        result = self.client.execute(mutation)
        self.assertIsNone(result.get('errors'))
        self.assertTrue(result['data']['createTestModel']['success'])
        self.assertEqual(result['data']['createTestModel']['testModel']['title'], "New Test Item")

        # Verify it was created in the database
        created_id = result['data']['createTestModel']['testModel']['id']
        self.assertTrue(TestModel.objects.filter(id=created_id).exists())

    def test_update_test_model(self):
        mutation = """
        mutation {
            updateTestModel(id: %s, title: "Updated Title") {
                testModel {
                    id
                    title
                }
                success
                message
            }
        }
        """ % self.test_model1.id

        result = self.client.execute(mutation)
        self.assertIsNone(result.get('errors'))
        self.assertTrue(result['data']['updateTestModel']['success'])
        self.assertEqual(result['data']['updateTestModel']['testModel']['title'], "Updated Title")

        # Verify it was updated in the database
        self.test_model1.refresh_from_db()
        self.assertEqual(self.test_model1.title, "Updated Title")

    def test_delete_test_model(self):
        mutation = """
        mutation {
            deleteTestModel(id: %s) {
                success
                message
            }
        }
        """ % self.test_model1.id

        result = self.client.execute(mutation)
        self.assertIsNone(result.get('errors'))
        self.assertTrue(result['data']['deleteTestModel']['success'])

        # Verify it was deleted from the database
        self.assertFalse(TestModel.objects.filter(id=self.test_model1.id).exists())

    def test_get_nonexistent_test_model(self):
        query = """
        query {
            testModel(id: 999) {
                id
                title
            }
        }
        """

        result = self.client.execute(query)
        self.assertIsNone(result.get('errors'))
        self.assertIsNone(result['data']['testModel'])