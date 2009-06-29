import djapian

from turbion.core.blogs.models import Post, Comment

class PostIndexer(djapian.Indexer):
    fields = ("text",)
    tags = [
        ("status", "status"),
        ("title",  "title"),
        ("author", "created_by"),
        ("date",   "created_on"),
    ]
    trigger = lambda indexer, post: post.is_published

class CommentIndexer(djapian.Indexer):
    fields = ("text",)
    tags = [
        ("author", "created_by"),
    ]

djapian.add_index(Post, PostIndexer, attach_as="indexer")
djapian.add_index(Comment, CommentIndexer, attach_as="indexer")
