from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework.status import * # Good for HTTP descriptive consts

from .models import Video
from .serializers import VideoSerializer

# Create your views here.
@api_view(['GET'])
def all_videos(request):
    try:
        all_videos = Video.objects.all()
        serializer = VideoSerializer(all_videos, many=True) # many=True needed otherwise Django would think one item only
        return Response(serializer.data, status=HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": f"Can't get videos"}, status=HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_video(request):
    try:
        video_id = request.data.get('video_id')
        
        if not video_id:
            return Response({"error": "You must provide a video_id"}, status=HTTP_400_BAD_REQUEST)
        
        # video = get_object_or_404(Video, video_id=video_id)
        video = Video.objects.get(video_id=video_id)
        serializer = VideoSerializer(video)
        return Response({"success": serializer.data}, status=HTTP_200_OK)
    
    # TODO Video.DoesNotExist is not getting caught
    except Video.DoesNotExist:
        return Response({"error": "Video does not exist"}, status=HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"error": "Can't get video"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def add_video(request):
    try:
        serializer = VideoSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
        if Video.objects.filter(title__iexact=serializer.validated_data['title']).exists():
            return Response({"error": "Video already exists"}, status=HTTP_400_BAD_REQUEST)
            
        serializer.save()
        return Response({"success": "Video created successfully"}, status=HTTP_201_CREATED)
    
    except Exception as e:
        return Response({"error": f"Can't add video"}, status=HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def edit_video(request):
    try:
        video_id = request.data.get('video_id')
        existing_video = Video.objects.get(video_id=video_id)
        
        if not video_id:
            return Response({"error": "You must provide a video_id"}, status=HTTP_400_BAD_REQUEST)
        
        serializer = VideoSerializer(existing_video, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
        serializer.save()
        
        return Response({"success": serializer.data}, status=HTTP_200_OK)
    
    except Video.DoesNotExist:
        return Response({"error": "Video does not exist"}, status=HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"error": "Can't update video"}, status=HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def del_video(request):
    try:
        video_id = request.data.get('video_id')
        if not video_id:
            return Response({"error": "You must provide a video_id"}, status=HTTP_400_BAD_REQUEST)
        # video = get_object_or_404(Video, video_id=video_id)
        video = Video.objects.get(video_id=video_id)
        video.delete()
        return Response({"success": "Video was successfully deleted"}, status=HTTP_204_NO_CONTENT)
    except Video.DoesNotExist:
        return Response({"error": "Video does not exist"}, status=HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": "Can't delete video"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    