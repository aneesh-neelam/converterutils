from django.test import TestCase

from .models import NumberSystem, NumberSystemConversion


class NumberSystemModelsTest(TestCase):
    def create_number_systems(self):
        NumberSystem.objects.create(name='Western', locale='en-US')
        NumberSystem.objects.create(name='Indian', locale='en-IN')

    def create_number_system_conversions(self):
        NumberSystemConversion.objects.create(system_id='Western', value=1000000, name='Million',
                                              synonyms=NumberSystemConversion.serialize_synonyms(
                                                  ['M', 'MM', 'mn', 'Mega']))
        NumberSystemConversion.objects.create(system_id='Western', value=1000000000, name='Billion',
                                              synonyms=NumberSystemConversion.serialize_synonyms(
                                                  ['B', 'G', 'bn', 'Giga', 'Milliard']))
        NumberSystemConversion.objects.create(system_id='Western', value=1000000000000, name='Trillion',
                                              synonyms=NumberSystemConversion.serialize_synonyms(['T', 'tn', 'Tera']))
        NumberSystemConversion.objects.create(system_id='Western', value=1000000000000000, name='Quadrillion',
                                              synonyms=NumberSystemConversion.serialize_synonyms(['Q', 'qn', 'Peta']))
        NumberSystemConversion.objects.create(system_id='Indian', value=100000, name='Lakh',
                                              synonyms=NumberSystemConversion.serialize_synonyms(['L', 'Lac', 'lakṣa']))
        NumberSystemConversion.objects.create(system_id='Indian', value=10000000, name='Crore',
                                              synonyms=NumberSystemConversion.serialize_synonyms(['cr', 'koṭi']))

    def delete_number_system_conversions(self):
        NumberSystemConversion.objects.all().delete()

    def delete_number_systems(self):
        NumberSystem.objects.all().delete()

    def setUp(self):
        self.create_number_systems()
        self.create_number_system_conversions()

    def test_number_system_models(self):
        # Test number of number systems in Database
        number_systems = NumberSystem.objects.all()
        self.assertEqual(number_systems.count(), 2)

        # Test number of number system conversion entries in Database
        number_system_conversions = NumberSystemConversion.objects.all()
        self.assertEqual(number_system_conversions.count(), 6)

        # Get all Number System conversions in Western system
        conversions_for_western = NumberSystemConversion.objects.filter(system_id='Western')
        self.assertEqual(conversions_for_western.count(), 4)
        # Verify Serialization and Deserialization
        self.assertEqual(
            len(NumberSystemConversion.deserialize_synonyms(conversions_for_western.get(name='Million').synonyms)), 4)
        self.assertEqual(
            len(NumberSystemConversion.deserialize_synonyms(conversions_for_western.get(name='Billion').synonyms)), 5)
        self.assertEqual(
            len(NumberSystemConversion.deserialize_synonyms(conversions_for_western.get(name='Trillion').synonyms)), 3)
        self.assertEqual(
            len(NumberSystemConversion.deserialize_synonyms(conversions_for_western.get(name='Quadrillion').synonyms)),
            3)

        # Get all Number System conversions in Indian system
        conversions_for_indian = NumberSystemConversion.objects.filter(system_id='Indian')
        self.assertEqual(conversions_for_indian.count(), 2)
        # Verify Serialization and Deserialization
        self.assertEqual(
            len(NumberSystemConversion.deserialize_synonyms(conversions_for_indian.get(name='Lakh').synonyms)), 3)
        self.assertEqual(
            len(NumberSystemConversion.deserialize_synonyms(conversions_for_indian.get(name='Crore').synonyms)), 2)

    def tearDown(self):
        self.delete_number_system_conversions()
        self.delete_number_systems()
