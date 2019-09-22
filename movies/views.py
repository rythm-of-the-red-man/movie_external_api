from django.shortcuts import render
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

# App imports
from movies.serializers import ImdbInfoSeriaize, MovieExternalApiSerializer
from movies.serializers import StaffExternalApiSerializer, MarketingInfoExternalApiSerializer
from movies.serializers import RatingExternalApiSerializer, TimelineExternalApiSerializer, MovieSerialier
from movies.serializers import CommentSerializer, TopSerializer
from movies.models import ImdbInfo, Staff, Movie, MarketingInfo, Timeline, Rating, Comment
from movies.movie_service import MovieService

from recruitment.settings import MOVIES_API as url
from recruitment.settings import MOVIES_APIKEY as api_key


from math import inf

# Django rest framework imports
from rest_framework import views, viewsets
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

def home(request):
    return render(request,'movies/index.html')

class MovieView(views.APIView):

    authentication_classes = [authentication.SessionAuthentication]


    def post(self, request):
        # Get title from service API
        service_api_serializer = MovieSerialier(data=request.data)
        if not service_api_serializer.is_valid():
            return Response({'title': 'Not valid title provided!'}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize Service locator class and get data from external API
        movie_service = MovieService(api_key, url)

        data = movie_service.get_movie(service_api_serializer.data['title'])

        print(data)
        # run ModelSerializers, save models if all pass
        serializers = {
            'movie': MovieExternalApiSerializer(data=data),
            'imdbinfo': ImdbInfoSeriaize(data=data),
            'staff': StaffExternalApiSerializer(data=data),
            'marketinginfo': MarketingInfoExternalApiSerializer(data=data),
            'timeline': TimelineExternalApiSerializer(data=data),
            'ratings': [RatingExternalApiSerializer(data=rating) for rating in data['ratings']],
        }
        errors = {}
        for name, serializer in serializers.items():
            if name != 'ratings':
                if not serializer.is_valid():
                    errors.update(serializer.errors)
            else:
                for rating_serializer in serializer:
                    if not rating_serializer.is_valid():
                        errors.update(rating_serializer.errors)

        if not errors:
            movie = serializers['movie'].save()
            ImdbInfo(movie=movie, **
                     serializers['imdbinfo'].validated_data).save()
            Staff(movie=movie, **serializers['staff'].validated_data).save()
            MarketingInfo(
                movie=movie, **serializers['marketinginfo'].validated_data).save()
            Timeline(movie=movie, **
                     serializers['timeline'].validated_data).save()
            for rating in serializers['ratings']:
                Rating(movie=movie, **rating.validated_data).save()
        else:
            return Response({'Errors': errors, 'message': 'Errors occured during data retrieveing!'})
        # Return record from database to user.
        return Response({
            'Movie Details': MovieExternalApiSerializer(movie).data,
            'Staff Details': StaffExternalApiSerializer(movie.staff).data,
            'Timeline': TimelineExternalApiSerializer(movie.timeline).data,
            'Marketing Info': MarketingInfoExternalApiSerializer(movie.marketinginfo).data,
            'Imdb Info': ImdbInfoSeriaize(movie.imdbinfo).data,
            'Ratings': [RatingExternalApiSerializer(rating).data for rating in movie.rating_set.all()],
        })

    def get(self, request):
        movies = Movie.objects.all()
        result = []

        for movie in movies:
            result.append({
                'Movie Details': MovieExternalApiSerializer(movie).data,
                'Staff Details': StaffExternalApiSerializer(movie.staff).data,
                'Timeline': TimelineExternalApiSerializer(movie.timeline).data,
                'Marketing Info': MarketingInfoExternalApiSerializer(movie.marketinginfo).data,
                'Imdb Info': ImdbInfoSeriaize(movie.imdbinfo).data
            })

        return Response(result)


class CommentView(views.APIView):

    authentication_classes = [authentication.SessionAuthentication]


    def post(self, request):
        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            comment = comment_serializer.save()
            return Response(CommentSerializer(comment).data)
        else:
            return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        movie_id = request.query_params.get('movie_id')
        if movie_id:
            comments = Comment.objects.filter(movie=movie_id)
        else:
            comments = Comment.objects.all()

        response = CommentSerializer(comments, many=True).data
        return Response(response)


class TopView(views.APIView):

    authentication_classes = [authentication.SessionAuthentication]


    def get(self, request):
        serializer = TopSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors)

        query = Movie.objects.annotate(comments_count=Count('comment',
                                                            filter=Q(comment__date_of_creation__gt=serializer.validated_data['date_start'],
                                                                     comment__date_of_creation__lt=serializer.validated_data['date_end']))
                                       ).order_by('-comments_count')
        result = []
        ranking = 0
        comparitor = inf
        for q in query:
            if q.comments_count < comparitor:
                comparitor = q.comments_count
                ranking += 1
            result.append({'movie_id': q.id,
                           'total_comments': q.comments_count,
                           'ranking': ranking})
        return Response(result)

