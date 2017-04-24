from rest_framework import serializers
from bailout.models import Bailout

class BailoutSerializer(serializers.ModelSerializer):

	class Meta:
		model = Bailout
		fields = ('name', 'party', 'vote_1', 'vote_2', 'switch', 'PAC', 'state', 'bailout_opposition', 'bailout_support') 
		