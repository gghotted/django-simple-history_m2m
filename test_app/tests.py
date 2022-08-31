from django.test import TestCase

from test_app.models import NoHistory, Person, Post


class TrackManyToManyFieldTestCase(TestCase):
    def setUp(self):
        self.person = Person.objects.create()
        self.post = Post.objects.create()
    
    def test_track(self):
        self.person.like_posts.add(self.post)
        self.assertEqual(self.person.like_posts.count(), 1)
        self.assertEqual(len(Person.objects.first().like_posts_list), 1)
        self.assertEqual(
            set(Person.objects.first().history.first().updated_fields),
            {'like_posts'},
        )

    def test_no_prev(self):
        self.assertEqual(self.person.history.first().updated_fields, [])

    def test_no_history_m2m(self):
        obj = NoHistory.objects.create()
        obj.like_posts.add(self.post)
