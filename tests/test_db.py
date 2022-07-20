import unittest
from app import TimelinePost
from peewee import *

MODELS = [TimelinePost]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()

    def test_timeline_db_creates_correct_data(self):
        first_post = TimelinePost.create(
            name="Lucy Wang", 
            email="lwang5@villanova.edu",
            content="Test posting to timeline DB"
        )
        second_post = TimelinePost.create(
            name="Billy Bob",
            email="bob@gmail.com",
            content="Test posting to timeline DB #2"
        )

        assert first_post.id == 1
        assert second_post.id == 2
        self.assertIsNotNone(first_post.created_at)
        self.assertIsNotNone(second_post.created_at)

        posts = TimelinePost.select()
        posts = [
            {
                'id': post.id, 
                'name': post.name, 
                'email': post.email,
                'content': post.content
            } for post in posts
        ]

        assert posts == [
            {
                'id': 1,
                'name': "Lucy Wang",
                'email': "lwang5@villanova.edu",
                'content': "Test posting to timeline DB"
            },
            {
                'id': 2,
                'name': "Billy Bob",
                'email': "bob@gmail.com",
                'content': "Test posting to timeline DB #2"
            }
        ]
    
