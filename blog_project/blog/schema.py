import graphene
from graphene_django import DjangoObjectType
from .models import Post, Comment


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = "__all__"


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = "__all__"


class PostInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    content = graphene.String(required=True)


class CommentInput(graphene.InputObjectType):
    post_id = graphene.Int(required=True, name="postId")
    author = graphene.String(required=True)
    content = graphene.String(required=True)


class CreatePost(graphene.Mutation):
    class Arguments:
        input = PostInput(required=True)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, input):
        post = Post(
            title=input.title,
            content=input.content
        )
        post.save()
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = PostInput(required=True)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, id, input):
        post = Post.objects.get(pk=id)
        post.title = input.title
        post.content = input.content
        post.save()
        return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        post = Post.objects.get(pk=id)
        post.delete()
        return DeletePost(success=True)


class CreateComment(graphene.Mutation):
    class Arguments:
        input = CommentInput(required=True)

    comment = graphene.Field(CommentType)

    @classmethod
    def mutate(cls, root, info, input):
        post = Post.objects.get(pk=input.post_id)
        comment = Comment(
            post=post,
            author=input.author,
            content=input.content
        )
        comment.save()
        return CreateComment(comment=comment)


class UpdateComment(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = CommentInput(required=False)  # Make optional for partial updates

    comment = graphene.Field(CommentType)

    @classmethod
    def mutate(cls, root, info, id, input=None):
        comment = Comment.objects.get(pk=id)
        if input:
            if input.author:
                comment.author = input.author
            if input.content:
                comment.content = input.content
            if input.post_id:
                comment.post = Post.objects.get(pk=input.post_id)
        comment.save()
        return UpdateComment(comment=comment)


class DeleteComment(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        comment = Comment.objects.get(pk=id)
        comment.delete()
        return DeleteComment(success=True)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    create_comment = CreateComment.Field()
    update_comment = UpdateComment.Field()
    delete_comment = DeleteComment.Field()


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post_by_id = graphene.Field(PostType, id=graphene.Int())
    comments_by_post = graphene.List(CommentType, post_id=graphene.Int())

    def resolve_all_posts(root, info):
        return Post.objects.all()

    def resolve_post_by_id(root, info, id):
        return Post.objects.get(pk=id)

    def resolve_comments_by_post(root, info, post_id):
        return Comment.objects.filter(post_id=post_id)


schema = graphene.Schema(query=Query, mutation=Mutation)