from django.test import TestCase
from sign.models import Event, Guest

# Create your tests here.


class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=1, name="小米发布会", status=True, limit=20000, address='深圳',
                             start_time='2019-08-22 15:16:19')
        Guest.objects.create(id=1, event_id=1, realname='alen',
                             phone='13711001101', email='alen@mail.com', sign=False)

    def test_event_models(self):
        result = Event.objects.get(name="小米发布会")
        self.assertEqual(result.address, "深圳")
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone='13711001101')
        self.assertEqual(result.realname, "alen")
        self.assertFalse(result.sign)
