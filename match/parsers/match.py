import logging
from typing import Literal
from pydantic import Field, validator
from core.parsers import BaseModelWithLogger
from lolsite.tasks import get_riot_api

from player.models import simplify

logger = logging.getLogger(__name__)


class StylesModel(BaseModelWithLogger):
    description: str
    selections: list[dict[Literal['perk', 'var1', 'var2', 'var3'], int]]
    style: int


class SelectionModel(BaseModelWithLogger):
    perk: int
    var1: int
    var2: int
    var3: int


class PrimaryPerkStyleModel(BaseModelWithLogger):
    description: Literal['primaryStyle']
    style: int
    selections: list[SelectionModel]

    @validator('selections')
    def validate_selections(cls, v):
        if len(v) != 4:
            raise ValueError(f'selections should have length 4 but had length {len(v)}')
        return v


class SubPerkStyleModel(BaseModelWithLogger):
    description: Literal['subStyle']
    style: int
    selections: list[SelectionModel]

    @validator('selections')
    def validate_selections(cls, v):
        if len(v) != 2:
            raise ValueError(f'selections should have length 2 but had length {len(v)}')
        return v


class PerksModel(BaseModelWithLogger):
    statPerks: dict[Literal['defense', 'flex', 'offense'], int]
    styles: list[StylesModel]

    @property
    def primary_style(self):
        out = [x for x in self.styles if x.description == 'primaryStyle'][0]
        return PrimaryPerkStyleModel(**out.dict())

    @property
    def sub_style(self):
        out = [x for x in self.styles if x.description == 'subStyle'][0]
        return SubPerkStyleModel(**out.dict())


class ParticipantModel(BaseModelWithLogger):
    challenges: dict[str, float | int] = Field(default_factory=dict)
    perks: PerksModel
    assists: int
    baronKills: int
    bountyLevel: int
    champExperience: int
    champLevel: int
    championId: int
    championName: str
    championTransform: int
    consumablesPurchased: int
    damageDealtToBuildings: int
    damageDealtToObjectives: int
    damageDealtToTurrets: int
    damageSelfMitigated: int
    deaths: int
    detectorWardsPlaced: int
    doubleKills: int
    dragonKills: int
    eligibleForProgression: bool | None
    allInPings: int | None = 0
    assistMePings: int | None = 0
    baitPings: int | None = 0
    basicPings: int | None = 0
    commandPings: int | None = 0
    dangerPings: int | None = 0
    enemyMissingPings: int | None = 0
    enemyVisionPings: int | None = 0
    getBackPings: int | None = 0
    holdPings: int | None = 0
    needVisionPings: int | None = 0
    onMyWayPings: int | None = 0
    pushPings: int | None = 0
    visionClearedPings: int | None = 0
    firstBloodAssist: bool
    firstBloodKill: bool
    firstTowerAssist: bool
    firstTowerKill: bool
    gameEndedInEarlySurrender: bool
    gameEndedInSurrender: bool
    goldEarned: int
    goldSpent: int
    individualPosition: str
    inhibitorKills: int
    inhibitorTakedowns: int | None
    inhibitorsLost: int
    item0: int
    item1: int
    item2: int
    item3: int
    item4: int
    item5: int
    item6: int
    itemsPurchased: int
    killingSprees: int
    kills: int
    lane: str
    largestCriticalStrike: int
    largestKillingSpree: int
    largestMultiKill: int
    longestTimeSpentLiving: int
    magicDamageDealt: int
    magicDamageDealtToChampions: int
    magicDamageTaken: int
    neutralMinionsKilled: int
    nexusKills: int
    nexusLost: int
    nexusTakedowns: int | None
    objectivesStolen: int
    objectivesStolenAssists: int
    participantId: int
    pentaKills: int
    physicalDamageDealt: int
    physicalDamageDealtToChampions: int
    physicalDamageTaken: int
    profileIcon: int
    puuid: str
    quadraKills: int
    riotIdName: str
    riotIdTagline: str
    role: str
    sightWardsBoughtInGame: int
    spell1Casts: int = 0
    spell2Casts: int = 0
    spell3Casts: int = 0
    spell4Casts: int = 0
    summoner1Casts: int
    summoner1Id: int
    summoner2Casts: int
    summoner2Id: int
    summonerId: str
    summonerLevel: int
    summonerName: str
    teamEarlySurrendered: bool
    teamId: int
    teamPosition: str
    timeCCingOthers: int
    timePlayed: int
    totalDamageDealt: int
    totalDamageDealtToChampions: int
    totalDamageShieldedOnTeammates: int
    totalDamageTaken: int
    totalHeal: int
    totalHealsOnTeammates: int
    totalMinionsKilled: int
    totalTimeCCDealt: int
    totalTimeSpentDead: int
    totalUnitsHealed: int
    tripleKills: int
    trueDamageDealt: int
    trueDamageDealtToChampions: int
    trueDamageTaken: int
    turretKills: int = 0
    turretTakedowns: int | None
    turretsLost: int
    unrealKills: int
    visionScore: int
    visionWardsBoughtInGame: int
    wardsKilled: int = 0
    wardsPlaced: int = 0
    win: bool

    @property
    def simple_name(self):
        return simplify(self.summonerName)

    @property
    def stat_perk_0(self):
        return self.perks.statPerks.get('offense', 0)

    @property
    def stat_perk_1(self):
        return self.perks.statPerks.get('flex', 0)

    @property
    def stat_perk_2(self):
        return self.perks.statPerks.get('defense', 0)

    @validator(
        'allInPings', 'pushPings', 'assistMePings',
        'baitPings', 'commandPings', 'dangerPings',
        'enemyMissingPings', 'enemyVisionPings', 'getBackPings',
        'holdPings', 'needVisionPings', 'onMyWayPings',
        'pushPings', 'visionClearedPings',
        pre=True,
        always=True,
    )
    def validate_pings(cls, v):
        if not v:
            return 0
        return v


class BanType(BaseModelWithLogger):
    championId: int
    pickTurn: int


class TeamObjectiveModel(BaseModelWithLogger):
    first: bool
    kills: int


class TeamObjectives(BaseModelWithLogger):
    baron: TeamObjectiveModel
    champion: TeamObjectiveModel
    dragon: TeamObjectiveModel
    inhibitor: TeamObjectiveModel
    riftHerald: TeamObjectiveModel
    tower: TeamObjectiveModel


class TeamModel(BaseModelWithLogger):
    bans: list[BanType]
    objectives: TeamObjectives
    teamId: int
    win: bool = False


class MatchMetaDataModel(BaseModelWithLogger):
    dataVersion: int
    matchId: str
    participants: list[str]


class MatchModel(BaseModelWithLogger):
    participants: list[ParticipantModel]
    teams: list[TeamModel]
    gameCreation: int
    gameEndTimestamp: int | None
    gameDuration: int
    gameId: int
    gameMode: str
    gameName: str
    gameStartTimestamp: int
    gameType: str
    gameVersion: str
    mapId: int
    platformId: str
    queueId: int
    tournamentCode: str | None

    @validator('gameDuration')
    def game_duration_is_sometimes_not_right(cls, v, values, **kwargs):
        if values['gameEndTimestamp']:
            return v * 1000
        return v

    @property
    def sem_ver(self):
        version = {i: int(x) for i, x in enumerate(self.gameVersion.split("."))}
        return version


class MatchResponseModel(BaseModelWithLogger):
    metadata: MatchMetaDataModel
    info: MatchModel


def do_test():
    api = get_riot_api()
    data = api.match.get('NA1_4495779664', 'na').json()
    return MatchResponseModel(**data)
