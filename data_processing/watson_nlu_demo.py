import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as features


natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2017-02-27',
    username='0db91844-fcf1-4cfb-9575-7b6a667ed1f2',
    password='J5qwraJbMPuA')

response = natural_language_understanding.analyze(
    text='Bruce Banner is the Hulk and Bruce Wayne is BATMAN! '
         'Superman fears not Banner, but Wayne.',
    features=[features.Entities(), features.Keywords()])

print(json.dumps(response, indent=2))
