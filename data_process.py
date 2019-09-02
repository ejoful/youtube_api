#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from ytb_api import YoutubeApi
import pymysql.cursors
import logging
import json
import time



class Data_process(object):
    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='asdf@#123.',
                                     db='maiziedu_first',
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)

    def save_list_result(self):
        channel_id = "UCAEDC_Ku-K6zTVpGi6kLS1g"
        api_key = "AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM"
        authorization = "SAPISIDHASH 1566476655_6d41cfbafc6f997332441ff7f700c598a4a73210"
        cookie = 'YSC=28hWu0m0oGA; s_gl=6a2e51b9ffc40731bf28901719b90714cwIAAABISw==; LOGIN_INFO=AFmmF2swRgIhAN6gGlxa54_JQLqO7esYvWUI-jjQNdueQs8H4Y1Q9NsDAiEAtJ6E8OgyBOtFFHbRtton9z4lr7zVcEqQGucyTbNuFwU:QUQ3MjNmd092Z2VxZFJUdWpUWGZGV0J0RHEtUVhUNzJtOXl1R2pCUFVpXzNUU2FTVTJjb1FQN1NWeTRkYUtuclRzUV9JeTNHallLYUhRU09WMGhBR3dvYnNUdVRKWWMyRTRTX0lad2FKTE9IYmZCMTU4UjVvWUtSMWlFUWI2YVhobi1KbWhPQUxDb1hjWmhLSmZRc0c3ZEpUTEc1OVlaNHJhV2VzTVNQRm1QUXk5VWE1RUU2SDhmN29ITDR4cDAwakQxclpJLUQ1MDdJRC1TbVZlYU9DMzFNSnBXZmpzUVhnd3dCTmx1YzNOX2xqQWdUdy1NdW1EMA==; VISITOR_INFO1_LIVE=idEidP6ZO0w; PREF=f1=50000000&f4=4000000&al=zh-CN&f5=30; _ga=GA1.2.835656688.1563512766; SID=nQcX7zwiHO-3xpbxMCWE0R774JgijHcqJsySvyR_lL5KT76KCIaFfL28Iz6yF2BjrcJQVQ.; HSID=A_EoLLjk-I-p_AcNu; SSID=A7_Iul9_5zGOHWWBv; APISID=bC094xprieLcfVS7/AO4s_zgs4XmJgz2FI; SAPISID=uppH3GPXlPq3O2Ug/ALstYYYV8jb-QfUO1; SIDCC=AN0-TYtg1Ub63X5fw1kNQN3THCTh89mhK2wIfoJqml8aW5HOyPuih4XB-WVBLur1ItdbBE4I8gM'
        # post_data = json.loads(post_data)
        x = YoutubeApi(channel_id, api_key)

        next_page_token = None
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "select next_page_token from tbl_ytb_search_list order by id desc limit 1;"
            cursor.execute(sql)
            token_result = cursor.fetchone()
            # if token_result:
                # next_page_token = token_result['next_page_token']

        while 1 < 2:
            response_str = x.list_creator_videos(authorization, cookie, next_page_token)
            response_dict = json.loads(response_str)
            # print(response_dict['nextPageToken'])
            # print(response_str)
            # print(response_dict['videos'])
            # list = response_dict['videos']
            # print(list[0])
            # exit()
            if  'nextPageToken' not in response_dict:
                item = {'next_page_token': None, 'data': response_str}
                self.insert_ytb_search_list(item)
                self.insert_ytb_video(response_dict['videos'])
                break
            else:
                next_page_token = response_dict['nextPageToken']
                item = {'next_page_token': response_dict['nextPageToken'], 'data': response_str}
                self.insert_ytb_search_list(item)
                self.insert_ytb_video(response_dict['videos'])

    def insert_ytb_search_list(self, item):
        with self.connection.cursor() as cursor:

            sql = """INSERT INTO `tbl_ytb_search_list` (`id`, `next_page_token`, `data`,`create_time`)
                                VALUES (null,%s,%s,%s)"""
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            lis = (item['next_page_token'], item['data'], create_time)
            cursor.execute(sql, lis)
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        self.connection.commit()

    def save_playlists_list_result(self):
        channel_id = "UCAEDC_Ku-K6zTVpGi6kLS1g"
        api_key = "AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM"
        authorization = "Bearer ya29.Gl9vB7HfBGbsyZhyJ4zOTTieD1lUC7XYN91qMGA45f6JnHmHvPGudmlRoKNVwrkTjvGf4gtZD9ak7W-v9uxThWCqIw-b7cw0qhoJJ5UzU13Ky55Bk9Kdf23hh-jpKh2lBQ"
        x = YoutubeApi(channel_id, api_key)
        next_page_token = None

        while 1 < 2:
            response_str = x.playlists_list(authorization, next_page_token)
            response_dict = json.loads(response_str)
            # print(response_dict)
            # print(response_str)
            # print(response_dict['videos'])
            # list = response_dict['videos']
            # print(list[0])
            # exit()
            if  'nextPageToken' not in response_dict:
                item = {'next_page_token': None, 'data': response_str}
                self.insert_ytb_playlists_list(item)
                self.insert_ytb_playlist(response_dict['items'])
                break
            else:
                next_page_token = response_dict['nextPageToken']
                item = {'next_page_token': response_dict['nextPageToken'], 'data': response_str}
                self.insert_ytb_playlists_list(item)
                self.insert_ytb_playlist(response_dict['items'])

    def get_playlists_items(self):
        channel_id = "UCAEDC_Ku-K6zTVpGi6kLS1g"
        api_key = "AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM"
        authorization = "Bearer ya29.Gl9vB-rw5dfFnH7Tmb4oCqpvfMWJ6dfXDqDyHaL1RaMDgRJ19MnS6v6EcKMk3KFsLCW6tOLJRRsvCasR4IeUGhCDWOU4fMExrMCzSSIu4Zxix2fEQYhRPCXrBpV0ZUK60A"
        x = YoutubeApi(channel_id, api_key)
        next_page_token = None

        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM  `tbl_ytb_playlist`;"
            cursor.execute(sql)
            playlist_results = cursor.fetchall()
            for playlist in playlist_results:
                while 1 < 2:
                    response_str = x.playlists_items_list(authorization, playlist['list_id'], next_page_token)
                    response_dict = json.loads(response_str)
                    # print(response_dict['items'])
                    # exit()
                    if response_dict is not None:
                        if  'nextPageToken' not in response_dict:
                            self.update_ytb_video(response_dict['items'])
                            break
                        else:
                            next_page_token = response_dict['nextPageToken']
                            self.update_ytb_video(response_dict['items'])

    def insert_ytb_playlists_list(self, item):
        with self.connection.cursor() as cursor:

            sql = """INSERT INTO `tbl_ytb_playlists_list` (`id`, `next_page_token`, `data`,`create_time`)
                                VALUES (null,%s,%s,%s)"""
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            lis = (item['next_page_token'], item['data'], create_time)
            cursor.execute(sql, lis)
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        self.connection.commit()


    def insert_ytb_video(self, items):
        #todo
        #INSERT INTO `tbl_ytb_video` (`id`, `video_id`, `title`, `position`, `video_link`, `data`, `vid`, `cid`, `list_id`, `is_update`, `create_time`) VALUES (NULL, '1', '1', NULL, 'https://www.youtube.com/watch?v=', NULL, NULL, NULL, NULL, '0', current_timestamp());
        str = ''
        for x in items:
            str += "(NULL, '"+x['videoId']+"', '"+pymysql.escape_string(x['title'].rstrip().lstrip())+"', NULL, 'https://www.youtube.com/watch?v="+x['videoId']+"', NULL, NULL, NULL, NULL, '0', current_timestamp()),"
        str = str[0:-1]
        with self.connection.cursor() as cursor:

            sql = """INSERT INTO `tbl_ytb_video` (`id`, `video_id`, `title`, `position`, `video_link`, `data`, `vid`, `cid`, `list_id`, `is_update`, `create_time`) VALUES """ + str
            # create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # lis = (item['next_page_token'], item['data'], create_time)
            cursor.execute(sql)
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        self.connection.commit()


    def insert_ytb_playlist(self, items):
        for item in items:
            with self.connection.cursor() as cursor:
                sql = "insert `tbl_ytb_playlist` (`id`, `list_id`, `title`, `data`, `cid`, `is_old`, `create_time`) VALUES (NULL, %s, %s, NULL, NULL, '1', CURRENT_TIME());"
                lis = (item['id'], item['snippet']['title'])
                cursor.execute(sql, lis)
        sql = "update tbl_ytb_playlist as a, tbl_course as b set a.cid = b.id where a.title=b.title;"
        cursor.execute(sql)
        self.connection.commit()


    def update_ytb_video(self, items):
        for item in items:
            with self.connection.cursor() as cursor:
                sql = "update `tbl_ytb_video` set list_id='"+item['snippet']['playlistId']+"' ,list_position='"+str(item['snippet']['position'])+"' ,is_old='1' where video_id='"+item['contentDetails']['videoId']+"' ;"
                # create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                # lis = (item['next_page_token'], item['data'], create_time)
                cursor.execute(sql)
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()

    def create_playlist(self):
        channel_id = "UCAEDC_Ku-K6zTVpGi6kLS1g"
        api_key = "AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM"
        authorization = "Bearer ya29.Gl9vB8IZO0rcK2jzlwrUlMNDx7sI-WEAfqGb7Q7Vjxsm5-cFw8AdcKv81ijB4OGT8nGu1Isxe7V9dALEMXZKv2wsJAhZwBBaxrjHO1Dzc7BHs1_glFrg0c2909p_ZRC1yw"
        x = YoutubeApi(channel_id, api_key)
        with self.connection.cursor() as cursor:
            # Read a single record title like '" + ctitle + "%' and
            sql = "select * from tbl_course as a where a.list_id is null and a.need_create=1;"
            cursor.execute(sql)
            videos = cursor.fetchall()
            for video in videos:
                data = {
                  "snippet": {
                    "title": video['title'],
                    "description": video['des'],
                    "tags": video['keywords'].split(','),
                    "defaultLanguage": "zh-CN"
                  },
                  "status": {
                    "privacyStatus": "public"
                  }
                }
                # print(type(json.dumps(data)))
                # print(json.dumps(data))
                # exit()
                response_str = x.playlists_insert(authorization, json.dumps(data))
                response_dict = json.loads(response_str)
                print(response_dict)
                sql = "update tbl_course as a set a.list_id='"+response_dict['id']+"' where a.id='"+str(video['id'])+"';"
                cursor.execute(sql)
                self.connection.commit()

    def create_playlist2(self):
        channel_id = "UCAEDC_Ku-K6zTVpGi6kLS1g"
        api_key = "AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM"
        x = YoutubeApi(channel_id, api_key)
        with self.connection.cursor() as cursor:
            # Read a single record title like '" + ctitle + "%' and
            sql = "select * from tbl_course as a where a.list_id is null and a.need_create=1;"
            cursor.execute(sql)
            courses = cursor.fetchall()
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            for course in courses:
                sql = "select * from tbl_video as a where a.video_id is not null and a.course_id='"+str(course['id'])+"' order by a.position asc limit 50;"
                cursor.execute(sql)
                videos = cursor.fetchall()
                video_ids = ''
                for video in videos:
                    video_ids += video['video_id'] + ','
                video_ids = video_ids[0:-1]
                data = {
                    'video_ids': video_ids,
                    'source_playlist_id': '',
                    'n': course['title'],
                    'p': 'public',
                    'session_token': 'QUFFLUhqblVlNmQ0VkxISzI0aS1TVk5XVndmRl9TUnlsZ3xBQ3Jtc0ttQlhNNlpXcEtCRzNZOF9PQkY1TVVoRnBlZTB5eVl4SFJ3NmRlWUJ3Q054TjFaVEdPbENHQWp3RVVhcnVfNGEyYU1veWdQdFNRdlo1T1dPV2ZQUGo1XzFBVklubjVwS211Z1FvSndUdlMtZjJRX19qUlhxZzQwa2taYkhnV0trdzZFYVdBeGIzVGdQNzNLWExhbGthTFE3R1JaLU5NQU1uZGtOaUJIU2RDUFpEa2E3d1E='
                }
                # print(type(json.dumps(data)))
                # print(json.dumps(data))
                # exit()
                response_str = x.playlists_create(data)
                response_dict = json.loads(response_str)
                print(response_dict)
                if response_dict.get('result').get('playlistId') is not None:
                    sql = "update tbl_course as a set a.list_id='"+response_dict['result']['playlistId']+"', a.create_playlist_time='"+create_time+"' where a.id='"+str(course['id'])+"';"
                    cursor.execute(sql)
                    self.connection.commit()

    def update_video_description(self):
        channel_id = "UCAEDC_Ku-K6zTVpGi6kLS1g"
        api_key = "AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM"
        x = YoutubeApi(channel_id, api_key)
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with self.connection.cursor() as cursor:
            # Read a single record title like '" + ctitle + "%' and
            sql = "select a.*,b.des,b.keywords,b.title as ctitle,b.list_id as blist_id from tbl_video as a,tbl_course as b where a.course_id=b.id and b.list_id is not null and a.is_update_des=0 limit 120;"
            cursor.execute(sql)
            videos = cursor.fetchall()
            for video in videos:
                title = video['ctitle'] + '-' + video['title']
                des = video['ctitle'] + '  播放列表: https://www.youtube.com/watch?v=' + video['video_id'] + '&list='+video['blist_id'] + '\n'+video['des']
                data = {"encryptedVideoId":video['video_id'],"videoReadMask":{"channelId":true,"videoId":true,"lengthSeconds":true,"premiere":{"all":true},"status":true,"thumbnailDetails":{"all":true},"title":true,"draftStatus":true,"downloadUrl":true,"watchUrl":true,"permissions":{"all":true},"timeCreatedSeconds":true,"timePublishedSeconds":true,"origin":true,"livestream":{"all":true},"privacy":true,"features":{"all":true},"category":true,"allowComments":true,"commentFilter":true,"defaultCommentSortOrder":true,"ageRestriction":true,"license":true,"audioLanguage":{"all":true},"uncaptionedReason":true,"paidProductPlacement":true,"dateRecorded":{"all":true},"publishing":{"all":true},"allowRatings":true,"allowEmbed":true,"music":{"all":true},"ownedClaim":{"all":true},"location":{"all":true},"liveChat":{"all":true},"gameTitle":{"all":true},"claimDetails":{"all":true},"description":true,"tags":{"all":true},"originalFilename":true,"videoStreamUrl":true,"thumbnailEditorState":{"all":true},"scheduledPublishingDetails":{"all":true},"responseStatus":{"all":true},"statusDetails":{"all":true},"sponsorsOnly":{"all":true},"unlistedExpired":true,"crowdsourcingEnabled":true},"title":{"newTitle":title,"shouldSegment":false},"description":{"newDescription":des,"shouldSegment":false},"tags":{"newTags":video['keywords'].split(',')},"context":{"client":{"clientName":62,"clientVersion":"1.20190901.0.0","hl":"zh-CN","gl":"HK","experimentIds":[]},"request":{"returnLogEntry":true,"internalExperimentFlags":[{"key":"upload_copy_file","value":"false"},{"key":"enable_polymer_resin","value":"false"},{"key":"is_browser_support_for_webcam_streaming","value":"true"},{"key":"enable_midroll_ad_insertion","value":"true"},{"key":"web_logging_max_batch","value":"100"},{"key":"html5_load_ads_control_flow","value":"false"},{"key":"video_level_fundraiser_create","value":"false"},{"key":"matterhorn_v1_study","value":"0"},{"key":"highlight_clip_creation_ftue_display_option","value":"0"},{"key":"enable_ve_tracker_key","value":"true"},{"key":"is_browser_supported_for_chromecast_streaming","value":"false"},{"key":"web_gel_debounce_ms","value":"10000"},{"key":"use_first_tick","value":"false"},{"key":"enable_lcr_v1_features","value":"false"},{"key":"force_route_delete_playlist_to_outertube","value":"false"},{"key":"update_super_chat_moderation","value":"false"},{"key":"restudio_hagrid","value":"false"},{"key":"live_chat_unicode_emoji_json_url","value":"https://www.gstatic.com/youtube/img/emojis/emojis-svg-1.json"},{"key":"restudio_web_canary_holdback","value":"false"},{"key":"restudio_onboarding","value":"true"},{"key":"live_chat_continuation_expiration_usec","value":"300000000"},{"key":"log_window_onerror_fraction","value":"1"},{"key":"restudio_thumbnails","value":"false"},{"key":"retry_web_logging_batches","value":"true"},{"key":"enable_live_premieres_creation","value":"true"},{"key":"enable_client_streamz_web","value":"true"},{"key":"restudio_disable_hash","value":"true"},{"key":"log_sequence_info_on_gel_web","value":"false"},{"key":"ignore_empty_xhr","value":"true"},{"key":"analytics_deep_dive_view","value":"true"},{"key":"fill_submit_endpoint_on_preview_web","value":"true"},{"key":"enable_lcr_account_menu","value":"false"},{"key":"analytics_snowball","value":"false"},{"key":"deep_dive_discoverability","value":"0"},{"key":"enable_creator_comment_filters","value":"false"},{"key":"restudio_banners","value":"true"},{"key":"enable_live_studio_ux","value":"true"},{"key":"restudio_upload_link","value":"true"},{"key":"show_livechat_creator_tooltips","value":"false"},{"key":"restudio_hats","value":"true"},{"key":"live_chat_show_settings_in_creator_studio","value":"true"},{"key":"enable_live_studio_url","value":"true"},{"key":"console_log_js_exceptions","value":"true"},{"key":"restudio_scheduled_publishing","value":"true"},{"key":"json_serialize_service_endpoints2","value":"true"},{"key":"web_system_health_fraction","value":"1"},{"key":"add_creator_entities_to_accounts_list","value":"true"},{"key":"channel_fluctuation_decline_experiment","value":"0"},{"key":"flush_onbeforeunload","value":"true"},{"key":"log_js_exceptions_fraction","value":"1"},{"key":"restudio_nav_refresh","value":"true"},{"key":"yta_see_more_link","value":"true"},{"key":"restudio","value":"false"},{"key":"analytics_headlines_holdback_state","value":"1"},{"key":"enable_mobile_crosswalk_selection","value":"false"},{"key":"custom_csi_timeline_use_gel","value":"false"},{"key":"json_serialize_shut_off2","value":"false"},{"key":"content_owner_delegation","value":"false"},{"key":"restudio_comments","value":"true"},{"key":"html5_disable_client_tmp_logs","value":"false"},{"key":"enable_lcr_improved_preview","value":"false"},{"key":"restudio_web_canary","value":"false"},{"key":"html5_force_debug_data_for_client_tmp_logs","value":"false"},{"key":"live_chat_invite_only_mode_creator_ui","value":"false"},{"key":"capping_comment_replies","value":"false"}]},"user":{"onBehalfOfUser":"103906469025013614191"},"clientScreenNonce":"MC4wMTM3MTQzMjg4OTU2NjYyNjE."}}

                # print(type(json.dumps(data)))
                # print(json.dumps(data))
                # exit()
                response_str = x.video_description_update(json.dumps(data))
                response_dict = json.loads(response_str)
                print(response_dict)
                if 'responseContext' in response_dict:
                    print('success')
                    sql = "update tbl_video as a set a.is_update_des=1,a.update_des_time='"+create_time+"' where a.id='" + str(video['id']) + "';"
                    cursor.execute(sql)
                    self.connection.commit()

    def update_playlist_description(self):
        channel_id = "UCAEDC_Ku-K6zTVpGi6kLS1g"
        api_key = "AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM"
        x = YoutubeApi(channel_id, api_key)
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with self.connection.cursor() as cursor:
            # Read a single record title like '" + ctitle + "%' and
            sql = "select a.* from tbl_course as a where a.is_update_playlist_des=0 limit 120;"
            cursor.execute(sql)
            items = cursor.fetchall()
            for item in items:
                data = {
                    'playlist_id': item['list_id'],
                    'playlist_description': item['des'],
                    'session_token': 'QUFFLUhqbmpLUmtkOHFPNm9HYXB5UkZpUnJna0hHdmNvd3xBQ3Jtc0tsSVFHWXV5MEtYTUY3Z2lvUnJ6Z1ZmZFhsNUhfSlJBRTBsRWJMYk1HemotcTFWLVVzMFUwbml4RnJwci1LcndBYmNmdlNORUtkdi1Ma2dIMXNKTGNYN01naVdnN0J1VWRaalpWc1dKeFBCU09fNmNrTjNzSFBBeElBM2hldTk4VjJKNENSQ05vQkNhMS1NZXJiVDFheHhUc0ZOYlBjRDZpdjVWcEpleG1iY2dYZnB4Tzg='
                }
                # print(type(json.dumps(data)))
                # print(json.dumps(data))
                # exit()
                response_str = x.set_playlist_description(data)
                response_dict = json.loads(response_str)
                print(response_dict)
                if 'form_html' in response_dict:
                    print('success')
                    sql = "update tbl_course as a set a.is_update_playlist_des=1,a.update_playlist_des_time='"+create_time+"'  where a.id='" + str(item['id']) + "';"
                    cursor.execute(sql)
                    self.connection.commit()


    def add_vid_cid(self):
        with self.connection.cursor() as cursor:
            # Read a single record title like '" + ctitle + "%' and
            sql = "select a.title as ctitle,b.id,.b.course_id,b.position,b.title as vtitle from tbl_video as b,tbl_course as a where a.id=b.course_id ;"
            cursor.execute(sql)
            videos = cursor.fetchall()
            for x in videos:
                with self.connection.cursor() as cursor:
                    vtitle = pymysql.escape_string(x['vtitle'].replace('.',' '))
                    # vtitle = pymysql.escape_string(x['vtitle'])
                    ctitle = pymysql.escape_string(x['ctitle'])

                    update_sql = "update tbl_ytb_video set vid='" + str(x['id'])+ "',cid='" + str(x['course_id']) + "' where  title like '" + ctitle + "%' and title like '%"+vtitle+"' and vid is null;"
                    cursor.execute(update_sql)
                    vtitle = pymysql.escape_string(x['vtitle'][0:x['vtitle'].find('.')])
                    # print(ctitle + ' '+ vtitle)
                    update_sql = "update tbl_ytb_video set vid='" + str(x['id']) + "',cid='" + str(x['course_id']) + "' where  title like '" + ctitle + ' '+ vtitle + " %' and vid is null;"
                    cursor.execute(update_sql)
                    # print(update_sql)
                    ctitle = pymysql.escape_string(x['ctitle'].replace('.',' ').replace('-',' ').replace(':',''))
                    vtitle = pymysql.escape_string(x['vtitle'][0:x['vtitle'].find('.')])
                    # print(ctitle + ' '+ vtitle)
                    update_sql = "update tbl_ytb_video set vid='" + str(x['id']) + "',cid='" + str(
                        x['course_id']) + "' where  title like '" + ctitle + ' ' + vtitle + " %' and vid is null;"
                    cursor.execute(update_sql)
                    # print(update_sql)
                    vtitle = pymysql.escape_string(x['vtitle'].replace('.',' '))
                    # print(ctitle + ' '+ vtitle)
                    update_sql = "update tbl_ytb_video set vid='" + str(x['id']) + "',cid='" + str(
                        x['course_id']) + "' where  title like '% " + vtitle + "' and vid is null;"
                    cursor.execute(update_sql)
                    print(update_sql)
                    cursor.execute("update tbl_video as a, tbl_ytb_video as b set a.video_id=b.video_id where a.id=b.vid;")
                self.connection.commit()

    def add_position(self):
        with self.connection.cursor() as cursor:
            # Read a single record title like '" + ctitle + "%' and
            sql = "select a.* from tbl_video as a where a.position is null;"
            cursor.execute(sql)
            videos = cursor.fetchall()
            for x in videos:
                index = int(x['title'][0:x['title'].find('.')]) - 1
                update_sql = "update tbl_video set position='" + str(index) + "' where  id = " + str(x['id']) + ";"
                # print(update_sql)
                # exit()
                cursor.execute(update_sql)
            update_sql = "update tbl_video as a,tbl_ytb_video as b set b.position=a.position where  b.video_id = a.video_id;"
            cursor.execute(update_sql)
            self.connection.commit()


    def handle_error(self, e):
        print('handle_error')
        logging.error(e)

    def __del__(self):
        try:
            self.connection.close()
        except Exception as ex:
            print(ex)

a = Data_process()
# a.save_list_result()
# a.add_vid_cid()
# a.add_position()
# a.save_playlists_list_result()
# a.get_playlists_items()
# a.create_playlist()
# a.create_playlist2()
# a.update_video_description()
a.update_playlist_description()