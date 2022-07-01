import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Juan Acosta</title>" in html
        # TODO add more tests relating to home page

        # test homepage has about section
        assert '<div class="about">' in html

        # test homepage has education section 
        assert '<div class="edu">' in html

        # test homepage has work experience section
        assert '<section class="experiences-container"' in html

        # test homepage has projects section
        assert '<section class="projects-container"' in html

        # test homepage has skills section
        assert '<section class="skills-container"' in html

        # test homepage has hobbies section
        assert '<section class="hobbies-container"' in html

        # test homepage has map section
        assert '<section class="map"' in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0 # assuming we are using a clean db
        
        # TODO test GET and POST endpoints
        response = self.client.post("/api/timeline_post", )
        assert response.status_code == 200


        # TODO more tests for timeline page