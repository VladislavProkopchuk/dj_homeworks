from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.permissions import SAFE_METHODS

from advertisements.models import Advertisement, FavoriteAdvertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)
        # также можно переопределить perform_create() в классе AdvertisementViewSet
        # def perform_create(self, serializer):
        #         serializer.save(creator=self.request.user)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        method = self.context["request"].method
        if method in ['POST', 'PUT', 'PATCH']:
            user = self.context["request"].user
            status = self.context["request"].data.get("status")

            if method == 'POST' or status == 'OPEN':
                count_open_advs = self.Meta.model.objects.filter(creator=user, status='OPEN').count()
                if count_open_advs >= settings.MAX_OPEN_ADV:
                    message = 'You can only have %d active messages.' % settings.MAX_OPEN_ADV
                    raise serializers.ValidationError(message)

        return data


class FavoriteAdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для избранных объявления."""

    subscriber = UserSerializer(
        read_only=True,
    )
    # advertisement = AdvertisementSerializer(
    #     read_only=True,
    # )

    class Meta:
        model = FavoriteAdvertisement
        fields = ('id', 'advertisement', 'subscriber', )

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["subscriber"] = self.context["request"].user
        id_adv = self.context["request"].data.get('advertisement')
        adv = self.Meta.model.objects.filter(
            subscriber=validated_data["subscriber"],
            advertisement=id_adv
        )
        if adv:
            message = 'the advertisement is already in favorites'
            raise serializers.ValidationError(message)
        return super().create(validated_data)

    def validate(self, data):
        method = self.context["request"].method
        if method in SAFE_METHODS:
            return data
        # запрещаем добавлять в избранное собственные объявления
        if method in ['POST', 'PATCH']:
            user = self.context["request"].user
            id_adv = self.context["request"].data.get('advertisement')
            adv = Advertisement.objects.filter(creator=user, id=id_adv)
            if adv:
                message = 'you can\'t add your ad to favorites'
                raise serializers.ValidationError(message)

        return data
