import json
from http import HTTPStatus

from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog.models import Post
from blog.api.serializers import PostSerializer

@api_view(["GET", "POST"])
@csrf_exempt
def post_list(request, format=None):
    if request.method == "GET":
        posts = Post.objects.all()
        return Response({"data": PostSerializer(posts, many=True).data})
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=HTTPStatus.CREATED,
            headers={"Location": reverse("api_post_detail", args=(post.pk,))},
        )

    return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@csrf_exempt
def post_detail(request, pk, format=None):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=HTTPStatus.NOT_FOUND)

    if request.method == "GET":
        return Response(PostSerializer(post).data)

    elif request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=HTTPStatus.NO_CONTENT)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
      
    elif request.method == "DELETE":
        post.delete()
        return Response(status=HTTPStatus.NO_CONTENT)