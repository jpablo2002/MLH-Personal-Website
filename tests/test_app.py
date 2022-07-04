import unittest
import os
os.environ['TESTING'] = 'true'
from flask import template_rendered # signal to use to make sure templates are rendered with variables

from app import app

# context manager to determine which templates were rendered and what variables were passed to the template
# the record function is attached to the template_rendered signal
# adds a template to a list and returns that along with the variables used with that template
def captured_templates(app, recorded, **extra):
    def record(sender, template, context):
        recorded.append((template, context))
    return template_rendered.connected_to(record, app)

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        templates = []
        with captured_templates(app, templates):
            response = app.test_client().get('/')
            assert response.status_code == 200

            # template tests
            assert len(templates) == 1
            template, context = templates[0]

            self.assertIsNotNone(template.name)
            assert template.name == 'juan.html'

            template_vars = [
                'title',
                'name',
                'university',
                'member',
                'linkedin',
                'github',
                'degree',
                'years',
                'activities',
                'skills',
                'about',
                'seal',
                'firstname',
            ]

            for var in template_vars:
                assert context[var] != ''

            html = response.get_data(as_text=True)

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

            # test side menu (div) exists
            assert '<div class="slide-menu">' in html

            # test side menu has nav links
            nav_links = [
                'profile',
                'about-edu',
                'experiences',
                'projects',
                'skills',
                'hobbies',
                'locations',
            ]
            for link in nav_links:
                assert '<li class="nav__link"><a href="#' + link + '">' in html

            page_links = [
                'timeline',
            ]
            for link in page_links:
                assert '<li class="page__link"><a href="/' + link + '">' in html


    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0 # assuming we are using a clean db
        # if ^ returns an error, likely means one of the other tests didn't work properly
        
        # test GET and POST endpoints
        response = self.client.post("/api/timeline_post", data={
            "name": "Lucy Wang", 
            "email": "lwang5@villanova.edu", 
            "content": "How are you?"
        })
        
        assert response.status_code == 200

        response = self.client.get("/api/timeline_post")
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 1
        assert json["timeline_posts"][0]["name"] == "Lucy Wang"
        assert json["timeline_posts"][0]["email"] == "lwang5@villanova.edu"
        assert json["timeline_posts"][0]["content"] == "How are you?"

        # more tests for timeline page
        templates = []
        with captured_templates(app, templates):
            response = self.client.get("/timeline")
            assert response.status_code == 200

            # template tests
            assert len(templates) == 1
            template, context = templates[0]

            self.assertIsNotNone(template.name)
            assert template.name == 'timeline.html'

            template_vars = [
                'title',
            ]
            for var in template_vars:
                assert context[var] != ''

            html = response.get_data(as_text=True)

            # check the form and every input is there
            assert '<form id="postForm">' in html
            assert '<input type="text" id="name" name="name"' in html
            assert '<input type="text" id="email" name="email"' in html
            assert '<textarea name="content" id="content"' in html
            assert '<button id="submit-post"><span>Submit</span></button>' in html

            # check the timeline div is there
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
        response_text = response.get_data(as_text=True)
        assert "Invalid name: missing" in response_text

        # POST request empty name
        response  = self.client.post("/api/timeline_post", data=
            {
                "name": "",
                "email": "john@example.com",
                "content": "Hello World, I'm John!",
            }
        )
        assert response.status_code == 400
        response_text = response.get_data(as_text=True)
        assert "Invalid name: empty" in response_text

        # POST request with missing content
        response  = self.client.post("/api/timeline_post", data=
            {
                "name": "John Doe",
                "email": "john@example.com",
            }
        )
        assert response.status_code == 400
        response_text = response.get_data(as_text=True)
        assert "Invalid content: missing" in response_text
        
        # POST request with empty content
        response  = self.client.post("/api/timeline_post", data=
            {
                "name": "John Doe",
                "email": "john@example.com",
                "content": "",
            }
        )
        assert response.status_code == 400
        response_text = response.get_data(as_text=True)
        assert "Invalid content: empty" in response_text

        # POST request with missing email
        response  = self.client.post("/api/timeline_post", data=
            {
                "name": "John Doe",
                "content": "Hello World, I'm John!",
            }
        )
        assert response.status_code == 400
        response_text = response.get_data(as_text=True)
        assert "Invalid email: missing" in response_text

        # POST request with empty email
        response  = self.client.post("/api/timeline_post", data=
            {
                "name": "John Doe",
                "email": "",
                "content": "Hello World, I'm John!",
            }
        )
        assert response.status_code == 400
        response_text = response.get_data(as_text=True)
        assert "Invalid email: empty" in response_text

        # POST request with malformed email
        response  = self.client.post("/api/timeline_post", data=
            {
                "name": "John Doe",
                "email": "not-an-email",
                "content": "Hello World, I'm John!",
            }
        )
        assert response.status_code == 400
        response_text = response.get_data(as_text=True)
        assert "Invalid email: not an email" in response_text

