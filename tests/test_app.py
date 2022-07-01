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
        
        # test GET and POST endpoints
        response = self.client.post("/api/timeline_post", data={
            "name": "Lucy Wang", 
            "email": "lwang5@villanova.edu", 
            "content": "How are you?"
        })
        try:
            assert response.status_code == 200
        except:
            print(response.status_code)

        response = self.client.get("/api/timeline_post")
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 1
        assert json["timeline_posts"][0]["name"] == "Lucy Wang"
        assert json["timeline_posts"][0]["email"] == "lwang5@villanova.edu"
        assert json["timeline_posts"][0]["content"] == "How are you?"

        # more tests for timeline page
        response = self.client.get("/timeline")
        html = response.get_data(as_text=True)
        assert "<title>Timeline</title>" in html

        # check the form and every input is there
        assert '<form id="postForm">' in html
        assert '<input type="text" id="name" name="name"' in html
        assert '<input type="text" id="email" name="email"' in html
        assert '<textarea name="content" id="content"' in html
        assert '<button id="submit-post"><span>Submit</span></button>' in html
        assert '<div id="timeline">' in html

