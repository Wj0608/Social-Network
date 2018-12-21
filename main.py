# encoding:utf-8
import csv
import math
import numpy as np
import random
from functools import reduce
import copy


def read_excel(adj, dep, deg):
    csv_file = csv.reader(open('adj.csv', 'r'))
    for i in csv_file:
        adj.append(i)
    csv_file = csv.reader(open('dep.csv', 'r'))
    for i in csv_file:
        dep.append(i)
    for i in range(0, 1005):
        temp = 0
        for j in range(0, 1005):
            if adj[i][j] == '1':
                temp += 1
        deg[i][i] = temp


def compute_cond(points):
    cnt = 0
    deg_cnt = 0
    deg_cnt2 = 0
    for x in range(1005):
        for y in range(1005):
            if adjacent_matrix[x][y] == '1':
                if x in points:
                    if y not in points:
                        cnt += 1
    for z in range(1005):
        if z in points:
            deg_cnt += degree[z][z]
        else:
            deg_cnt2 += degree[z][z]
    return cnt / (min(deg_cnt, deg_cnt2))


def l2_distance(a, b):
    sum = 0
    for i in range(20):
        sum += (a[i]-b[i])*(a[i]-b[i])
    return math.sqrt(math.sqrt(sum.real*sum.real+sum.imag*sum.imag))


if __name__ == '__main__':
    adjacent_matrix = []
    department = []
    degree = []
    for i in range(0, 1005):
        t = []
        for j in range(0, 1005):
            t.append(0)
        degree.append(t)
    read_excel(adjacent_matrix, department, degree)
    degree_np = np.array(degree, np.int64)
    adjacent_matrix_np = np.array(adjacent_matrix, np.int64)
    lap = degree_np - adjacent_matrix_np
    eigvalue = np.linalg.eig(lap)[0]
    eigvector = np.linalg.eig(lap)[1]
    conductance = []
    for i in range(5):
        points = []
        for j in range(1005):
            if random.randint(1, 1005) <= 500 and len(points) < 200:
                points.append(j)
        conductance.append(compute_cond(points))
    avg_cond = reduce(lambda x, y: x + y, conductance) / len(conductance)
    print(avg_cond)
    origin_eigvalue = copy.copy(eigvalue)
    eigvalue.sort()
    print(eigvalue[0:10])
    min_eigvector = 0
    min20_eigvector = []
    for j in range(20):
        for i in range(len(origin_eigvalue)):
            if origin_eigvalue[i] == eigvalue[j+1]:
                min20_eigvector.append(eigvector[i])
    for i in range(len(origin_eigvalue)):
        if origin_eigvalue[i] == eigvalue[1]:
            min_eigvector = eigvector[i]
    allpoints = []
    for i in range(1005):
        allpoints.append(i)
    sorted_points = sorted(allpoints, key=lambda x: min_eigvector[x])
    for i in range(99, 400):
        pick_points = sorted_points[0: i+1]
        t = compute_cond(pick_points)
        if t < avg_cond:
            break
    print(i, t)
    dim_vector = []
    for i in range(1005):
        temp = []
        for j in range(20):
            temp.append(min20_eigvector[j][i])
        dim_vector.append(temp)
    distance_list = []
    for i in range(1005):
        if i != 0:
            distance = l2_distance(dim_vector[0], dim_vector[i])
        else:
            distance = 0
        distance_list.append(distance)
    pd_dict = {}
    for i in range(1005):
        pd_dict[i] = distance_list[i]
    pd_dict = sorted(pd_dict.items(), key=lambda d: d[1], reverse=False)
    closest_points = []
    for i in range(1, 111):
        closest_points.append(pd_dict[i][0])
    m = 1
    index = 10
    for i in range(10, 110):
        t = closest_points[0:i]
        cond = compute_cond(t)
        if cond < m:
            m = cond
            index = i
    print(m, index)
    add = 0
    for i in range(1, 111):
        if department[i] == department[0]:
            add += 1
    print(add/110)

    for i in range(1005):
        if i != 7:
            distance = l2_distance(dim_vector[7], dim_vector[i])
        else:
            distance = 0
        distance_list.append(distance)
    pd_dict = {}
    for i in range(1005):
        pd_dict[i] = distance_list[i]
    pd_dict = sorted(pd_dict.items(), key=lambda d: d[1], reverse=False)
    closest_points = []
    for i in range(1, 111):
        closest_points.append(pd_dict[i][0])
    m = 1
    index = 10
    for i in range(10, 110):
        t = closest_points[0:i]
        cond = compute_cond(t)
        if cond < m:
            m = cond
            index = i
    print(m, index)
    add = 0
    for i in range(1, 111):
        if department[i] == department[7]:
            add += 1
    print(add/110)












