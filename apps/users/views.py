from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import RegisterSerializer
from .services.services import save_pending_registration


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        save_pending_registration(
            email=validated_data["email"],
            full_name=validated_data["full_name"],
            password=validated_data["password"],
        )

        return Response(
            {
                "message": "Registration data saved successfully. Please complete verification."
            },
            status=status.HTTP_201_CREATED,
        )