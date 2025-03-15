from django.test import TestCase, Client
from apps.main.models import CV, Skill, CVSkill


class CVListViewTests(TestCase):
    def setUp(self):
        # Initialize test client
        self.client = Client()
        # Use the actual URL path instead of the name to avoid conflicts with the API URLs
        self.list_url = '/'
        
        # Create test CV instances
        self.cv1 = CV.objects.create(
            firstname="Тарас",
            lastname="Шевченко",
            title="Full Stack Developer",
            summary="Test summary 1",
            bio="Test bio 1"
        )
        
        self.cv2 = CV.objects.create(
            firstname="Леся",
            lastname="Українка",
            title="UI/UX Designer",
            summary="Test summary 2",
            bio="Test bio 2"
        )
        
        # Create skills and link them to CVs
        self.skill1 = Skill.objects.create(name="Python")
        self.skill2 = Skill.objects.create(name="JavaScript")
        
        CVSkill.objects.create(cv=self.cv1, skill=self.skill1, level="expert")
        CVSkill.objects.create(cv=self.cv1, skill=self.skill2, level="intermediate")
        CVSkill.objects.create(cv=self.cv2, skill=self.skill2, level="expert")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/cv_list.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_context_data(self):
        response = self.client.get(self.list_url)
        self.assertTrue('cvs' in response.context)
        self.assertEqual(len(response.context['cvs']), 2)

    def test_cv_list_content(self):
        response = self.client.get(self.list_url)
        self.assertContains(response, "Тарас Шевченко")
        self.assertContains(response, "Леся Українка")
        self.assertContains(response, "Full Stack Developer")
        self.assertContains(response, "UI/UX Designer")
        self.assertContains(response, "Test summary 1")
        self.assertContains(response, "Test summary 2")

    def test_skills_display(self):
        response = self.client.get(self.list_url)
        self.assertContains(response, "Python")
        self.assertContains(response, "JavaScript")

    def test_empty_cv_list(self):
        # Remove all CVs to test empty state
        CV.objects.all().delete()
        response = self.client.get(self.list_url)
        self.assertContains(response, "No CVs available yet")

    def test_cv_list_ordering(self):
        cvs = self.client.get(self.list_url).context['cvs']
        # Check if CVs are ordered by updated_at in descending order
        self.assertTrue(all(cvs[i].updated_at >= cvs[i+1].updated_at 
                          for i in range(len(cvs)-1)))

    def test_prefetch_related_usage(self):
        # Expected queries:
        # 1. Main query for CV objects
        # 2. Query for CVSkill relations
        # 3. Query for Project relations
        # 4. Query for Contact relations
        # 5. Query for related Skill objects (needed for template rendering)
        with self.assertNumQueries(5):
            response = self.client.get(self.list_url)
            # Force evaluation of querysets and related objects
            for cv in response.context['cvs']:
                list(cv.skills.all())
                list(cv.projects.all())
                list(cv.contacts.all())
