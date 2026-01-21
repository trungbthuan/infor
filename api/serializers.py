from rest_framework import serializers
from .models import Students, Profiles

class StudentsSerializer(serializers.ModelSerializer):
    # Tùy chỉnh định dạng ngày tháng ngay tại đây
    birthday = serializers.DateField(
        format="%d/%m/%Y",  # Định dạng output (GET)
        input_formats=["%d/%m/%Y", "iso-8601"] # Định dạng input (POST)
    )
    class Meta:
        model = Students
        fields = ['id', 'full_name', 'birthday', 'sex', 'class_name', 'average', 'morality', 'performance']

        # Trường 'id' là Read-Only vì nó tự động được tạo.
        read_only_fields = ('id',)

class ProfilesSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(
        format="%d/%m/%Y",  # Định dạng output (GET)
        input_formats=["%d/%m/%Y", "iso-8601"] # Định dạng input (POST)
    )
    recruitment_day = serializers.DateField(
        format="%d/%m/%Y",  # Định dạng output (GET)
        input_formats=["%d/%m/%Y", "iso-8601"] # Định dạng input (POST)
    )

    class Meta:
        model = Profiles
        fields = ['id', 'full_name', 'birthday', 'sex', 'birth_place', 'nation', 'recruitment_day', 'job_title', 'department']

        read_only_fields = ('id',)
