from rest_framework.test import APITestCase
from rest_framework import status
from apps.main.models import CV, Skill
from datetime import date


class CVAPITests(APITestCase):
    def setUp(self):
        # Create test skill
        self.skill = Skill.objects.create(name="Python")
        self.skill2 = Skill.objects.create(name="Django")
        
        # Initial CV data for create test
        self.cv_data = {
            "firstname": "John",
            "lastname": "Doe",
            "bio": "Web developer with 5 years of experience",
            "title": "Senior Developer",
            "summary": "Experienced in Django and React",
            "skills": [
                {
                    "skill_id": self.skill.id,
                    "level": "expert"
                }
            ],
            "contacts": [
                {
                    "type": "email",
                    "value": "john@example.com"
                },
                {
                    "type": "github",
                    "value": "johndoe"
                }
            ],
            "projects": [
                {
                    "name": "Portfolio Website",
                    "description": "Personal portfolio website",
                    "technologies": "Django, Bootstrap",
                    "start_date": "2023-01-01",
                    "end_date": "2023-02-15",
                    "url": "https://example.com"
                }
            ]
        }
    
    def test_create_cv(self):
        """Test creating a CV with nested relationships"""
        url = '/api/cvs/'
        response = self.client.post(url, self.cv_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CV.objects.count(), 1)
        self.assertEqual(CV.objects.get().firstname, 'John')
        self.assertEqual(CV.objects.get().lastname, 'Doe')
        
        # Check nested relationships
        cv = CV.objects.get()
        self.assertEqual(cv.skills.count(), 1)
        self.assertEqual(cv.contacts.count(), 2)
        self.assertEqual(cv.projects.count(), 1)
        
        # Check skill details
        cv_skill = cv.skills.first()
        self.assertEqual(cv_skill.skill.name, 'Python')
        self.assertEqual(cv_skill.level, 'expert')
        
        # Check project details
        project = cv.projects.first()
        self.assertEqual(project.name, 'Portfolio Website')
        self.assertEqual(project.start_date, date(2023, 1, 1))
    
    def test_get_cv_list(self):
        """Test retrieving a list of CVs"""
        # Create a CV first
        self.test_create_cv()
        
        url = '/api/cvs/'
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_get_cv_detail(self):
        """Test retrieving a single CV"""
        # Create a CV first
        response = self.client.post('/api/cvs/', self.cv_data, format='json')
        cv_id = response.data['id']
        
        url = f'/api/cvs/{cv_id}/'
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['firstname'], 'John')
        self.assertEqual(response.data['lastname'], 'Doe')
        
        # Check nested relationships
        self.assertEqual(len(response.data['skills']), 1)
        self.assertEqual(len(response.data['contacts']), 2)
        self.assertEqual(len(response.data['projects']), 1)
    
    def test_update_cv(self):
        """Test updating a CV"""
        # Create a CV first
        response = self.client.post('/api/cvs/', self.cv_data, format='json')
        cv_id = response.data['id']
        
        url = f'/api/cvs/{cv_id}/'
        
        # Data to update
        update_data = {
            "firstname": "Jane",
            "lastname": "Smith",
            "bio": "Full stack developer",
            "title": "Lead Developer",
            "summary": "Experienced in Django, React and Vue",
            "skills": [
                {
                    "skill_id": self.skill2.id,
                    "level": "advanced"
                }
            ],
            "contacts": [
                {
                    "type": "email",
                    "value": "jane@example.com"
                }
            ],
            "projects": [
                {
                    "name": "E-commerce Website",
                    "description": "Online shop",
                    "technologies": "Django, React",
                    "start_date": "2023-03-01",
                    "end_date": "2023-05-15",
                    "url": "https://shop.example.com"
                }
            ]
        }
        
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh the CV from the database
        cv = CV.objects.get(pk=cv_id)
        
        # Check updated data
        self.assertEqual(cv.firstname, 'Jane')
        self.assertEqual(cv.lastname, 'Smith')
        self.assertEqual(cv.title, 'Lead Developer')
        
        # Check updated relationships
        self.assertEqual(cv.skills.count(), 1)
        self.assertEqual(cv.skills.first().skill.name, 'Django')
        self.assertEqual(cv.skills.first().level, 'advanced')
        
        self.assertEqual(cv.contacts.count(), 1)
        self.assertEqual(cv.contacts.first().value, 'jane@example.com')
        
        self.assertEqual(cv.projects.count(), 1)
        self.assertEqual(cv.projects.first().name, 'E-commerce Website')
    
    def test_delete_cv(self):
        """Test deleting a CV"""
        # Create a CV first
        response = self.client.post('/api/cvs/', self.cv_data, format='json')
        cv_id = response.data['id']
        
        url = f'/api/cvs/{cv_id}/'
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CV.objects.count(), 0)