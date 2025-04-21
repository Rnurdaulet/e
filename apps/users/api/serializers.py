from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import UserProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя с ролевыми ограничениями"""

    language = serializers.SerializerMethodField()
    school = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "phone", "iin", "avatar", "school",
                  "is_active", "is_staff", "is_superuser", "has_full_access", "language"]

    def get_language(self, obj):
        """Получаем язык пользователя из профиля"""
        if hasattr(obj, "profile") and obj.profile.language:
            return obj.profile.language.id  # Или obj.profile.language.name, если нужен текст
        return None

    def get_school(self, obj):
        """Получаем школу пользователя из профиля"""
        if hasattr(obj, "profile") and obj.profile.school:
            return obj.profile.school.id  # Или obj.profile.school.name, если нужен текст
        return None

    def get_fields(self):
        fields = super().get_fields()
        user = self.context["request"].user

        #  USER не должен видеть критические поля
        if user.role == User.Role.USER:
            fields.pop("school", None)
            fields.pop("is_active", None)
            fields.pop("is_staff", None)
            fields.pop("is_superuser", None)
            fields.pop("has_full_access", None)

        #  Только `ADMIN` может менять критические поля
        if not user.is_superuser:
            fields["role"].read_only = True
            fields["iin"].read_only = True
            fields["school"].read_only = True
            fields["is_active"].read_only = True
            fields["is_staff"].read_only = True
            fields["is_superuser"].read_only = True
            fields["has_full_access"].read_only = True

        #  SCHOOL_ADMIN не может изменять school (оно назначается автоматически)
        if user.role == User.Role.SCHOOL_ADMIN:
            fields["school"].read_only = True

        return fields

    def validate_role(self, value):
        """SCHOOL_ADMIN может создавать только TEACHER и STUDENT."""
        user = self.context["request"].user
        if user.role == User.Role.SCHOOL_ADMIN and value not in [User.Role.TEACHER, User.Role.STUDENT]:
            raise serializers.ValidationError("Вы можете создавать только учителей и учеников.")
        return value

    def update(self, instance, validated_data):
        """SCHOOL_ADMIN не может менять школу и роль после создания."""
        user = self.context["request"].user

        if user.role == User.Role.SCHOOL_ADMIN:
            validated_data.pop("role", None)  #  Нельзя менять роль после создания
            validated_data.pop("school", None)  #  Нельзя менять школу

        return super().update(instance, validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор профиля пользователя с защитой от обхода API"""

    user = UserSerializer(read_only=True)  #  Запрещаем редактирование `user`

    class Meta:
        model = UserProfile
        fields = "__all__"

    def get_fields(self):
        fields = super().get_fields()
        user = self.context["request"].user

        #  USER не должен видеть `subject`, `school_class_prefix`, `school_class`, `school`
        if user.role == User.Role.USER:
            fields.pop("subject", None)
            fields.pop("school_class_prefix", None)
            fields.pop("school_class", None)
            fields.pop("school", None)

        #  SCHOOL_ADMIN, TEACHER, EXPERT, STUDENT не могут изменять `school`
        if user.role in [User.Role.SCHOOL_ADMIN, User.Role.TEACHER, User.Role.EXPERT, User.Role.STUDENT]:
            fields["school"].read_only = True  # Блокируем редактирование школы

        #  Никто, кроме ADMIN, не может менять is_active, is_staff, is_superuser
        if not user.is_superuser:
            fields.pop("is_active", None)
            fields.pop("is_staff", None)
            fields.pop("is_superuser", None)

        return fields

    def update(self, instance, validated_data):
        """
        - Блокируем изменение user.
        - Запрещаем SCHOOL_ADMIN, TEACHER, EXPERT, STUDENT изменять school.
        - Запрещаем USER менять language у других пользователей.
        """
        user = self.context["request"].user

        if "user" in validated_data:
            validated_data.pop("user")  #  Нельзя менять `user` через `UserProfile`

        if user.role in [User.Role.SCHOOL_ADMIN, User.Role.TEACHER, User.Role.EXPERT, User.Role.STUDENT]:
            validated_data.pop("school", None)  #  Эти роли не могут менять school

        #  USER может менять language только у себя
        if user.role == User.Role.USER and instance.user != user:
            validated_data.pop("language", None)

        return super().update(instance, validated_data)


class CustomRegisterSerializer(serializers.ModelSerializer):
    """Регистрация пользователя с защитой от обхода прав"""

    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["email", "password1", "password2", "first_name", "last_name", "role", "phone", "iin"]

    def validate(self, attrs):
        """Проверяем пароли, роль и уникальность email"""
        request_user = self.context["request"].user if "request" in self.context else None

        #  Запрещаем дублирование email
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({"email": "Пользователь с таким email уже существует."})

        #  Запрещаем SCHOOL_ADMIN создавать кого-то, кроме TEACHER и STUDENT
        if request_user and request_user.role == User.Role.SCHOOL_ADMIN and attrs["role"] not in [User.Role.TEACHER, User.Role.STUDENT]:
            raise serializers.ValidationError({"role": "Вы можете создавать только учителей и учеников."})

        #  Обычные пользователи не могут выбирать роль – они всегда USER
        if not request_user:
            attrs["role"] = User.Role.USER  #  Если нет request_user, роль USER
        elif request_user.role not in [User.Role.ADMIN, User.Role.SCHOOL_ADMIN]:
            attrs["role"] = User.Role.USER  #  Если регистрируется сам, то USER

        #  Проверяем совпадение паролей
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})

        return attrs

    def create(self, validated_data):
        """Создаем пользователя с безопасными ограничениями"""
        validated_data.pop("password2")  # Удаляем второй пароль
        password = validated_data.pop("password1")

        request_user = self.context["request"].user if "request" in self.context else None

        # Только `ADMIN` и `SCHOOL_ADMIN` могут задавать роль
        if request_user and request_user.role in [User.Role.ADMIN, User.Role.SCHOOL_ADMIN]:
            role = validated_data.get("role", User.Role.USER)
        else:
            role = User.Role.USER  # Если пользователь неавторизован – роль всегда USER

        # Если `SCHOOL_ADMIN` создаёт пользователя, он может задать только `TEACHER` или `STUDENT`
        if request_user and request_user.role == User.Role.SCHOOL_ADMIN:
            if role not in [User.Role.TEACHER, User.Role.STUDENT]:
                role = User.Role.STUDENT  # По умолчанию создаем учителя
            validated_data["school"] = request_user.school  # Назначаем школу

        validated_data["role"] = role

        user = User.objects.create(**validated_data)
        user.set_password(password)  # Шифруем пароль
        user.save()
        return user

class ChangePasswordSerializer(serializers.Serializer):
    """Смена пароля"""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Старый пароль неверен.")
        return value
