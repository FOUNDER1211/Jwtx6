import json
import base64
import asyncio
import httpx
import sys
import logging
from Crypto.Cipher import AES
from flask import Flask, request, jsonify

# =====================================================================
# Protobuf Imports and Initialization
# =====================================================================
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import json_format

try:
    from google.protobuf import runtime_version as _runtime_version
except ImportError:
    _runtime_version = None

_sym_db = _symbol_database.Default()
_globals = globals()

# --- 1. FreeFire_pb2.py ---
if _runtime_version:
    try:
        _runtime_version.ValidateProtobufRuntimeVersion(
            _runtime_version.Domain.PUBLIC, 6, 30, 0, '', 'FreeFire.proto'
        )
    except Exception:
        pass

DESCRIPTOR_FF = _descriptor_pool.Default().AddSerializedFile(b'\n\x0e\x46reeFire.proto\"c\n\x08LoginReq\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0blogin_token\x18\x1d \x01(\t\x12\x1b\n\x13orign_platform_type\x18\x63 \x01(\t\"]\n\x10\x42lacklistInfoRes\x12\x1e\n\nban_reason\x18\x01 \x01(\x0e\x32\n.BanReason\x12\x17\n\x0f\x65xpire_duration\x18\x02 \x01(\r\x12\x10\n\x08\x62\x61n_time\x18\x03 \x01(\r\"f\n\x0eLoginQueueInfo\x12\r\n\x05\x61llow\x18\x01 \x01(\x08\x12\x16\n\x0equeue_position\x18\x02 \x01(\r\x12\x16\n\x0eneed_wait_secs\x18\x03 \x01(\r\x12\x15\n\rqueue_is_full\x18\x04 \x01(\x08\"\xa0\x03\n\x08LoginRes\x12\x12\n\naccount_id\x18\x01 \x01(\x04\x12\x13\n\x0block_region\x18\x02 \x01(\t\x12\x13\n\x0bnoti_region\x18\x03 \x01(\t\x12\x11\n\tip_region\x18\x04 \x01(\t\x12\x19\n\x11\x61gora_environment\x18\x05 \x01(\t\x12\x19\n\x11new_active_region\x18\x06 \x01(\t\x12\x19\n\x11recommend_regions\x18\x07 \x03(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03ttl\x18\t \x01(\r\x12\x12\n\nserver_url\x18\n \x01(\t\x12\x16\n\x0e\x65mulator_score\x18\x0b \x01(\r\x12$\n\tblacklist\x18\x0c \x01(\x0b\x32\x11.BlacklistInfoRes\x12#\n\nqueue_info\x18\r \x01(\x0b\x32\x0f.LoginQueueInfo\x12\x0e\n\x06tp_url\x18\x0e \x01(\t\x12\x15\n\rapp_server_id\x18\x0f \x01(\r\x12\x0f\n\x07\x61no_url\x18\x10 \x01(\t\x12\x0f\n\x07ip_city\x18\x11 \x01(\t\x12\x16\n\x0eip_subdivision\x18\x12 \x01(\t*\xa8\x01\n\tBanReason\x12\x16\n\x12\x42\x41N_REASON_UNKNOWN\x10\x00\x12\x1b\n\x17\x42\x41N_REASON_IN_GAME_AUTO\x10\x01\x12\x15\n\x11\x42\x41N_REASON_REFUND\x10\x02\x12\x15\n\x11\x42\x41N_REASON_OTHERS\x10\x03\x12\x16\n\x12\x42\x41N_REASON_SKINMOD\x10\x04\x12 \n\x1b\x42\x41N_REASON_IN_GAME_AUTO_NEW\x10\xf6\x07\x62\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR_FF, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR_FF, 'FreeFire_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR_FF._loaded_options = None
    _globals['_BANREASON']._serialized_start=738
    _globals['_BANREASON']._serialized_end=906
    _globals['_LOGINREQ']._serialized_start=18
    _globals['_LOGINREQ']._serialized_end=117
    _globals['_BLACKLISTINFORES']._serialized_start=119
    _globals['_BLACKLISTINFORES']._serialized_end=212
    _globals['_LOGINQUEUEINFO']._serialized_start=214
    _globals['_LOGINQUEUEINFO']._serialized_end=316
    _globals['_LOGINRES']._serialized_start=319
    _globals['_LOGINRES']._serialized_end=735

# --- 2. my_pb2.py ---
DESCRIPTOR_MY = _descriptor_pool.Default().AddSerializedFile(b'\n\x08my.proto\"\xae\t\n\x08GameData\x12\x11\n\ttimestamp\x18\x03 \x01(\t\x12\x11\n\tgame_name\x18\x04 \x01(\t\x12\x14\n\x0cgame_version\x18\x05 \x01(\x05\x12\x14\n\x0cversion_code\x18\x07 \x01(\t\x12\x0f\n\x07os_info\x18\x08 \x01(\t\x12\x13\n\x0b\x64\x65vice_type\x18\t \x01(\t\x12\x18\n\x10network_provider\x18\n \x01(\t\x12\x17\n\x0f\x63onnection_type\x18\x0b \x01(\t\x12\x14\n\x0cscreen_width\x18\x0c \x01(\x05\x12\x15\n\rscreen_height\x18\r \x01(\x05\x12\x0b\n\x03\x64pi\x18\x0e \x01(\t\x12\x10\n\x08\x63pu_info\x18\x0f \x01(\t\x12\x11\n\ttotal_ram\x18\x10 \x01(\x05\x12\x10\n\x08gpu_name\x18\x11 \x01(\t\x12\x13\n\x0bgpu_version\x18\x12 \x01(\t\x12\x0f\n\x07user_id\x18\x13 \x01(\t\x12\x12\n\nip_address\x18\x14 \x01(\t\x12\x10\n\x08language\x18\x15 \x01(\t\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x15\n\rplatform_type\x18\x17 \x01(\x05\x12\x1a\n\x12\x64\x65vice_form_factor\x18\x18 \x01(\t\x12\x14\n\x0c\x64\x65vice_model\x18\x19 \x01(\t\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x1d \x01(\t\x12\x18\n\x10unknown_field_30\x18\x1e \x01(\x05\x12\"\n\x1asecondary_network_provider\x18) \x01(\t\x12!\n\x19secondary_connection_type\x18* \x01(\t\x12\x11\n\tunique_id\x18\x39 \x01(\t\x12\x10\n\x08\x66ield_60\x18< \x01(\x05\x12\x10\n\x08\x66ield_61\x18= \x01(\x05\x12\x10\n\x08\x66ield_62\x18> \x01(\x05\x12\x10\n\x08\x66ield_63\x18? \x01(\x05\x12\x10\n\x08\x66ield_64\x18@ \x01(\x05\x12\x10\n\x08\x66ield_65\x18\x41 \x01(\x05\x12\x10\n\x08\x66ield_66\x18\x42 \x01(\x05\x12\x10\n\x08\x66ield_67\x18\x43 \x01(\x05\x12\x10\n\x08\x66ield_70\x18\x46 \x01(\x05\x12\x10\n\x08\x66ield_73\x18I \x01(\x05\x12\x14\n\x0clibrary_path\x18J \x01(\t\x12\x10\n\x08\x66ield_76\x18L \x01(\x05\x12\x10\n\x08\x61pk_info\x18M \x01(\t\x12\x10\n\x08\x66ield_78\x18N \x01(\x05\x12\x10\n\x08\x66ield_79\x18O \x01(\x05\x12\x17\n\x0fos_architecture\x18Q \x01(\t\x12\x14\n\x0c\x62uild_number\x18S \x01(\t\x12\x10\n\x08\x66ield_85\x18U \x01(\x05\x12\x18\n\x10graphics_backend\x18V \x01(\t\x12\x19\n\x11max_texture_units\x18W \x01(\x05\x12\x15\n\rrendering_api\x18X \x01(\x05\x12\x18\n\x10\x65ncoded_field_89\x18Y \x01(\t\x12\x10\n\x08\x66ield_92\x18\\ \x01(\x05\x12\x13\n\x0bmarketplace\x18] \x01(\t\x12\x16\n\x0e\x65ncryption_key\x18^ \x01(\t\x12\x15\n\rtotal_storage\x18_ \x01(\x05\x12\x10\n\x08\x66ield_97\x18\x61 \x01(\x05\x12\x10\n\x08\x66ield_98\x18\x62 \x01(\x05\x12\x10\n\x08\x66ield_99\x18\x63 \x01(\t\x12\x11\n\tfield_100\x18\x64 \x01(\tb\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR_MY, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR_MY, 'my_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR_MY._options = None
    _globals['_GAMEDATA']._serialized_start=13
    _globals['_GAMEDATA']._serialized_end=1211

# --- 3. output_pb2.py ---
DESCRIPTOR_OUT = _descriptor_pool.Default().AddSerializedFile(b'\n\x13jwt_generator.proto\"\xd2\x02\n\nGarena_420\x12\x12\n\naccount_id\x18\x01 \x01(\x03\x12\x0e\n\x06region\x18\x02 \x01(\t\x12\r\n\x05place\x18\x03 \x01(\t\x12\x10\n\x08location\x18\x04 \x01(\t\x12\x0e\n\x06status\x18\x05 \x01(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\n\n\x02id\x18\t \x01(\x05\x12\x0b\n\x03\x61pi\x18\n \x01(\t\x12\x0e\n\x06number\x18\x0c \x01(\x05\x12\x1e\n\tGarena420\x18\x0f \x01(\x0b\x32\x0b.Garena_420\x12\x0c\n\x04\x61rea\x18\x10 \x01(\t\x12\x11\n\tmain_area\x18\x12 \x01(\t\x12\x0c\n\x04\x63ity\x18\x13 \x01(\t\x12\x0c\n\x04name\x18\x14 \x01(\t\x12\x11\n\ttimestamp\x18\x15 \x01(\x03\x12\x0e\n\x06\x62inary\x18\x16 \x01(\x0c\x12\x13\n\x0b\x62inary_data\x18\x17 \x01(\x0c\x1a\"\n\x12\x44\x65\x63rypted_Payloads\x12\x0c\n\x04type\x18\x01 \x01(\x05\x62\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR_OUT, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR_OUT, 'output_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR_OUT._options = None
    _globals['_GARENA_420']._serialized_start=24
    _globals['_GARENA_420']._serialized_end=362
    _globals['_GARENA_420_DECRYPTED_PAYLOADS']._serialized_start=328
    _globals['_GARENA_420_DECRYPTED_PAYLOADS']._serialized_end=362

# --- 4. AccountPersonalShow_pb2.py ---
DESCRIPTOR_ACC = _descriptor_pool.Default().AddSerializedFile(b'\n\x19\x41\x63\x63ountPersonalShow.proto\x12\x08\x66reefire\"\xbc\x01\n\x0e\x41\x63\x63ountPrefers\x12\x15\n\rhide_my_lobby\x18\x01 \x01(\x08\x12\x1c\n\x14pregame_show_choices\x18\x02 \x03(\r\x12\x1f\n\x17\x62r_pregame_show_choices\x18\x03 \x03(\r\x12\x1a\n\x12hide_personal_info\x18\x04 \x01(\x08\x12\x1f\n\x17\x64isable_friend_spectate\x18\x05 \x01(\x08\x12\x17\n\x0fhide_occupation\x18\x06 \x01(\x08\"\x8a\x01\n\x10\x45xternalIconInfo\x12\x15\n\rexternal_icon\x18\x01 \x01(\t\x12,\n\x06status\x18\x02 \x01(\x0e\x32\x1c.freefire.ExternalIconStatus\x12\x31\n\tshow_type\x18\x03 \x01(\x0e\x32\x1e.freefire.ExternalIconShowType\"\\\n\x0fSocialHighLight\x12\'\n\nhigh_light\x18\x01 \x01(\x0e\x32\x13.freefire.HighLight\x12\x11\n\texpire_at\x18\x02 \x01(\x03\x12\r\n\x05value\x18\x03 \x01(\r\"\xfc\x01\n\x14WeaponPowerTitleInfo\x12\x0e\n\x06region\x18\x01 \x01(\t\x12\x14\n\x0ctitle_cfg_id\x18\x02 \x01(\r\x12\x16\n\x0eleaderboard_id\x18\x03 \x01(\x04\x12\x11\n\tweapon_id\x18\x04 \x01(\r\x12\x0c\n\x04rank\x18\x05 \x01(\r\x12\x13\n\x0b\x65xpire_time\x18\x06 \x01(\x03\x12\x13\n\x0breward_time\x18\x07 \x01(\x03\x12\x12\n\nRegionName\x18\x08 \x01(\t\x12\x39\n\nRegionType\x18\t \x01(\x0e\x32%.freefire.ELeaderBoardTitleRegionType\x12\x0c\n\x04IsBr\x18\n \x01(\x08\"\xad\x01\n\x11GuildWarTitleInfo\x12\x0e\n\x06region\x18\x01 \x01(\t\x12\x0f\n\x07\x63lan_id\x18\x02 \x01(\x04\x12\x14\n\x0ctitle_cfg_id\x18\x03 \x01(\r\x12\x16\n\x0eleaderboard_id\x18\x04 \x01(\x04\x12\x0c\n\x04rank\x18\x05 \x01(\r\x12\x13\n\x0b\x65xpire_time\x18\x06 \x01(\x03\x12\x13\n\x0breward_time\x18\x07 \x01(\x03\x12\x11\n\tclan_name\x18\x08 \x01(\t\"\x92\x01\n\x14LeaderboardTitleInfo\x12?\n\x17weapon_power_title_info\x18\x01 \x03(\x0b\x32\x1e.freefire.WeaponPowerTitleInfo\x12\x39\n\x14guild_war_title_info\x18\x02 \x03(\x0b\x32\x1b.freefire.GuildWarTitleInfo\"\xfb\x03\n\x0fSocialBasicInfo\x12\x12\n\naccount_id\x18\x01 \x01(\x04\x12 \n\x06gender\x18\x02 \x01(\x0e\x32\x10.freefire.Gender\x12$\n\x08language\x18\x03 \x01(\x0e\x32\x12.freefire.Language\x12)\n\x0btime_online\x18\x04 \x01(\x0e\x32\x14.freefire.TimeOnline\x12)\n\x0btime_active\x18\x05 \x01(\x0e\x32\x14.freefire.TimeActive\x12/\n\nbattle_tag\x18\x06 \x03(\x0e\x32\x1b.freefire.PlayerBattleTagID\x12\'\n\nsocial_tag\x18\x07 \x03(\x0e\x32\x13.freefire.SocialTag\x12)\n\x0bmode_prefer\x18\x08 \x01(\x0e\x32\x14.freefire.ModePrefer\x12\x11\n\tsignature\x18\t \x01(\t\x12%\n\trank_show\x18\n \x01(\x0e\x32\x12.freefire.RankShow\x12\x18\n\x10\x62\x61ttle_tag_count\x18\x0b \x03(\r\x12!\n\x19signature_ban_expire_time\x18\x0c \x01(\x03\x12:\n\x12leaderboard_titles\x18\r \x01(\x0b\x32\x1e.freefire.LeaderboardTitleInfo\"\x92\x01\n#SocialHighLightsWithSocialBasicInfo\x12\x35\n\x12social_high_lights\x18\x01 \x03(\x0b\x32\x19.freefire.SocialHighLight\x12\x34\n\x11social_basic_info\x18\x02 \x01(\x0b\x32\x19.freefire.SocialBasicInfo\"c\n\x0eOccupationInfo\x12\x15\n\roccupation_id\x18\x01 \x01(\r\x12\x0e\n\x06scores\x18\x02 \x01(\x04\x12\x13\n\x0bproficients\x18\x03 \x01(\x04\x12\x15\n\rproficient_lv\x18\x04 \x01(\r\"d\n\x14OccupationSeasonInfo\x12\x11\n\tseason_id\x18\x01 \x01(\r\x12\x11\n\tgame_mode\x18\x02 \x01(\r\x12&\n\x04info\x18\x03 \x01(\x0b\x32\x18.freefire.OccupationInfo\"\xcb\x0c\n\x10\x41\x63\x63ountInfoBasic\x12\x12\n\naccount_id\x18\x01 \x01(\x04\x12\x14\n\x0c\x61\x63\x63ount_type\x18\x02 \x01(\r\x12\x10\n\x08nickname\x18\x03 \x01(\t\x12\x13\n\x0b\x65xternal_id\x18\x04 \x01(\t\x12\x0e\n\x06region\x18\x05 \x01(\t\x12\r\n\x05level\x18\x06 \x01(\r\x12\x0b\n\x03\x65xp\x18\x07 \x01(\r\x12\x15\n\rexternal_type\x18\x08 \x01(\r\x12\x15\n\rexternal_name\x18\t \x01(\t\x12\x15\n\rexternal_icon\x18\n \x01(\t\x12\x11\n\tbanner_id\x18\x0b \x01(\r\x12\x10\n\x08head_pic\x18\x0c \x01(\r\x12\x11\n\tclan_name\x18\r \x01(\t\x12\x0c\n\x04rank\x18\x0e \x01(\r\x12\x16\n\x0eranking_points\x18\x0f \x01(\r\x12\x0c\n\x04role\x18\x10 \x01(\r\x12\x16\n\x0ehas_elite_pass\x18\x11 \x01(\x08\x12\x11\n\tbadge_cnt\x18\x12 \x01(\r\x12\x10\n\x08\x62\x61\x64ge_id\x18\x13 \x01(\r\x12\x11\n\tseason_id\x18\x14 \x01(\r\x12\r\n\x05liked\x18\x15 \x01(\r\x12\x12\n\nis_deleted\x18\x16 \x01(\x08\x12\x11\n\tshow_rank\x18\x17 \x01(\x08\x12\x15\n\rlast_login_at\x18\x18 \x01(\x03\x12\x14\n\x0c\x65xternal_uid\x18\x19 \x01(\x04\x12\x11\n\treturn_at\x18\x1a \x01(\x03\x12\x1e\n\x16\x63hampionship_team_name\x18\x1b \x01(\t\x12$\n\x1c\x63hampionship_team_member_num\x18\x1c \x01(\r\x12\x1c\n\x14\x63hampionship_team_id\x18\x1d \x01(\x04\x12\x0f\n\x07\x63s_rank\x18\x1e \x01(\r\x12\x19\n\x11\x63s_ranking_points\x18\x1f \x01(\r\x12\x19\n\x11weapon_skin_shows\x18  \x03(\r\x12\x0e\n\x06pin_id\x18! \x01(\r\x12\x19\n\x11is_cs_ranking_ban\x18\" \x01(\x08\x12\x10\n\x08max_rank\x18# \x01(\r\x12\x13\n\x0b\x63s_max_rank\x18$ \x01(\r\x12\x1a\n\x12max_ranking_points\x18% \x01(\r\x12\x15\n\rgame_bag_show\x18& \x01(\r\x12\x15\n\rpeak_rank_pos\x18\' \x01(\r\x12\x18\n\x10\x63s_peak_rank_pos\x18( \x01(\r\x12\x31\n\x0f\x61\x63\x63ount_prefers\x18) \x01(\x0b\x32\x18.freefire.AccountPrefers\x12\x1f\n\x17periodic_ranking_points\x18* \x01(\r\x12\x15\n\rperiodic_rank\x18+ \x01(\r\x12\x11\n\tcreate_at\x18, \x01(\x03\x12:\n\x16veteran_leave_days_tag\x18- \x01(\x0e\x32\x1a.freefire.VeteranLeaveDays\x12\x1b\n\x13selected_item_slots\x18. \x03(\r\x12\x38\n\x10pre_veteran_type\x18/ \x01(\x0e\x32\x1e.freefire.PreVeteranActionType\x12\r\n\x05title\x18\x30 \x01(\r\x12\x36\n\x12\x65xternal_icon_info\x18\x31 \x01(\x0b\x32\x1a.freefire.ExternalIconInfo\x12\x17\n\x0frelease_version\x18\x32 \x01(\t\x12\x1b\n\x13veteran_expire_time\x18\x33 \x01(\x04\x12\x14\n\x0cshow_br_rank\x18\x34 \x01(\x08\x12\x14\n\x0cshow_cs_rank\x18\x35 \x01(\x08\x12\x0f\n\x07\x63lan_id\x18\x36 \x01(\x04\x12\x15\n\rclan_badge_id\x18\x37 \x01(\r\x12\x19\n\x11\x63ustom_clan_badge\x18\x38 \x01(\t\x12\x1d\n\x15use_custom_clan_badge\x18\x39 \x01(\x08\x12\x15\n\rclan_frame_id\x18: \x01(\r\x12\x18\n\x10membership_state\x18; \x01(\x08\x12:\n\x12select_occupations\x18< \x03(\x0b\x32\x1e.freefire.OccupationSeasonInfo\x12Y\n\"social_high_lights_with_basic_info\x18= \x01(\x0b\x32-.freefire.SocialHighLightsWithSocialBasicInfo\"\x9a\x01\n\x0f\x41vatarSkillSlot\x12\x14\n\x07slot_id\x18\x01 \x01(\x04H\x00\x88\x01\x01\x12\x15\n\x08skill_id\x18\x02 \x01(\x04H\x01\x88\x01\x01\x12\x30\n\x0c\x65quip_source\x18\x03 \x01(\x0e\x32\x15.freefire.EquipSourceH\x02\x88\x01\x01\x42\n\n\x08_slot_idB\x0b\n\t_skill_idB\x0f\n\r_equip_source\"\xfe\x03\n\rAvatarProfile\x12\x16\n\tavatar_id\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x17\n\nskin_color\x18\x03 \x01(\rH\x01\x88\x01\x01\x12\x0f\n\x07\x63lothes\x18\x04 \x03(\r\x12\x16\n\x0e\x65quiped_skills\x18\x05 \x03(\r\x12\x18\n\x0bis_selected\x18\x06 \x01(\x08H\x02\x88\x01\x01\x12\x1f\n\x12pve_primary_weapon\x18\x07 \x01(\rH\x03\x88\x01\x01\x12\x1f\n\x12is_selected_awaken\x18\x08 \x01(\x08H\x04\x88\x01\x01\x12\x15\n\x08\x65nd_time\x18\t \x01(\rH\x05\x88\x01\x01\x12.\n\x0bunlock_type\x18\n \x01(\x0e\x32\x14.freefire.UnlockTypeH\x06\x88\x01\x01\x12\x18\n\x0bunlock_time\x18\x0b \x01(\rH\x07\x88\x01\x01\x12\x1b\n\x0eis_marked_star\x18\x0c \x01(\x08H\x08\x88\x01\x01\x12\x1e\n\x16\x63lothes_tailor_effects\x18\x0d \x03(\rB\x0c\n\n_avatar_idB\r\n\x0b_skin_colorB\x0e\n\x0c_is_selectedB\x15\n\x13_pve_primary_weaponB\x15\n\x13_is_selected_awakenB\x0b\n\t_end_timeB\x0e\n\x0c_unlock_typeB\x0e\n\x0c_unlock_timeB\x11\n\x0f_is_marked_star\"\xd8\x02\n\x12\x41\x63\x63ountNewsContent\x12\x10\n\x08item_ids\x18\x01 \x03(\r\x12\x11\n\x04rank\x18\x02 \x01(\rH\x00\x88\x01\x01\x12\x17\n\nmatch_mode\x18\x03 \x01(\rH\x01\x88\x01\x01\x12\x13\n\x06map_id\x18\x04 \x01(\rH\x02\x88\x01\x01\x12\x16\n\tgame_mode\x18\x05 \x01(\rH\x03\x88\x01\x01\x12\x17\n\ngroup_mode\x18\x06 \x01(\rH\x04\x88\x01\x01\x12\x1b\n\x0etreasurebox_id\x18\x07 \x01(\rH\x05\x88\x01\x01\x12\x19\n\x0c\x63ommodity_id\x18\x08 \x01(\rH\x06\x88\x01\x01\x12\x15\n\x08store_id\x18\t \x01(\rH\x07\x88\x01\x01\x42\x07\n\x05_rankB\r\n\x0b_match_modeB\t\n\x07_map_idB\x0c\n\n_game_modeB\r\n\x0b_group_modeB\x11\n\x0f_treasurebox_idB\x0f\n\r_commodity_idB\x0b\n\t_store_id\"\xa7\x01\n\x0b\x41\x63\x63ountNews\x12%\n\x04type\x18\x01 \x01(\x0e\x32\x12.freefire.NewsTypeH\x00\x88\x01\x01\x12\x32\n\x07\x63ontent\x18\x02 \x01(\x0b\x32\x1c.freefire.AccountNewsContentH\x01\x88\x01\x01\x12\x18\n\x0bupdate_time\x18\x03 \x01(\x03H\x02\x88\x01\x01\x42\x07\n\x05_typeB\n\n\x08_contentB\x0e\n\x0c_update_time\"\x99\x02\n\x0b\x42\x61sicEPInfo\x12\x18\n\x0b\x65p_event_id\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x17\n\nowned_pass\x18\x02 \x01(\x08H\x01\x88\x01\x01\x12\x15\n\x08\x65p_badge\x18\x03 \x01(\rH\x02\x88\x01\x01\x12\x16\n\tbadge_cnt\x18\x04 \x01(\rH\x03\x88\x01\x01\x12\x14\n\x07\x62p_icon\x18\x05 \x01(\tH\x04\x88\x01\x01\x12\x16\n\tmax_level\x18\x06 \x01(\rH\x05\x88\x01\x01\x12\x17\n\nevent_name\x18\x07 \x01(\tH\x06\x88\x01\x01\x42\x0e\n\x0c_ep_event_idB\r\n\x0b_owned_passB\x0b\n\t_ep_badgeB\x0c\n\n_badge_cntB\n\n\x08_bp_iconB\x0c\n\n_max_levelB\r\n\x0b_event_name\"\x9d\x02\n\rClanInfoBasic\x12\x14\n\x07\x63lan_id\x18\x01 \x01(\x04H\x00\x88\x01\x01\x12\x16\n\tclan_name\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x17\n\ncaptain_id\x18\x03 \x01(\x04H\x02\x88\x01\x01\x12\x17\n\nclan_level\x18\x04 \x01(\rH\x03\x88\x01\x01\x12\x15\n\x08\x63\x61pacity\x18\x05 \x01(\rH\x04\x88\x01\x01\x12\x17\n\nmember_num\x18\x06 \x01(\rH\x05\x88\x01\x01\x12\x18\n\x0bhonor_point\x18\x07 \x01(\rH\x06\x88\x01\x01\x42\n\n\x08_clan_idB\x0c\n\n_clan_nameB\r\n\x0b_captain_idB\r\n\x0b_clan_levelB\x0b\n\t_capacityB\r\n\x0b_member_numB\x0e\n\x0c_honor_point\"|\n\x0cPetSkillInfo\x12\x13\n\x06pet_id\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x15\n\x08skill_id\x18\x02 \x01(\rH\x01\x88\x01\x01\x12\x18\n\x0bskill_level\x18\x03 \x01(\rH\x02\x88\x01\x01\x42\t\n\x07_pet_idB\x0b\n\t_skill_idB\x0e\n\x0c_skill_level\"\x84\x03\n\x07PetInfo\x12\x0f\n\x02id\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x11\n\x04name\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x12\n\x05level\x18\x03 \x01(\rH\x02\x88\x01\x01\x12\x10\n\x03\x65xp\x18\x04 \x01(\rH\x03\x88\x01\x01\x12\x18\n\x0bis_selected\x18\x05 \x01(\x08H\x04\x88\x01\x01\x12\x14\n\x07skin_id\x18\x06 \x01(\rH\x05\x88\x01\x01\x12\x0f\n\x07\x61\x63tions\x18\x07 \x03(\r\x12&\n\x06skills\x18\x08 \x03(\x0b\x32\x16.freefire.PetSkillInfo\x12\x1e\n\x11selected_skill_id\x18\t \x01(\rH\x06\x88\x01\x01\x12\x1b\n\x0eis_marked_star\x18\n \x01(\x08H\x07\x88\x01\x01\x12\x15\n\x08\x65nd_time\x18\x0b \x01(\rH\x08\x88\x01\x01\x42\x05\n\x03_idB\x07\n\x05_nameB\x08\n\x06_levelB\x06\n\x04_expB\x0e\n\x0c_is_selectedB\n\n\x08_skin_idB\x14\n\x12_selected_skill_idB\x11\n\x0f_is_marked_starB\x0b\n\t_end_time\"<\n\x0e\x44iamondCostRes\x12\x19\n\x0c\x64iamond_cost\x18\x01 \x01(\rH\x00\x88\x01\x01\x42\x0f\n\r_diamond_cost\"\xfd\x03\n\x14\x43reditScoreInfoBasic\x12\x19\n\x0c\x63redit_score\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x14\n\x07is_init\x18\x02 \x01(\x08H\x01\x88\x01\x01\x12\x30\n\x0creward_state\x18\x03 \x01(\x0e\x32\x15.freefire.RewardStateH\x02\x88\x01\x01\x12&\n\x19periodic_summary_like_cnt\x18\x04 \x01(\rH\x03\x88\x01\x01\x12)\n\x1cperiodic_summary_illegal_cnt\x18\x05 \x01(\rH\x04\x88\x01\x01\x12\x1d\n\x10weekly_match_cnt\x18\x06 \x01(\rH\x05\x88\x01\x01\x12(\n\x1bperiodic_summary_start_time\x18\x07 \x01(\x03H\x06\x88\x01\x01\x12&\n\x19periodic_summary_end_time\x18\x08 \x01(\x03H\x07\x88\x01\x01\x42\x0f\n\r_credit_scoreB\n\n\x08_is_initB\x0f\n\r_reward_stateB\x1c\n\x1a_periodic_summary_like_cntB\x1f\n\x1d_periodic_summary_illegal_cntB\x13\n\x11_weekly_match_cntB\x1e\n\x1c_periodic_summary_start_timeB\x1c\n\x1a_periodic_summary_end_time\"-\n\x0c\x45quipAchInfo\x12\x0e\n\x06\x61\x63h_id\x18\x01 \x01(\r\x12\r\n\x05level\x18\x02 \x01(\r\"\xfa\x06\n\x17\x41\x63\x63ountPersonalShowInfo\x12\x33\n\nbasic_info\x18\x01 \x01(\x0b\x32\x1a.freefire.AccountInfoBasicH\x00\x88\x01\x01\x12\x32\n\x0cprofile_info\x18\x02 \x01(\x0b\x32\x17.freefire.AvatarProfileH\x01\x88\x01\x01\x12$\n\x17ranking_leaderboard_pos\x18\x03 \x01(\x05H\x02\x88\x01\x01\x12#\n\x04news\x18\x04 \x03(\x0b\x32\x15.freefire.AccountNews\x12.\n\x0fhistory_ep_info\x18\x05 \x03(\x0b\x32\x15.freefire.BasicEPInfo\x12\x35\n\x0f\x63lan_basic_info\x18\x06 \x01(\x0b\x32\x17.freefire.ClanInfoBasicH\x03\x88\x01\x01\x12;\n\x12\x63\x61ptain_basic_info\x18\x07 \x01(\x0b\x32\x1a.freefire.AccountInfoBasicH\x04\x88\x01\x01\x12(\n\x08pet_info\x18\x08 \x01(\x0b\x32\x11.freefire.PetInfoH\x05\x88\x01\x01\x12\x33\n\x0bsocial_info\x18\t \x01(\x0b\x32\x19.freefire.SocialBasicInfoH\x06\x88\x01\x01\x12\x37\n\x10\x64iamond_cost_res\x18\n \x01(\x0b\x32\x18.freefire.DiamondCostResH\x07\x88\x01\x01\x12>\n\x11\x63redit_score_info\x18\x0b \x01(\x0b\x32\x1e.freefire.CreditScoreInfoBasicH\x08\x88\x01\x01\x12=\n\x10pre_veteran_type\x18\x0c \x01(\x0e\x32\x1e.freefire.PreVeteranActionTypeH\t\x88\x01\x01\x12,\n\x0c\x65quipped_ach\x18\r \x03(\x0b\x32\x16.freefire.EquipAchInfoB\r\n\x0b_basic_infoB\x0f\n\r_profile_infoB\x1a\n\x18_ranking_leaderboard_posB\x12\n\x10_clan_basic_infoB\x15\n\x13_captain_basic_infoB\x0b\n\t_pet_infoB\x0e\n\x0c_social_infoB\x13\n\x11_diamond_cost_resB\x14\n\x12_credit_score_infoB\x13\n\x11_pre_veteran_type*\xa0\x01\n\x10VeteranLeaveDays\x12\x19\n\x15VeteranLeaveDays_NONE\x10\x00\x12\x1a\n\x16VeteranLeaveDays_SHORT\x10\x01\x12\x1b\n\x17VeteranLeaveDays_NORMAL\x10\x02\x12\x19\n\x15VeteranLeaveDays_LONG\x10\x03\x12\x1d\n\x19VeteranLeaveDays_VERYLONG\x10\x04*w\n\x14PreVeteranActionType\x12\x1d\n\x19PreVeteranActionType_NONE\x10\x00\x12!\n\x1dPreVeteranActionType_ACTIVITY\x10\x01\x12\x1d\n\x19PreVeteranActionType_BUFF\x10\x02*s\n\x12\x45xternalIconStatus\x12\x1b\n\x17\x45xternalIconStatus_NONE\x10\x00\x12!\n\x1d\x45xternalIconStatus_NOT_IN_USE\x10\x01\x12\x1d\n\x19\x45xternalIconStatus_IN_USE\x10\x02*t\n\x14\x45xternalIconShowType\x12\x1d\n\x19\x45xternalIconShowType_NONE\x10\x00\x12\x1f\n\x1b\x45xternalIconShowType_FRIEND\x10\x01\x12\x1c\n\x18\x45xternalIconShowType_ALL\x10\x02*\xf0\x02\n\tHighLight\x12\x12\n\x0eHighLight_NONE\x10\x00\x12\x14\n\x10HighLight_BR_WIN\x10\x01\x12\x14\n\x10HighLight_CS_MVP\x10\x02\x12\x1b\n\x17HighLight_BR_STREAK_WIN\x10\x03\x12\x1b\n\x17HighLight_CS_STREAK_WIN\x10\x04\x12#\n\x1fHighLight_CS_RANK_GROUP_UPGRADE\x10\x05\x12\x16\n\x12HighLight_TEAM_ACE\x10\x06\x12 \n\x1cHighLight_WEAPON_POWER_TITLE\x10\x07\x12#\n\x1fHighLight_BR_RANK_GROUP_UPGRADE\x10\t\x12&\n\"HighLight_BR_STREAK_WIN_EXECELLENT\x10\n\x12&\n\"HighLight_CS_STREAK_WIN_EXECELLENT\x10\x0b\x12\x15\n\x11HighLight_VETERAN\x10\x0c*T\n\x06Gender\x12\x0f\n\x0bGender_NONE\x10\x00\x12\x0f\n\x0bGender_MALE\x10\x01\x12\x11\n\rGender_FEMALE\x10\x02\x12\x15\n\x10Gender_UNLIMITED\x10\xe7\x07*\xf5\x03\n\x08Language\x12\x11\n\rLanguage_NONE\x10\x00\x12\x0f\n\x0bLanguage_EN\x10\x01\x12\x1a\n\x16Language_CN_SIMPLIFIED\x10\x02\x12\x1b\n\x17Language_CN_TRADITIONAL\x10\x03\x12\x11\n\rLanguage_Thai\x10\x04\x12\x17\n\x13Language_VIETNAMESE\x10\x05\x12\x17\n\x13Language_INDONESIAN\x10\x06\x12\x17\n\x13Language_PORTUGUESE\x10\x07\x12\x14\n\x10Language_SPANISH\x10\x08\x12\x14\n\x10Language_RUSSIAN\x10\t\x12\x13\n\x0fLanguage_KOREAN\x10\n\x12\x13\n\x0fLanguage_FRENCH\x10\x0b\x12\x13\n\x0fLanguage_GERMAN\x10\x0c\x12\x14\n\x10Language_TURKISH\x10\r\x12\x12\n\x0eLanguage_HINDI\x10\x0e\x12\x15\n\x11Language_JAPANESE\x10\x0f\x12\x15\n\x11Language_ROMANIAN\x10\x10\x12\x13\n\x0fLanguage_ARABIC\x10\x11\x12\x14\n\x10Language_BURMESE\x10\x12\x12\x11\n\rLanguage_URDU\x10\x13\x12\x14\n\x10Language_BENGALI\x10\x14\x12\x17\n\x12Language_UNLIMITED\x10\xe7\x07*l\n\nTimeOnline\x12\x13\n\x0fTimeOnline_NONE\x10\x00\x12\x16\n\x12TimeOnline_WORKDAY\x10\x01\x12\x16\n\x12TimeOnline_WEEKEND\x10\x02\x12\x19\n\x14TimeOnline_UNLIMITED\x10\xe7\x07*\x84\x01\n\nTimeActive\x12\x13\n\x0fTimeActive_NONE\x10\x00\x12\x16\n\x12TimeActive_MORNING\x10\x01\x12\x18\n\x14TimeActive_AFTERNOON\x10\x02\x12\x14\n\x10TimeActive_NIGHT\x10\x03\x12\x19\n\x14TimeActive_UNLIMITED\x10\xe7\x07*\xf6\x02\n\x11PlayerBattleTagID\x12\x1a\n\x16PlayerBattleTagID_NONE\x10\x00\x12!\n\x1cPlayerBattleTagID_DOMINATION\x10\xcd\x08\x12\x1e\n\x19PlayerBattleTagID_UNCROWN\x10\xce\x08\x12\"\n\x1dPlayerBattleTagID_BESTPARTNER\x10\xcf\x08\x12\x1d\n\x18PlayerBattleTagID_SNIPER\x10\xd0\x08\x12\x1c\n\x17PlayerBattleTagID_MELEE\x10\xd1\x08\x12!\n\x1cPlayerBattleTagID_PEACEMAKER\x10\xd2\x08\x12\x1d\n\x18PlayerBattleTagID_AMBUSH\x10\xd3\x08\x12 \n\x1bPlayerBattleTagID_SHORTSTOP\x10\xd4\x08\x12\x1e\n\x19PlayerBattleTagID_RAMPAGE\x10\xd5\x08\x12\x1d\n\x18PlayerBattleTagID_LEADER\x10\xd6\x08*\xe4\x01\n\tSocialTag\x12\x12\n\x0eSocialTag_NONE\x10\x00\x12\x16\n\x11SocialTag_FASHION\x10\xb5\x10\x12\x15\n\x10SocialTag_SOCIAL\x10\xb6\x10\x12\x16\n\x11SocialTag_VETERAN\x10\xb7\x10\x12\x15\n\x10SocialTag_NEWBIE\x10\xb8\x10\x12\x19\n\x14SocialTag_PLAYFORWIN\x10\xb9\x10\x12\x19\n\x14SocialTag_PLAYFORFUN\x10\xba\x10\x12\x16\n\x11SocialTag_VOICEON\x10\xbb\x10\x12\x17\n\x12SocialTag_VOICEOFF\x10\xbc\x10*\x80\x01\n\nModePrefer\x12\x13\n\x0fModePrefer_NONE\x10\x00\x12\x11\n\rModePrefer_BR\x10\x01\x12\x11\n\rModePrefer_CS\x10\x02\x12\x1c\n\x18ModePrefer_ENTERTAINMENT\x10\x03\x12\x19\n\x14ModePrefer_UNLIMITED\x10\xe7\x07*X\n\x08RankShow\x12\x11\n\rRankShow_NONE\x10\x00\x12\x0f\n\x0bRankShow_BR\x10\x01\x12\x0f\n\x0bRankShow_CS\x10\x02\x12\x17\n\x12RankShow_UNLIMITED\x10\xe7\x07*L\n\x1b\x45LeaderBoardTitleRegionType\x12\x08\n\x04None\x10\x00\x12\x0b\n\x07\x43ountry\x10\x01\x12\x0c\n\x08Province\x10\x02\x12\x08\n\x04\x43ity\x10\x03*6\n\nUnlockType\x12\x13\n\x0fUnlockType_NONE\x10\x00\x12\x13\n\x0fUnlockType_LINK\x10\x01*E\n\x0b\x45quipSource\x12\x14\n\x10\x45quipSource_SELF\x10\x00\x12 \n\x1c\x45quipSource_CONFIDANT_FRIEND\x10\x01*\xfa\x01\n\x08NewsType\x12\x11\n\rNewsType_NONE\x10\x00\x12\x11\n\rNewsType_RANK\x10\x01\x12\x14\n\x10NewsType_LOTTERY\x10\x02\x12\x15\n\x11NewsType_PURCHASE\x10\x03\x12\x18\n\x14NewsType_TREASUREBOX\x10\x04\x12\x16\n\x12NewsType_ELITEPASS\x10\x05\x12\x1a\n\x16NewsType_EXCHANGESTORE\x10\x06\x12\x13\n\x0fNewsType_BUNDLE\x10\x07\x12#\n\x1fNewsType_LOTTERYSPECIALEXCHANGE\x10\x08\x12\x13\n\x0fNewsType_OTHERS\x10\t*]\n\x0bRewardState\x12\x18\n\x14REWARD_STATE_INVALID\x10\x00\x12\x1a\n\x16REWARD_STATE_UNCLAIMED\x10\x01\x12\x18\n\x14REWARD_STATE_CLAIMED\x10\x02\x62\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR_ACC, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR_ACC, 'AccountPersonalShow_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR_ACC._options = None
    _globals['_VETERANLEAVEDAYS']._serialized_start=7312
    _globals['_VETERANLEAVEDAYS']._serialized_end=7472
    _globals['_PREVETERANACTIONTYPE']._serialized_start=7474
    _globals['_PREVETERANACTIONTYPE']._serialized_end=7593
    _globals['_EXTERNALICONSTATUS']._serialized_start=7595
    _globals['_EXTERNALICONSTATUS']._serialized_end=7710
    _globals['_EXTERNALICONSHOWTYPE']._serialized_start=7712
    _globals['_EXTERNALICONSHOWTYPE']._serialized_end=7828
    _globals['_HIGHLIGHT']._serialized_start=7831
    _globals['_HIGHLIGHT']._serialized_end=8199
    _globals['_GENDER']._serialized_start=8201
    _globals['_GENDER']._serialized_end=8285
    _globals['_LANGUAGE']._serialized_start=8288
    _globals['_LANGUAGE']._serialized_end=8789
    _globals['_TIMEONLINE']._serialized_start=8791
    _globals['_TIMEONLINE']._serialized_end=8899
    _globals['_TIMEACTIVE']._serialized_start=8902
    _globals['_TIMEACTIVE']._serialized_end=9034
    _globals['_PLAYERBATTLETAGID']._serialized_start=9037
    _globals['_PLAYERBATTLETAGID']._serialized_end=9411
    _globals['_SOCIALTAG']._serialized_start=9414
    _globals['_SOCIALTAG']._serialized_end=9642
    _globals['_MODEPREFER']._serialized_start=9645
    _globals['_MODEPREFER']._serialized_end=9773
    _globals['_RANKSHOW']._serialized_start=9775
    _globals['_RANKSHOW']._serialized_end=9863
    _globals['_ELEADERBOARDTITLEREGIONTYPE']._serialized_start=9865
    _globals['_ELEADERBOARDTITLEREGIONTYPE']._serialized_end=9941
    _globals['_UNLOCKTYPE']._serialized_start=9943
    _globals['_UNLOCKTYPE']._serialized_end=9997
    _globals['_EQUIPSOURCE']._serialized_start=9999
    _globals['_EQUIPSOURCE']._serialized_end=10068
    _globals['_NEWSTYPE']._serialized_start=10071
    _globals['_NEWSTYPE']._serialized_end=10321
    _globals['_REWARDSTATE']._serialized_start=10323
    _globals['_REWARDSTATE']._serialized_end=10416
    _globals['_ACCOUNTPREFERS']._serialized_start=40
    _globals['_ACCOUNTPREFERS']._serialized_end=228
    _globals['_EXTERNALICONINFO']._serialized_start=231
    _globals['_EXTERNALICONINFO']._serialized_end=369
    _globals['_SOCIALHIGHLIGHT']._serialized_start=371
    _globals['_SOCIALHIGHLIGHT']._serialized_end=463
    _globals['_WEAPONPOWERTITLEINFO']._serialized_start=466
    _globals['_WEAPONPOWERTITLEINFO']._serialized_end=718
    _globals['_GUILDWARTITLEINFO']._serialized_start=721
    _globals['_GUILDWARTITLEINFO']._serialized_end=894
    _globals['_LEADERBOARDTITLEINFO']._serialized_start=897
    _globals['_LEADERBOARDTITLEINFO']._serialized_end=1043
    _globals['_SOCIALBASICINFO']._serialized_start=1046
    _globals['_SOCIALBASICINFO']._serialized_end=1553
    _globals['_SOCIALHIGHLIGHTSWITHSOCIALBASICINFO']._serialized_start=1556
    _globals['_SOCIALHIGHLIGHTSWITHSOCIALBASICINFO']._serialized_end=1702
    _globals['_OCCUPATIONINFO']._serialized_start=1704
    _globals['_OCCUPATIONINFO']._serialized_end=1803
    _globals['_OCCUPATIONSEASONINFO']._serialized_start=1805
    _globals['_OCCUPATIONSEASONINFO']._serialized_end=1905
    _globals['_ACCOUNTINFOBASIC']._serialized_start=1908
    _globals['_ACCOUNTINFOBASIC']._serialized_end=3519
    _globals['_AVATARSKILLSLOT']._serialized_start=3522
    _globals['_AVATARSKILLSLOT']._serialized_end=3676
    _globals['_AVATARPROFILE']._serialized_start=3679
    _globals['_AVATARPROFILE']._serialized_end=4189
    _globals['_ACCOUNTNEWSCONTENT']._serialized_start=4192
    _globals['_ACCOUNTNEWSCONTENT']._serialized_end=4536
    _globals['_ACCOUNTNEWS']._serialized_start=4539
    _globals['_ACCOUNTNEWS']._serialized_end=4706
    _globals['_BASICEPINFO']._serialized_start=4709
    _globals['_BASICEPINFO']._serialized_end=4990
    _globals['_CLANINFOBASIC']._serialized_start=4993
    _globals['_CLANINFOBASIC']._serialized_end=5278
    _globals['_PETSKILLINFO']._serialized_start=5280
    _globals['_PETSKILLINFO']._serialized_end=5404
    _globals['_PETINFO']._serialized_start=5407
    _globals['_PETINFO']._serialized_end=5795
    _globals['_DIAMONDCOSTRES']._serialized_start=5797
    _globals['_DIAMONDCOSTRES']._serialized_end=5857
    _globals['_CREDITSCOREINFOBASIC']._serialized_start=5860
    _globals['_CREDITSCOREINFOBASIC']._serialized_end=6369
    _globals['_EQUIPACHINFO']._serialized_start=6371
    _globals['_EQUIPACHINFO']._serialized_end=6416
    _globals['_ACCOUNTPERSONALSHOWINFO']._serialized_start=6419
    _globals['_ACCOUNTPERSONALSHOWINFO']._serialized_end=7309

# --- 5. main_pb2.py (sample.proto) ---
DESCRIPTOR_SAMPLE = _descriptor_pool.Default().AddSerializedFile(b'\n\x0csample.proto\"*\n\x12SearchWorkshopCode\x12\t\n\x01\x61\x18\x01 \x01(\t\x12\t\n\x01\x62\x18\x02 \x01(\x05\"-\n\x15GetPlayerPersonalShow\x12\t\n\x01\x61\x18\x01 \x01(\x03\x12\t\n\x01\x62\x18\x02 \x01(\x05\"\xf8\x08\n\x0cJwtGenerator\x12\x11\n\ttimestamp\x18\x03 \x01(\t\x12\x11\n\tgame_name\x18\x04 \x01(\t\x12\x14\n\x0cversion_code\x18\x05 \x01(\x05\x12\x13\n\x0b\x61pp_version\x18\x07 \x01(\t\x12\x17\n\x0f\x61ndroid_version\x18\x08 \x01(\t\x12\x13\n\x0b\x64\x65vice_type\x18\t \x01(\t\x12\x18\n\x10network_provider\x18\n \x01(\t\x12\x14\n\x0cnetwork_type\x18\x0b \x01(\t\x12\x14\n\x0cscreen_width\x18\x0c \x01(\x05\x12\x15\n\rscreen_height\x18\r \x01(\x05\x12\x0b\n\x03\x64pi\x18\x0e \x01(\t\x12\x10\n\x08\x63pu_info\x18\x0f \x01(\t\x12\x0b\n\x03\x66ps\x18\x10 \x01(\x05\x12\x11\n\tgpu_model\x18\x11 \x01(\t\x12\x16\n\x0eopengl_version\x18\x12 \x01(\t\x12\x11\n\tdevice_id\x18\x13 \x01(\t\x12\x12\n\nip_address\x18\x14 \x01(\t\x12\x10\n\x08language\x18\x15 \x01(\t\x12\x13\n\x0b\x64\x65vice_hash\x18\x16 \x01(\t\x12\x14\n\x0cos_api_level\x18\x17 \x01(\t\x12\x15\n\ros_build_type\x18\x18 \x01(\t\x12\x14\n\x0c\x64\x65vice_model\x18\x19 \x01(\t\x12\x19\n\x11package_signature\x18\x1d \x01(\t\x12\x12\n\nuser_level\x18\x1e \x01(\x05\x12\x14\n\x0c\x63\x61rrier_name\x18) \x01(\t\x12\x1a\n\x12network_generation\x18* \x01(\t\x12\x15\n\rapp_signature\x18\x39 \x01(\t\x12\x11\n\tplayer_id\x18< \x01(\x03\x12\x12\n\nsession_id\x18= \x01(\x03\x12\x10\n\x08match_id\x18> \x01(\x05\x12\r\n\x05score\x18@ \x01(\x03\x12\x13\n\x0btotal_score\x18\x41 \x01(\x03\x12\x12\n\nhigh_score\x18\x42 \x01(\x03\x12\x11\n\tmax_score\x18\x43 \x01(\x03\x12\x13\n\x0bplayer_rank\x18I \x01(\x05\x12\x17\n\x0fnative_lib_path\x18J \x01(\t\x12\x15\n\ris_debuggable\x18L \x01(\x05\x12\x12\n\napp_source\x18M \x01(\t\x12\x0f\n\x07is_beta\x18N \x01(\x05\x12\x11\n\tis_tester\x18O \x01(\x05\x12\x1b\n\x13target_architecture\x18Q \x01(\t\x12\x18\n\x10\x61pp_version_code\x18S \x01(\t\x12\x19\n\x11\x61pp_revision_code\x18U \x01(\x05\x12\x14\n\x0cgraphics_api\x18V \x01(\t\x12\x18\n\x10max_texture_size\x18W \x01(\x05\x12\x17\n\x0fprocessor_count\x18X \x01(\x05\x12\x16\n\x0e\x65ncryption_key\x18Y \x01(\t\x12\x19\n\x11\x66rame_buffer_size\x18\\ \x01(\x05\x12\x15\n\rplatform_type\x18] \x01(\t\x12\x16\n\x0esecurity_token\x18^ \x01(\t\x12\x18\n\x10\x64isplay_settings\x18` \x01(\t\x12\x14\n\x0cis_logged_in\x18\x61 \x01(\x05\x62\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR_SAMPLE, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR_SAMPLE, 'sample_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR_SAMPLE._options = None
    _globals['_SEARCHWORKSHOPCODE']._serialized_start=16
    _globals['_SEARCHWORKSHOPCODE']._serialized_end=58
    _globals['_GETPLAYERPERSONALSHOW']._serialized_start=60
    _globals['_GETPLAYERPERSONALSHOW']._serialized_end=105
    _globals['_JWTGENERATOR']._serialized_start=108
    _globals['_JWTGENERATOR']._serialized_end=1252

# Ensure globals contains LoginReq / LoginRes natively now for App logic
LoginReq = _globals['LoginReq']
LoginRes = _globals['LoginRes']

# =====================================================================
# Flask Application Setup
# =====================================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Settings ===
try:
    MAIN_KEY = base64.b64decode('WWcmdGMlREV1aDYlWmNeOA==')
    MAIN_IV = base64.b64decode('Nm95WkRyMjJFM3ljaGpNJQ==')
    logger.info("Successfully decoded MAIN_KEY and MAIN_IV")
except Exception as e:
    logger.error(f"Failed to decode MAIN_KEY or MAIN_IV: {e}")
    raise

USERAGENT = "Dalvik/2.1.0 (Linux; U; Android 13; CPH2095 Build/RKQ1.211119.001)"
RELEASEVERSION = "OB54"

app = Flask(__name__)

# === Helper Functions ===
def pad(text: bytes) -> bytes:
    try:
        padding_length = AES.block_size - (len(text) % AES.block_size)
        return text + bytes([padding_length] * padding_length)
    except Exception as e:
        logger.error(f"Padding failed: {e}")
        raise

def aes_cbc_encrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    try:
        aes = AES.new(key, AES.MODE_CBC, iv=iv)
        return aes.encrypt(pad(plaintext))
    except Exception as e:
        logger.error(f"AES encryption failed: {e}")
        raise

async def json_to_proto(json_data: str, proto_message) -> bytes:
    try:
        parsed = json.loads(json_data) if isinstance(json_data, str) else json_data
        json_format.ParseDict(parsed, proto_message)
        return proto_message.SerializeToString()
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Protobuf conversion failed: {e}")
        raise

async def get_access_token(account: str):
    url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
    payload = f"{account}&response_type=token&client_type=2&client_secret=2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3&client_id=100067"
    headers = {
        'User-Agent': USERAGENT,
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/x-www-form-urlencoded"
    }
    try:
        async with httpx.AsyncClient() as client:
            logger.info(f"Sending access token request to {url}")
            resp = await client.post(url, data=payload, headers=headers, timeout=20.0)
            resp.raise_for_status()
            data = resp.json()
            access_token = data.get("access_token", "0")
            open_id = data.get("open_id", "0")
            if access_token == "0" or open_id == "0":
                logger.warning(f"Invalid access token or open_id received: {data}")
            return access_token, open_id
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error during access token request: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        logger.error(f"Failed to get access token: {e}")
        raise

async def create_jwt(uid: str, password: str):
    try:
        account = f"uid={uid}&password={password}"
        logger.info(f"Generating JWT for uid: {uid}")
        token_val, open_id = await get_access_token(account)
        body = json.dumps({
            "open_id": open_id,
            "open_id_type": "4",
            "login_token": token_val,
            "orign_platform_type": "4"
        })
        proto_bytes = await json_to_proto(body, LoginReq())
        payload = aes_cbc_encrypt(MAIN_KEY, MAIN_IV, proto_bytes)
        url = "https://loginbp.ggblueshark.com/MajorLogin"
        headers = {
            'User-Agent': USERAGENT,
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/octet-stream",
            'Expect': "100-continue",
            'X-Unity-Version': "2022.3.47f1",
            'X-GA': "v1 1",
            'ReleaseVersion': RELEASEVERSION
        }
        async with httpx.AsyncClient() as client:
            logger.info(f"Sending JWT request to {url}")
            resp = await client.post(url, data=payload, headers=headers, timeout=30.0)
            resp.raise_for_status()
            try:
                login_res_msg = LoginRes.FromString(resp.content)
                msg = json.loads(json_format.MessageToJson(login_res_msg))
            except Exception as parse_e:
                logger.error(f"Failed to parse LoginRes protobuf: {parse_e}")
                raise
            token = msg.get('token', '0')
            if token == '0':
                logger.warning(f"No token received in response: {msg}")
            return {
                'token': f"{token}",
                'region': msg.get('lockRegion', '0'),
                'server_url': msg.get('serverUrl', '0')
            }
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error during JWT creation: {e.response.status_code} - {e.response.text}")
        raise
    except Exception as e:
        logger.error(f"JWT creation failed: {e}")
        raise

# === Health Check Route ===
@app.route('/api/health', methods=['GET'])
def health_check():
    logger.info("Health check endpoint called")
    return jsonify({"status": "API is running", "version": RELEASEVERSION}), 200

# === API Route: generate token ===
@app.route('/api/token', methods=['GET'])
def get_jwt():
    try:
        logger.info(f"Received request to /api/token with args: {request.args}")
        uid = request.args.get('uid')
        password = request.args.get('password')
        if not uid or not password:
            logger.warning("Missing uid or password in request")
            return jsonify({"error": "Please provide both uid and password."}), 400
        result = asyncio.run(create_jwt(uid, password))
        logger.info(f"JWT generated successfully for uid: {uid}")
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in get_jwt: {e}")
        return jsonify({"error": f"Failed to generate JWT: {str(e)}"}), 500

# === API Route: decode JWT ===
@app.route('/api/decode', methods=['GET'])
def decode_jwt():
    try:
        jwt_token = request.args.get('jwt') or request.args.get('token')
        if not jwt_token:
            return jsonify({"error": "Please provide a JWT token via 'jwt' or 'token' query parameter."}), 400

        parts = jwt_token.split('.')
        if len(parts) < 2:
            return jsonify({"error": "Malformed JWT: expected at least header and payload separated by '.'"}), 400

        def b64url_decode(s: str) -> bytes:
            s = s.replace('-', '+').replace('_', '/')
            padding = len(s) % 4
            if padding != 0:
                s += '=' * (4 - padding)
            return base64.b64decode(s)

        header_json = {}
        payload_json = {}
        signature = parts[2] if len(parts) > 2 else ""

        try:
            raw_header = b64url_decode(parts[0])
            header_json = json.loads(raw_header.decode('utf-8'))
        except Exception as e:
            logger.warning(f"Failed to decode JWT header: {e}")
            header_json = {"error": "Failed to decode header", "raw": parts[0]}

        try:
            raw_payload = b64url_decode(parts[1])
            payload_json = json.loads(raw_payload.decode('utf-8'))
        except Exception as e:
            logger.warning(f"Failed to decode JWT payload: {e}")
            payload_json = {"error": "Failed to decode payload", "raw": parts[1]}

        return jsonify({
            "header": header_json,
            "payload": payload_json,
            "signature": signature
        }), 200

    except Exception as e:
        logger.error(f"Error decoding JWT: {e}")
        return jsonify({"error": f"Failed to decode JWT: {str(e)}"}), 500

# === Startup() ===
async def startup():
    logger.info("Running startup initialisation (no-op)")
    return

# === Startup / run ===
if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    print(f"[🚀] Starting {__name__.upper()} on port {port} ...")
    try:
        asyncio.run(startup())
    except Exception as e:
        print(f"[⚠️] Startup warning: {e} — continuing without full initialization")
    app.run(host='0.0.0.0', port=port, debug=False)