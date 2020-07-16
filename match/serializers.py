from rest_framework import serializers
from .models import Match, Participant, Stats
from .models import Timeline, Team, Ban

from .models import AdvancedTimeline, Frame, ParticipantFrame
from .models import Event, AssistingParticipants


class MatchSerializer(serializers.ModelSerializer):
    # get_absolute_url = serializers.CharField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = "__all__"

    def __init__(self, *args, summoner_name=None, **kwargs):
        self.summoner_name = summoner_name
        super().__init__(*args, **kwargs)

    def get_url(self, obj):
        return obj.get_absolute_url(pname=self.summoner_name)


class ParticipantSerializer(serializers.ModelSerializer):
    perk_sub_style_image_url = serializers.CharField()

    class Meta:
        model = Participant
        fields = "__all__"


class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stats
        fields = "__all__"


class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


class BanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ban
        fields = "__all__"


class FullParticipantSerializer(serializers.ModelSerializer):
    stats = StatsSerializer(read_only=True)
    timelines = TimelineSerializer(many=True, read_only=True)

    class Meta:
        model = Participant
        fields = "__all__"


class FullTeamSerializer(serializers.ModelSerializer):
    bans = BanSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = "__all__"


class FullMatchSerializer(serializers.ModelSerializer):
    participants = FullParticipantSerializer(many=True, read_only=True)
    teams = FullTeamSerializer(many=True, read_only=True)

    class Meta:
        model = Match
        fields = "__all__"


# ADVANCED TIMELINE
class AdvancedTimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvancedTimeline
        fields = "__all__"


class FrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = "__all__"


class ParticipantFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantFrame
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class AssistingParticipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistingParticipants
        fields = "__all__"
