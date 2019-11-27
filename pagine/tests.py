from datetime import datetime
from django.test import TestCase
from .models import (CourseSchedule, Location, ImageEntry)

class CourseScheduleTestCase(TestCase):
    def setUp(self):
        CourseSchedule.objects.create(full="Lunedì 16:00", abbrev="1-LU16")

    def test_name(self):
        """Name is correctly identified"""
        orario = CourseSchedule.objects.get(abbrev="1-LU16")
        self.assertEqual(orario.__str__(), 'Lunedì 16:00')

class LocationTestCase(TestCase):
    #@classmethod
    #def setUpTestData(cls):
    def setUp(self):
        # Set up data for the whole TestCase
        #cls.img = ImageEntry.objects.create(name='IMG', image='image.jpg',
            #thumb='image_thumb.jpg',
            #description = 'Description')
        Location.objects.create(title="Marco",
            #image = cls.img,
            address="Via Agnelli",
            gmap_link = 'https://goo.gl/maps/jLKe3iur2EtL8zuB7',
            gmap_embed = '<scrap>https://goo.gl/maps/jLKe3iur2EtL8zuB7</scrap>',
            body = 'Body')

    def test_name(self):
        """Name is correctly identified"""
        luogo = Location.objects.get(title="Marco")
        self.assertEqual(luogo.__str__(), 'Marco')

    def test_link(self):
        """Link is correctly identified"""
        luogo = Location.objects.get(title="Marco")
        self.assertEqual(luogo.get_gmap_link(),
            '<a href="https://goo.gl/maps/jLKe3iur2EtL8zuB7" class="btn" target="_blank">Mappa</a>')

    def test_thumb(self):
        """Thumbnail is correctly identified"""
        luogo = Location.objects.get(title="Marco")
        self.assertEqual(luogo.get_thumb(),
            '')
