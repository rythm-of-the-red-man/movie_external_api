from django.test import TestCase
from django.test import Client
from movies.models import Movie, Comment
# Create your tests here.


class TestMoviesRoute (TestCase):
    # Not calling fixtures as external API data structure might change
    # if so, tests will pass but API won't work.
    def setUp(self):
        self.client = Client()

        # Populate db (checks if request valid after every record.)
        # easy case
        self.client.post(
            '/movies/', {'title': 'Babadook'})

        # choosen because got $ in box office
        self.client.post('/movies/', {'title': 'Sinister'})

        # multiple words title
        self.client.post(
            '/movies/', {'title': 'The Shining'})

    def test_correct_movie_post(self):
        response = self.client.post('/movies/', {'title': 'Rosemary’s Baby'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 6)

    def test_boxoffice_special_signs_sanitation(self):
        response = self.client.post('/movies/', {'title': 'Sinister'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 6)

    def test_made_up_movie_post(self):
        response = self.client.post(
            '/movies/', {'title': 'Made up movie that will never exists unless someone will make it'})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(response.json()), 2)
        self.assertTrue('Error' in response.json().keys())

    def test_simple_movie_get(self):
        response = self.client.get('/movies/')
        self.assertEqual(len(response.json()), 3)
        self.assertTrue(response.status_code, 200)


class TestCommentsRoute(TestCase):

    def setUp(self):
        self.client = Client()
        # Populates DB.
        self.client.post(
            '/movies/', {'title': 'Halloween'})
        self.client.post(
            '/movies/', {'title': 'Jaws'})
        self.client.post(
            '/movies/', {'title': 'The Thing'})

    def test_db_population(self):
        response = self.client.get('/movies/')
        self.assertEqual(len(response.json()), 3)
        self.assertTrue(response.status_code, 200)

    def test_comment_post_route(self):
        commentary_text = 'This is spooky scary movie :ooo'
        the_thing_movie = Movie.objects.filter(title='The Thing').first()
        response = self.client.post(
            '/comments/', {'comment': commentary_text, "movie": the_thing_movie.id})
        response_data = response.json()
        self.assertEqual(response_data['movie'], the_thing_movie.id)
        self.assertEqual(response_data['comment'], commentary_text)
        self.assertTrue(response.status_code, 200)

    def test_invalid_comment_post_route(self):
        response = self.client.post('/comments/')
        response_data = response.json()
        self.assertTrue(response.status_code, 400)
        self.assertTrue('movie' in response.json().keys())
        self.assertTrue('comment' in response.json().keys())

    def test_comment_get_route(self):
        # Populate db
        jaws_movie = Movie.objects.filter(title='Jaws').first()
        comments = ['Sharkz are spooky :c',
                    'So many people eaten, like that!',
                    'This is stupid']
        for comment in comments:
            Comment(movie=jaws_movie, comment=comment).save()

        # Get comments from api, and from db
        response = self.client.get('/comments/')
        response_data = response.json()
        comments_amount_in_db = Comment.objects.count()
        comment_values_from_response = [
            comm['comment'] for comm in response_data]

        self.assertEqual(comments_amount_in_db, 3)
        self.assertTrue(len(response_data), 3)
        self.assertTrue(response.status_code, 200)
        for comment in comments:
            self.assertTrue(comment in comment_values_from_response)


class TestTopRoute(TestCase):

    def setUp(self):
        def populate_comments(movie_title, amount):
            counter = 0
            movie = Movie.objects.filter(title=movie_title).first()
            while counter < amount:
                Comment(movie=movie, comment='test').save()
                counter += 1
            return

        self.client = Client()
        # Populates DB.
        self.client.post(
            '/movies/', {'title': 'Halloween'})
        self.client.post(
            '/movies/', {'title': 'Jaws'})
        self.client.post(
            '/movies/', {'title': 'The Thing'})

        populate_comments('Halloween', 10)
        populate_comments('Jaws', 3)
        populate_comments('The Thing', 10)

    def test_top_route_valid_get(self):
        response = self.client.get('/top/', {
            'date_start': '2018-09-11',
            'date_end': '2020-09-11'
        })
        response_data = response.json()
        self.assertEqual(response_data[0]['ranking'], 1)
        self.assertEqual(response_data[1]['ranking'], 1)
        self.assertEqual(response_data[2]['ranking'], 2)

    def test_date_range_sort(self):
        # change date for The Thing comments
        comments = Movie.objects.filter(
            title='The Thing').first().comment_set.all()
        comments.update(date_of_creation='1995-10-21')

        # get top  without old comments
        response = self.client.get('/top/', {
            'date_start': '2018-09-11',
            'date_end': '2020-09-11'
        })
        response_data = response.json()
        self.assertEqual(response_data[0]['ranking'], 1)
        self.assertEqual(response_data[1]['ranking'], 2)
        # last one should have 0 comments in selected period
        self.assertEqual(response_data[2]['ranking'], 3)
        self.assertEqual(response_data[2]['total_comments'], 0)
