from django.http import HttpResponse
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import matplotlib.pyplot as plt


def main_view(request):  # главная
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        index: str = f.read()
        return HttpResponse(index, content_type="text/html; charset=utf-8")


def delete_department(latlng):
    less_dis = 999999.0
    less_id = latlng[0]
    for i in range(len(latlng)):
        current = latlng[i]
        distance = 0.0
        for j in range(len(latlng)):
            if j != i:
                distance += abs(current.latitude - latlng[j].latitude) + abs(current.longitude - latlng[j].longitude)
        if less_dis > distance:
            less_dis = distance
            less_id = current
    return less_id


@api_view(['GET', 'PUT', 'DELETE'])
def branch(request):
    if request.method == 'GET':
        branches = Branch.objects.all()
        serializer = Branch1Serializer(branches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        code = request.query_params['code']
        branch = Branch.objects.get(pk=code)
        branch.is_deleted = 0
        branch.save()
        return Response(status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        code = request.query_params['code']
        branch = Branch.objects.get(pk=code)
        branch.is_deleted = 1
        branch.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def deleted_branch(request):
    branches = Branch.objects.filter(is_deleted=1)
    serializer = Branch1Serializer(branches, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def candidates(request):
    branches = Branch.objects.raw('select max(pop) as pop, max(density) as density, city, count(*) as count, \
    count(*) / max(pop) * max(density) * 100 as rating, \
    max(code) as code from main_branch inner join main_city on main_branch.city = main_city.title \
    where is_deleted = 0 or is_deleted = null \
    group by city having count > 1 order by rating desc limit 5;')
    result = {'vonb': [], 'norm': []}
    for branch in branches:
        city = branch.city
        latlng = Branch.objects.filter(city=city, is_deleted__in=[0, None])
        vonb = delete_department(latlng)
        serializer_vonb = Branch1Serializer(vonb)
        serializer = Branch1Serializer(latlng, many=True)
        result['vonb'].append(serializer_vonb.data)
        result['norm'].append(serializer.data)
        x = []
        y = []
        c = []
        for point in serializer.data:
            if point['latitude'] == serializer_vonb.data['latitude'] and point['longitude'] == serializer_vonb.data['longitude']:
                c.append('r')
            else:
                c.append('g')
            x.append(point['latitude'])
            y.append(point['longitude'])
        fig, ax = plt.subplots()
        ax.scatter(x, y, c=c)
        image_path = 'static/' + str(branch.code) + '.png'
        plt.savefig(image_path)
        result['vonb'][-1]['image'] = image_path
    return Response(result, status=status.HTTP_200_OK)
