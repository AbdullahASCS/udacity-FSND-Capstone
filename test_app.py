import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
ASSISTANT_TOKEN = os.getenv('ASSISTANT_TOKEN')
PRODUCER_TOKEN = os.getenv('PRODUCER_TOKEN')

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app.""" 
        self.database_name = "capstone_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(os.getenv("database_user"),
                                                               os.getenv("database_password"),os.getenv("DATABASE_URL"), self.database_name)
        self.app = create_app(self.database_path)
        self.client = self.app.test_client

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_actor_200(self):
        res = self.client().get('/actors/5', headers={"content-type:": "application/json","Authorization": f"Bearer {ASSISTANT_TOKEN}"})
        self.assertEqual(res.status_code, 200)
    def test_get_actor_200_RBAC(self):
        res = self.client().get('/actors/5', headers={"content-type:": "application/json","Authorization": f"Bearer {PRODUCER_TOKEN}"})
        self.assertEqual(res.status_code, 200)
    def test_get_actor_404(self):
        res = self.client().get('/actors/100', headers={"content-type:": "application/json","Authorization": f"Bearer {ASSISTANT_TOKEN}"})
        self.assertEqual(res.status_code, 404) 
    def test_get_movie_200(self):
        res = self.client().get('/movies/6', headers={"content-type:": "application/json","Authorization": f"Bearer {ASSISTANT_TOKEN}"})
        self.assertEqual(res.status_code, 200)
    def test_get_movie_404(self):
        res = self.client().get('/movies/100', headers={"content-type:": "application/json","Authorization": f"Bearer {ASSISTANT_TOKEN}"})
        self.assertEqual(res.status_code, 404)
    def test_post_movie_405_RBAC(self):
        res = self.client().post('/movies', headers={"content-type:": "application/json","Authorization": f"Bearer {ASSISTANT_TOKEN}"},json={
        "title":"random4",
        "release_date": "12-12-2006",
        "actors_id": [1,3,4]
})
        self.assertEqual(res.status_code, 403)
    def test_post_movie_200_RBAC(self):
        res = self.client().post('/movies', headers={"content-type:": "application/json","Authorization": f"Bearer {PRODUCER_TOKEN}"},json={
        "title":"random4",
        "release_date": "12-12-2006",
        "actors_id": [1,3,4]
})
        self.assertEqual(res.status_code, 200)

    def test_patch_movie_404(self):
        res = self.client().patch('/movies/1', headers={"content-type:": "application/json","Authorization": f"Bearer {PRODUCER_TOKEN}"},json={
        "title":"random4",
        "release_date": "12-12-2006",
        "actors_id": [1,3,100]
})
        self.assertEqual(res.status_code, 404)
    def test_patch_movie_200(self):
        res = self.client().patch('/movies/5', headers={"content-type:": "application/json","Authorization": f"Bearer {PRODUCER_TOKEN}"},json={
        "title":"random4",
        "release_date": "12-12-2006",
        "actors_id": [1,3,4]
})
        self.assertEqual(res.status_code, 200)
    def test_delete_movie_404(self):
        res = self.client().delete('/movies/100', headers={"content-type:": "application/json","Authorization": f"Bearer {PRODUCER_TOKEN}"})
        self.assertEqual(res.status_code, 404)
    def test_delete_movie_200_RBAC(self):
        res = self.client().delete('/movies/9', headers={"content-type:": "application/json","Authorization": f"Bearer {PRODUCER_TOKEN}"})
        self.assertEqual(res.status_code, 200)
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
