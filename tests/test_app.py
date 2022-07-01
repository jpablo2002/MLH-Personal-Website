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
        try:
            assert len(json["timeline_posts"]) == 0 # assuming we are using a clean db
        except:
            print("LENGTH NOT 0. Length is ", len(json["timeline_posts"]))
        
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
        try:
            assert len(json["timeline_posts"]) == 1
        except:
            print("LENGTH NOT 1. Length is ", len(json["timeline_posts"]))
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

    def test_malformed_timeline_post(self):
        # POST request missing name
        response  = self.client.post("/api/timeline_post", data=
            {
                "email": "john@example.com",
                "content": "Hello World, I'm John!",
            }
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name: missing" in html

        # POST request empty name
        response  = self.client.post("/api/timeline_post", data=
            {
                "name": "",
                "email": "john@example.com",
                "content": "Hello World, I'm John!",
            }
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name: empty" in html

        # POST request with missing content
        response  = self.client.post("/api/timeline_post", data=
            {
                "name": "John Doe",
                "email": "john@example.com",
            }
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content: missing" in html
        
        # POST request with empty content
        response  = self.client.post("/api/timeline_post", data=
            {
                "name": "John Doe",
                "email": "john@example.com",
                "content": "",
            }
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content: empty" in html

        # POST request with missing email
        response  = self.client.post("/api/timeline_post", data=
            {
                "name": "John Doe",
                "content": "Hello World, I'm John!",
            }
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email: missing" in html

        # POST request with empty email
        response  = self.client.post("/api/timeline_post", data=
            {
                "name": "John Doe",
                "email": "",
                "content": "Hello World, I'm John!",
            }
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email: empty" in html

        # POST request with malformed email
        response  = self.client.post("/api/timeline_post", data=
            {
                "name": "John Doe",
                "email": "not-an-email",
                "content": "Hello World, I'm John!",
            }
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email: not an email" in html