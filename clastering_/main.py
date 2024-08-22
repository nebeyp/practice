# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import numpy as np
import matplotlib.pyplot as plt
import PIL
from PIL import Image

import random
from PIL import Image


class KMeans:
    # конструктор класса по умолчанию
    def __init__(self, k):
        self.k = k
        self.centroids = []

    # инициализируеv начальные центроиды рандомно.
    def initialize_centroids(self, pixels):
        self.centroids = random.sample(pixels, self.k)

    # делим пиксели по кластерам
    def assign_clusters(self, pixels):
        clusters = [[] for i in range(self.k)]
        for pixel in pixels:
            centroid_index = self._find_closest_centroid(pixel)
            clusters[centroid_index].append(pixel)
        return clusters

    # обновление положения центроидов
    def update_centroids(self, clusters):
        new_centroids = []
        for cluster in clusters:
            # если кластер не пустой
            if cluster:
                new_centroids.append(self._calculate_mean(cluster))
            else:
                new_centroids.append(random.choice(clusters))
        self.centroids = new_centroids

    # Приватный метод поиска ближайшего центроида к пикселю
    def _find_closest_centroid(self, pixel):
        min_distance = float('inf') # бесконечность
        centroid_index = 0
        for i, centroid in enumerate(self.centroids):
            distance = self._euclidean_distance(pixel, centroid)
            if distance < min_distance:
                min_distance = distance
                centroid_index = i
        return centroid_index

    # Евклидово расстояние, метрика
    def _euclidean_distance(self, pixel1, pixel2):
        return sum((p1 - p2) ** 2 for p1, p2 in zip(pixel1, pixel2)) ** 0.5

    # вычисляем средние значения для каждого компонента цвета в заданном кластере.
    def _calculate_mean(self, cluster):
        cluster_size = len(cluster) # размер кластера
        return [sum(x) // cluster_size for x in zip(*cluster)]

    def run(self, pixels, max_iterations=100):
        self.initialize_centroids(pixels)
        for i in range(max_iterations):
            clusters = self.assign_clusters(pixels) # делим пиксели по кластерам
            self.update_centroids(clusters) # обновляем центры кластеров
        return clusters, self.centroids


# загрузка изображения по имени файла
def load_image(filename):
    image = Image.open(filename)
    # print(list(image.getdata())[:10]) - список кортежей
    # возвращаем список из компонентов канала каждого пикселя в формате RGBA
    return list(image.getdata())


def save_image(filename, pixels, size):
    image = Image.new("RGB", size) # создаем объект изображения, указывая режим изображения и его размер
    image.putdata(pixels) # заполняем изображение пикселями
    image.save(filename) # сохраняем



# Загрузка изображения
image_filename = "C:\\Users\\Roads\\Downloads\\mom.png"
pixels = load_image(image_filename)
image_size = Image.open(image_filename).size # получаем (width, height) изображения

# Кластеризация изображения
k = 8  # Количество кластеров
kmeans = KMeans(k)
clusters, centroids = kmeans.run(pixels)

# Создание нового изображения с использованием центроидов
new_pixels = []
for pixel in pixels:
    centroid_index = kmeans._find_closest_centroid(pixel)
    new_pixels.append(tuple(map(int, centroids[centroid_index])))

# Сохранение нового изображения
new_image_filename = "C:\\Users\\Roads\\Downloads\\clustered.png"
save_image(new_image_filename, new_pixels, image_size)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
