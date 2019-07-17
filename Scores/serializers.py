from rest_framework import serializers

from Scores.models import ChartLevel, SongChart, ChartDifficulty


class DifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartDifficulty
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    beginner = DifficultySerializer(allow_null=True)
    basic = DifficultySerializer(allow_null=True)
    difficult = DifficultySerializer(allow_null=True)
    expert = DifficultySerializer(allow_null=True)
    challenge = DifficultySerializer(allow_null=True)

    class Meta:
        model = ChartLevel
        fields = '__all__'


class SongChartSerializer(serializers.ModelSerializer):
    single: LevelSerializer = LevelSerializer()
    double: LevelSerializer = LevelSerializer()

    class Meta:
        model = SongChart
        fields = '__all__'

    def create(self, validated_data):
        single_data = validated_data.pop('single')
        double_data = validated_data.pop('double')

        beginner_steps = single_data.pop('beginner')
        basic_steps = single_data.pop('basic')
        difficult_steps = single_data.pop('difficult')
        expert_steps = single_data.pop('expert')
        challenge_steps = single_data.pop('challenge')
        beg = ChartDifficulty.objects.create(**beginner_steps) if beginner_steps else None
        bas = ChartDifficulty.objects.create(**basic_steps) if basic_steps else None
        dif = ChartDifficulty.objects.create(**difficult_steps) if difficult_steps else None
        exp = ChartDifficulty.objects.create(**expert_steps) if expert_steps else None
        cha = ChartDifficulty.objects.create(**challenge_steps) if challenge_steps else None
        sing = ChartLevel.objects.create(
            beginner=beg,
            basic=bas,
            difficult=dif,
            expert=exp,
            challenge=cha
        )

        beginner_steps = double_data.pop('beginner')
        basic_steps = double_data.pop('basic')
        difficult_steps = double_data.pop('difficult')
        expert_steps = double_data.pop('expert')
        challenge_steps = double_data.pop('challenge')
        beg = ChartDifficulty.objects.create(**beginner_steps) if beginner_steps else None
        bas = ChartDifficulty.objects.create(**basic_steps) if basic_steps else None
        dif = ChartDifficulty.objects.create(**difficult_steps) if difficult_steps else None
        exp = ChartDifficulty.objects.create(**expert_steps) if expert_steps else None
        cha = ChartDifficulty.objects.create(**challenge_steps) if challenge_steps else None
        doub = ChartLevel.objects.create(
            beginner=beg,
            basic=bas,
            difficult=dif,
            expert=exp,
            challenge=cha
        )

        songchart = SongChart.objects.create(single=sing, double=doub, **validated_data)
        return songchart
