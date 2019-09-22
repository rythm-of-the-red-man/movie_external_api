from rest_framework import serializers
from movies.models import Movie, ImdbInfo, Staff, MarketingInfo, Timeline, Rating,Comment
from time import strftime


class MovieSerialier (serializers.Serializer):

    title = serializers.CharField(max_length=128)

    def create(self, validated_data):
        return validated_data


class ImdbInfoSeriaize(serializers.ModelSerializer):

    class Meta:
        model = ImdbInfo
        fields = ['imdbrating', 'imdbvotes', 'imdbid', 'metascore']


class MovieExternalApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id','title', 'runtime', 'genre',
                  'plot', 'language', 'country', 'type']


class StaffExternalApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['director', 'writer', 'actors', ]


class TimelineExternalApiSerializer(serializers.ModelSerializer):
    year = serializers.DateField(
        input_formats=[r'%Y'], required=False, allow_null=True)
    released = serializers.DateField(
        input_formats=[r'%d %b %Y'], required=False, allow_null=True)
    dvd = serializers.DateField(
        input_formats=[r'%d %b %Y'], required=False, allow_null=True)

    class Meta:
        model = Timeline
        fields = ['year', 'released', 'dvd', ]


class MarketingInfoExternalApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingInfo
        fields = ['boxoffice', 'production',
                  'website', 'poster', 'rated', 'awards']


class RatingExternalApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['source', 'value']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields=['movie','comment']

class TopSerializer(serializers.Serializer):
    date_start = serializers.DateField(style='input.html')
    date_end = serializers.DateField()
