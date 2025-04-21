from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.quizzes.models import Quiz

from apps.users.models import CustomUser
class QuizAPITests(APITestCase):
    def setUp(self):
        """Настройка тестов"""
        # Создаём пользователя
        self.user = CustomUser.objects.create_user(email='testuser@email.com', password='testpassword')
        self.url = reverse('quiz-list')  # URL для списка всех квизов

        # Создаём JWT токен
        self.token = self.get_jwt_token(self.user)

        # Создаём тестовый Quiz
        self.quiz = Quiz.objects.create(title="Test Quiz", description="This is a test quiz.")

    def get_jwt_token(self, user):
        """Функция для получения JWT токена"""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_quiz_list(self):
        """Тест на доступ к списку квизов для авторизованного пользователя"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Проверяем, что в ответе только один квиз

    def test_quiz_list_without_authentication(self):
        """Тест на доступ к списку квизов без авторизации"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_quiz_creation(self):
        """Тест на создание квиза с авторизацией"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {'title': 'New Quiz', 'description': 'A brand new quiz'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.count(), 2)  # Проверяем, что новый квиз был добавлен

    def test_quiz_creation_without_authentication(self):
        """Тест на создание квиза без авторизации"""
        data = {'title': 'New Quiz', 'description': 'A brand new quiz'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
