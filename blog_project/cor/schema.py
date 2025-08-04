import graphene
from graphene_django import DjangoObjectType
from .models import *


# GraphQL Schema for TestModel CRUD operations
# This file defines the GraphQL types, queries, and mutations for the TestModel

class TestModelType(DjangoObjectType):
    """
    GraphQL type for TestModel that automatically maps Django model fields
    to GraphQL fields. This provides a GraphQL representation of the TestModel.
    """

    class Meta:
        model = TestModel
        fields = "__all__"  # Expose all model fields to GraphQL


class Query(graphene.ObjectType):
    """
    Root Query class that defines all available GraphQL queries.
    This class contains resolver methods that handle data fetching.
    """
    # Single TestModel query - fetch one record by ID
    test_model = graphene.Field(
        TestModelType,id=graphene.Int(required=True, description="The ID of the TestModel to retrieve"))

    # List query - fetch all TestModel records
    all_test_models = graphene.List(TestModelType,description="Retrieve all TestModel records")

    def resolve_test_model(self, info, id):
        """
        Resolver for single TestModel query.

        Args:
            info: GraphQL execution info
            id: Primary key of the TestModel to fetch

        Returns:
            TestModel instance or None if not found
        """
        try:
            return TestModel.objects.get(pk=id)
        except TestModel.DoesNotExist:
            return None

    def resolve_all_test_models(self, info):
        """
        Resolver for all TestModels query.

        Args:
            info: GraphQL execution info

        Returns:
            QuerySet of all TestModel instances
        """
        return TestModel.objects.all()


class CreateTestModel(graphene.Mutation):
    """
    Mutation to create a new TestModel instance.
    Takes a title as input and creates a new record in the database.
    """

    class Arguments:
        title = graphene.String(required=True,description="The title for the new TestModel")

    # Return field - the created TestModel instance
    test_model = graphene.Field(TestModelType)
    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, title):
        """
        Create a new TestModel instance.

        Args:
            root: Root value (usually None)
            info: GraphQL execution info
            title: Title for the new TestModel

        Returns:
            CreateTestModel instance with the created object
        """
        try:
            test_model = TestModel(title=title)
            test_model.save()
            return CreateTestModel(test_model=test_model,success=True,message="TestModel created successfully")
        except Exception as e:
            return CreateTestModel(test_model=None,success=False,message=f"Error creating TestModel: {str(e)}")


class UpdateTestModel(graphene.Mutation):
    """
    Mutation to update an existing TestModel instance.
    Takes an ID and new title, updates the corresponding record.
    """

    class Arguments:
        id = graphene.Int(required=True,description="The ID of the TestModel to update")
        title = graphene.String(required=True,description="The new title for the TestModel")

    # Return fields
    test_model = graphene.Field(TestModelType)
    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, id, title):
        """
        Update an existing TestModel instance.

        Args:
            root: Root value (usually None)
            info: GraphQL execution info
            id: Primary key of the TestModel to update
            title: New title for the TestModel

        Returns:
            UpdateTestModel instance with the updated object or error info
        """
        try:
            test_model = TestModel.objects.get(pk=id)
            test_model.title = title
            test_model.save()
            return UpdateTestModel(test_model=test_model,success=True,message="TestModel updated successfully")
        except TestModel.DoesNotExist:
            return UpdateTestModel(test_model=None,success=False,message="TestModel not found")
        except Exception as e:
            return UpdateTestModel(test_model=None,success=False,message=f"Error updating TestModel: {str(e)}")


class DeleteTestModel(graphene.Mutation):
    """
    Mutation to delete an existing TestModel instance.
    Takes an ID and removes the corresponding record from the database.
    """

    class Arguments:
        id = graphene.Int(required=True,description="The ID of the TestModel to delete")

    # Return fields
    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, id):
        """
        Delete a TestModel instance.

        Args:
            root: Root value (usually None)
            info: GraphQL execution info
            id: Primary key of the TestModel to delete

        Returns:
            DeleteTestModel instance with success status and message
        """
        try:
            test_model = TestModel.objects.get(pk=id)
            test_model.delete()
            return DeleteTestModel(success=True,message="TestModel deleted successfully")
        except TestModel.DoesNotExist:
            return DeleteTestModel(success=False,message="TestModel not found")
        except Exception as e:
            return DeleteTestModel(success=False, message=f"Error deleting TestModel: {str(e)}")


class Mutation(graphene.ObjectType):
    """
    Root Mutation class that defines all available GraphQL mutations.
    This class registers all mutation fields that can be executed.
    """
    # CRUD operations for TestModel
    create_test_model = CreateTestModel.Field()
    update_test_model = UpdateTestModel.Field()
    delete_test_model = DeleteTestModel.Field()


# Main GraphQL schema that combines queries and mutations
# This is the entry point for all GraphQL operations
schema = graphene.Schema(query=Query,mutation=Mutation)

