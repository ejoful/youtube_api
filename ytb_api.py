#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import pycurl
import json
import time
from io import BytesIO
import logging
import urllib
import urllib.parse

class YoutubeApi:
    'Youtube api'

    def __init__(self, channel_id, api_key):
        self.channel_id = channel_id
        self.api_key = api_key


    def get_authorization(self):
        authorization_file = './authorization.txt'
        authorization_dict = {}

        with open(authorization_file, 'w+') as f:
            if len(f.readlines()) != 0:
                f.seek(0)
                authorization_dict = json.load(f)
            f.close()
        if (len(authorization_dict) == 0) or ((len(authorization_dict) > 0) and (authorization_dict['expires_time'] < time.time())):
            url = 'https://accounts.google.com/o/oauth2/iframerpc?action=issueToken&response_type=token&login_hint=AJDLj6KgV9kdAd77_xP7rgZrlfgtRsMzUCYtWNP_GEe92U4cXyANvheUfzLs1QJ_MlFS57aZkDztLv5PtK7PvwI97itrMFmJDrz0xQ02LYE1Nus2rMY7EgAy4cRYhCo5Yq5gY0x6iynQ&client_id=292824132082.apps.googleusercontent.com&origin=https%3A%2F%2Fexplorer.apis.google.com&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.readonly&ss_domain=https%3A%2F%2Fexplorer.apis.google.com&include_granted_scopes=false'
            headers = [
                'cookie: SMSV=ADHTe-DEhuda2ixl64a7vzmQdP8ClN4g7tkwNPijHdc2p0s2fvFkk-wp_ihE_FXu1IlhXsp54LOiSB25oLLXcgYQyB1GZkJTPtOBMOZwnjM3xZryusAoOQE; CONSENT=YES+HK.zh-CN+201905; ACCOUNT_CHOOSER=AFx_qI56srSJnCNUkMX5cJA22EYdYH_fAeI1qIu01nq23CCUJi72vS5Aj3queSeXXCnLZqi2Mpg2liFQk87ZCZ9TJ4X3WU-ielEyNoCabFeUpd7HvvDRxSWF3gHBMDvGJhARpDwhmRiGLAylQZHtJs79m3mWV7yI31h3IWKpvqq9Zq_4eZ8-_Lx3C1ZqQH-wsZnPDuvIIE0MRv-_jkvLEFUzb9WYQFpBAb26gU957iNEWPjgEXAFgv-CF-YT7F_AkYtZH69lrtmPznb4ULI_AkK_dCj1F-NhcCfde_0GrepgEaPO6MJrsT9Tav-E5lYueZhvZj7wjFggCYdlD2qs1xtxouqGggtzxEWeqUgOICOS4gWwshjkEIMiTteQ901Wm4yN7YBOk07uEsYUfzzLkBkF4MCX8ZPOIMMITDy5XMy46SEwwRLUyfIyWjSU9MjnQLbicnW_mNlZ; SID=nAcX7y2ndjx_Z8w-e0qO_Ix-ykDqhFhbU2WjnsYuX-e9p5AssujaOMO6tiwHHiztYjy1Hg.; LSID=CPanel|adsense|doritos|lso|o.console.cloud.google.com|o.console.developers.google.com|o.mail.google.com|o.myaccount.google.com|o.takeout.google.com|s.HK|s.youtube|sitemaps|ss|wise:nAcX7xVP6QPv2MJlBdseMipo8jjoUirfV2-P_rclumrhdEm2lgizNM37w3xcQXIAes8lvA.; HSID=AX8sdhqxM95h7ooz7; SSID=AiOcuXiPPq0Q6-xTq; APISID=E6D4VVrWkGnfnTys/AXf3ePYG8XECc6pdZ; SAPISID=1Ugl32n8sARZChz3/AwMCV5nqiwkS4vOzz; ANID=AHWqTUkOThDB87Ck0_bEZk-NKcQNDFWELh-5uZuHclUrJAkJA1AYupw-6I0Q_BrJ; SEARCH_SAMESITE=CgQIzo0B; NID=188=WaqbX129GEkZZJV-1B8WvmM2_Ma3M2z3byE4uwsTHkBXAaxPoKzI1fxNjxAw2xbQRSEj5oKkJ8OfLritOlEqs1E_7qT-J1NtdsTKCwr-l7mOUfb24GIYYdKrltl7S7roLBwVMCgpk1EwsKXGNfv7EnIkpUoVtLzwmQlh9A-ydXdHt17AbG3ju0v_rD2kmEiTir-H8a1RbmEijQFh6pIdkcRRUcAOPkR6Qvh_CHMwa-bakBfq_C3nHbEOb75zeSPbz1M73QBZCcwIl28Ajq5cy6rYHv2FfGlRpG-4oVsi3MD3KkPab8LvLv63SSHxpEbZhhFN8W9fmdp7-e3mDeYELYlmOVBkmeO9K8OysesHHiEaYgjnD0N8-lRyuaYD94EOVnDhaXVyqXvZ1MGxY3aQRKWwzQPBhKFyaOyaTQf27UXNKQ; 1P_JAR=2019-8-19-5; OCAK=WVY_5eaA8nHIq2rV3wsy6ziawXi_iaQgoWAx2N-vTn8; user_id=115823145306655450326; GAPS=1:ZzBOVAbfjRkrbsjwrxTkE8uHkTxj-VjMwsnjmXVEXAatarKJmFSX0Yv-cgklHYvkuTPTHtsoutZFvH0oT29lFwBzSSWuKOHFIsav1wDgNGSDyuCzVXTk44DjubMLsA:_rL2pGOiGWoYhmlN; LSOLH=EwyYh5XzVvwZYDgTgHYcB0sGkkiEyhY:26103200:305c; SIDCC=AN0-TYu-6h9pd6bJ5AHsmYcZ0e09fTDnT-1IuJorTLm451Bl2e0G7PKd9eU4LiL1Ey_bchYYv0g8',
                'dnt: 1',
                'accept-encoding: gzip, deflate, br',
                'accept-language: zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6,zh-HK;q=0.5,zh-TW;q=0.4',
                'x-chrome-id-consistency-request: version=1,client_id=77185425430.apps.googleusercontent.com,device_id=6dfd46ef-d49b-4fec-ac2a-73e278f460c2,sync_account_id=115823145306655450326,signin_mode=all_accounts,signout_mode=show_confirmation',
                'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
                'accept: */*',
                'referer: https://accounts.google.com/o/oauth2/iframe',
                'authority: accounts.google.com',
                'x-requested-with: XMLHttpRequest',
                'x-chrome-connected: mode=0,enable_account_consistency=false'
                'x-client-data: CIi2yQEIorbJAQipncoBCKijygEIsafKAQjiqMoBCPGpygEIzK7KAQ==',
            ]

            buffer = BytesIO()
            c = pycurl.Curl()
            c.setopt(c.URL, url)
            c.setopt(c.HTTPHEADER, headers)
            c.setopt(c.WRITEDATA, buffer)
            c.setopt(c.SSL_VERIFYPEER, 0)
            c.setopt(c.SSL_VERIFYHOST, 0)
            c.setopt(pycurl.ENCODING, 'gzip,deflate,br')
            c.perform()
            c.close()

            res_str = buffer.getvalue()
            res_dict = json.loads(res_str)
            if res_dict.get('access_token'):
                with open(authorization_file, "w") as f:
                    new_dict = {'access_token': res_dict.get('access_token'), 'expires_time': time.time() + res_dict.get('expires_in')}
                    json.dump(new_dict, f)
                    return res_dict.get('access_token')
            else:
                print(res_str)
                logging.error(res_str)
                exit(1)
        else:
            return authorization_dict['access_token']

    def search_list(self, authorization, next_page_token=None):
        url = "https://studio.youtube.com/youtubei/v1/creator/list_creator_videos?alt=json&key=" + self.channel_id
        url += "&maxResults=50&type=video&key=" + self.api_key
        if next_page_token is not None:
            url += '&pageToken=' + next_page_token
        headers = [
            'x-goog-encode-response-if-executable: base64',
            'accept-encoding: gzip, deflate, br',
            'x-origin: https://explorer.apis.google.com',
            'accept-language: zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6,zh-HK;q=0.5,zh-TW;q=0.4',
            'Authorization: ' + authorization,
            'x-requested-with: XMLHttpRequest',
            'x-client-data: CIi2yQEIorbJAQipncoBCKijygEIsafKAQjiqMoBCPGpygEIzK7KAQ==',
            'x-clientdetails: appVersion=5.0%20(X11%3B%20Linux%20x86_64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F73.0.3683.86%20Safari%2F537.36&platform=Linux%20x86_64&userAgent=Mozilla%2F5.0%20(X11%3B%20Linux%20x86_64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F73.0.3683.86%20Safari%2F537.36',
            'accept: */*',
            'referer: https://content.googleapis.com/static/proxy.html?usegapi=1&jsh=m%3B%2F_%2Fscs%2Fapps-static%2F_%2Fjs%2Fk%3Doz.gapi.zh_CN.ZwogFsKUz94.O%2Fam%3DwQE%2Fd%3D1%2Frs%3DAGLTcCMPx2FK7jpZcj3OzgpFLJQznoXsJA%2Fm%3D__features__',
            'authority: content.googleapis.com',
            'if-none-match: "0UM_wBUsFuT6ekiIlwaHvyqc80M/5F_YP4llDbYwQsbUKZRVy4AN45s"',
            'x-javascript-user-agent: apix/3.0.0 google-api-javascript-client/1.1.0',
            'x-referer: https://explorer.apis.google.com',
            'dnt: 1',
            'Accept:application/json',
        ]

        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.HTTPHEADER, headers)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.SSL_VERIFYPEER, 0)
        c.setopt(c.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.ENCODING, 'gzip,deflate,br')  # 处理gzip内容
        c.perform()
        c.close()

        body = buffer.getvalue().decode('UTF-8')
        return body

    def list_creator_videos(self, authorization, cookie, next_page_token=None):
        post_data = '{"filter":{"and":{"operands":[{"channelIdIs":{"value":"UCAEDC_Ku-K6zTVpGi6kLS1g"}},{"videoOriginIs":{"value":"VIDEO_ORIGIN_UPLOAD"}}]}},"order":"VIDEO_ORDER_DISPLAY_TIME_DESC","pageSize":50,"mask":{"channelId":true,"videoId":true,"lengthSeconds":true,"premiere":{"all":true},"status":true,"thumbnailDetails":{"all":true},"title":true,"draftStatus":true,"downloadUrl":true,"watchUrl":true,"permissions":{"all":true},"timeCreatedSeconds":true,"timePublishedSeconds":true,"origin":true,"livestream":{"all":true},"privacy":true,"metrics":{"all":true},"responseStatus":{"all":true},"description":true,"statusDetails":{"all":true},"scheduledPublishingDetails":{"all":true},"claimDetails":{"all":true},"sponsorsOnly":{"all":true},"unlistedExpired":true,"monetizationDetails":{"all":true},"selfCertification":{"all":true},"ageRestriction":true},"context":{"client":{"clientName":62,"clientVersion":"1.20190820.0.0","hl":"zh-CN","gl":"HK","experimentIds":[]},"request":{"returnLogEntry":true,"internalExperimentFlags":[{"key":"capping_comment_replies","value":"false"},{"key":"restudio_hagrid","value":"false"},{"key":"retry_web_logging_batches","value":"true"},{"key":"enable_live_premieres_creation","value":"true"},{"key":"enable_client_streamz_web","value":"true"},{"key":"restudio_web_canary","value":"false"},{"key":"restudio_disable_hash","value":"true"},{"key":"fill_submit_endpoint_on_preview_web","value":"true"},{"key":"highlight_clip_creation_ftue_display_option","value":"0"},{"key":"analytics_deep_dive_view","value":"true"},{"key":"restudio_comments","value":"true"},{"key":"enable_live_studio_ux","value":"true"},{"key":"log_window_onerror_fraction","value":"1"},{"key":"is_browser_support_for_webcam_streaming","value":"true"},{"key":"enable_lcr_v1_features","value":"false"},{"key":"live_chat_show_settings_in_creator_studio","value":"true"},{"key":"add_creator_entities_to_accounts_list","value":"true"},{"key":"html5_force_debug_data_for_client_tmp_logs","value":"false"},{"key":"restudio_banners","value":"true"},{"key":"json_serialize_shut_off2","value":"false"},{"key":"web_logging_max_batch","value":"100"},{"key":"show_livechat_creator_tooltips","value":"false"},{"key":"json_serialize_service_endpoints2","value":"true"},{"key":"enable_ve_tracker_key","value":"false"},{"key":"ignore_empty_xhr","value":"true"},{"key":"log_sequence_info_on_gel_web","value":"false"},{"key":"is_browser_supported_for_chromecast_streaming","value":"false"},{"key":"enable_lcr_account_menu","value":"false"},{"key":"restudio_nav_refresh","value":"true"},{"key":"video_level_fundraiser_create","value":"false"},{"key":"flush_onbeforeunload","value":"true"},{"key":"web_gel_debounce_ms","value":"10000"},{"key":"web_system_health_fraction","value":"1"},{"key":"custom_csi_timeline_use_gel","value":"false"},{"key":"restudio_web_canary_holdback","value":"false"},{"key":"restudio_scheduled_publishing","value":"true"},{"key":"analytics_headlines_holdback_state","value":"1"},{"key":"upload_copy_file","value":"false"},{"key":"channel_fluctuation_decline_experiment","value":"0"},{"key":"live_chat_continuation_expiration_usec","value":"300000000"},{"key":"force_route_delete_playlist_to_outertube","value":"false"},{"key":"update_super_chat_moderation","value":"false"},{"key":"enable_lcr_improved_preview","value":"false"},{"key":"enable_midroll_ad_insertion","value":"true"},{"key":"deep_dive_discoverability","value":"0"},{"key":"restudio_hats","value":"true"},{"key":"enable_creator_comment_filters","value":"false"},{"key":"live_chat_invite_only_mode_creator_ui","value":"false"},{"key":"yta_see_more_link","value":"true"},{"key":"live_chat_unicode_emoji_json_url","value":"https://www.gstatic.com/youtube/img/emojis/emojis-svg-1.json"},{"key":"content_owner_delegation","value":"false"},{"key":"log_js_exceptions_fraction","value":"1"},{"key":"analytics_snowball","value":"false"},{"key":"html5_load_ads_control_flow","value":"false"},{"key":"enable_polymer_resin","value":"false"},{"key":"restudio_upload_link","value":"true"},{"key":"html5_disable_client_tmp_logs","value":"false"},{"key":"enable_live_studio_url","value":"true"},{"key":"console_log_js_exceptions","value":"true"},{"key":"restudio_onboarding","value":"true"},{"key":"restudio_thumbnails","value":"false"},{"key":"enable_mobile_crosswalk_selection","value":"false"},{"key":"matterhorn_v1_study","value":"0"},{"key":"restudio","value":"false"}]},"user":{"onBehalfOfUser":"103906469025013614191"}}}'
        if next_page_token is not None:
            post_data_dict = json.loads(post_data)
            post_data_dict['pageToken'] = next_page_token
            post_data = json.dumps(post_data_dict)
        url = "https://studio.youtube.com/youtubei/v1/creator/list_creator_videos?alt=json&key=AIzaSyBUPetSUmoZL-OhlxA7wSac5XinrygCqMo"
        headers = [
            'cookie: ' + cookie,
            'origin: https://studio.youtube.com',
            'accept-encoding: gzip, deflate, br',
            'x-origin: https://studio.youtube.com',
            'accept-language: zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6,zh-HK;q=0.5,zh-TW;q=0.4',
            'authorization: ' + authorization,
            'x-youtube-utc-offset: 480',
            'x-client-data: CK21yQEIhLbJAQiktskBCMG2yQEI0bfJAQiJksoBCKmdygEIqKPKAQi5pcoBCLGnygEI4qjKAQjxqcoBCJetygEIza3KAQjIsMoB',
            'x-goog-authuser: 0',
            'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'content-type: application/json',
            'accept: */*',
            'referer: https://studio.youtube.com/channel/UCAEDC_Ku-K6zTVpGi6kLS1g/videos/upload?filter=%5B%5D&sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D',
            'x-youtube-client-name: 62',
            'authority: studio.youtube.com',
            'x-youtube-client-version: 1.20190820.0.0',
            'dnt: 1',
            'x-goog-visitor-id: CgtpZEVpZFA2Wk8wdyigw_jqBQ%3D%3D',
        ]

        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.HTTPHEADER, headers)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.SSL_VERIFYPEER, 0)
        c.setopt(c.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.ENCODING, 'gzip,deflate,br')  # 处理gzip内容
        c.setopt(pycurl.POSTFIELDS, post_data)
        c.perform()
        c.close()

        body = buffer.getvalue().decode('UTF-8')
        return body

    def playlists_list(self, authorization, next_page_token):
        url = "https://content.googleapis.com/youtube/v3/playlists?channelId=" + self.channel_id
        url += "&maxResults=50&part=snippet%2CcontentDetails&key=" + self.api_key
        if next_page_token is not None:
            url += '&pageToken=' + next_page_token

        headers = [
            'Authorization: ' + authorization,
            'dnt: 1',
            'referer: https://content.googleapis.com/static/proxy.html?usegapi=1&jsh=m%3B%2F_%2Fscs%2Fapps-static%2F_%2Fjs%2Fk%3Doz.gapi.zh_CN.ZwogFsKUz94.O%2Fam%3DwQE%2Fd%3D1%2Frs%3DAGLTcCMPx2FK7jpZcj3OzgpFLJQznoXsJA%2Fm%3D__features__',
            'Sec-Fetch-Mode: cors',
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'X-ClientDetails: appVersion=5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F76.0.3809.100%20Safari%2F537.36&platform=Win32&userAgent=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F76.0.3809.100%20Safari%2F537.36',
            'x-goog-encode-response-if-executable: base64',
            'x-javascript-user-agent: apix/3.0.0 google-api-javascript-client/1.1.0',
            'x-origin: https://explorer.apis.google.com',
            'x-referer: https://explorer.apis.google.com',
            'X-Requested-With: XMLHttpRequest',
            'accept-encoding: gzip, deflate, br',
        ]
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.HTTPHEADER, headers)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.SSL_VERIFYPEER, 0)
        c.setopt(c.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.ENCODING, 'gzip,deflate,br')  # 处理gzip内容
        c.perform()
        c.close()

        body = buffer.getvalue()
        return body

    def playlists_insert(self, authorization, data):
        'https://content.googleapis.com/youtube/v3/playlists?part=snippet%2Cstatus&alt=json&key=AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM'
        url = "https://content.googleapis.com/youtube/v3/playlists?part=snippet%2Cstatus&alt=json&key=" + self.api_key
        headers = [
            'Authorization: ' + authorization,
            'dnt: 1',
            'referer: https://content.googleapis.com/static/proxy.html?usegapi=1&jsh=m%3B%2F_%2Fscs%2Fapps-static%2F_%2Fjs%2Fk%3Doz.gapi.zh_CN.ZwogFsKUz94.O%2Fam%3DwQE%2Fd%3D1%2Frs%3DAGLTcCMPx2FK7jpZcj3OzgpFLJQznoXsJA%2Fm%3D__features__',
            'Sec-Fetch-Mode: cors',
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'X-ClientDetails: appVersion=5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F76.0.3809.100%20Safari%2F537.36&platform=Win32&userAgent=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F76.0.3809.100%20Safari%2F537.36',
            'x-goog-encode-response-if-executable: base64',
            'x-javascript-user-agent: apix/3.0.0 google-api-javascript-client/1.1.0',
            'x-origin: https://explorer.apis.google.com',
            'x-referer: https://explorer.apis.google.com',
            'X-Requested-With: XMLHttpRequest',
            'accept-encoding: gzip, deflate, br',
            'Content-Type: application/json',
        ]
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.HTTPHEADER, headers)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.SSL_VERIFYPEER, 0)
        c.setopt(c.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.ENCODING, 'gzip,deflate,br')  # 处理gzip内容
        c.setopt(c.POSTFIELDS, data)
        c.perform()
        c.close()

        body = buffer.getvalue()
        return body

    def playlists_create(self, data):
        url = "https://www.youtube.com/playlist_ajax?action_create_playlist=1"
        headers = [
            'origin: https://www.youtube.com',
            'accept-language: zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6,zh-HK;q=0.5,zh-TW;q=0.4',
            'x-youtube-page-label: youtube.ytfe.desktop_20190829_5_RC1',
            'x-youtube-page-cl: 266331450',
            'x-youtube-utc-offset: 480',
            'cookie: VISITOR_INFO1_LIVE=agupQC2ljlo; PREF=f1=50000000&al=zh-CN&f5=30; CONSENT=YES+HK.zh-CN+201905; LOGIN_INFO=AFmmF2swRgIhAIGYkZTnIhgFG-vyu8NN9MQUOYfbGnqRDW06Sy4ip0ugAiEA0kmFKKB1Tci9Dw24eXNsCI91WqpDogbRlIEcnZs_0yU:QUQ3MjNmd1BIanNpOEFLSzE0RmRNRTRlSWQ3aWFmOTMtLTk3VmJPNmlVbEJhb3pBa2F3c3NMd1VSMzVoRkxIc0lYZVlSbC1yb3RSbml3UjJ3WHMtTE0yczNuUXdMcmEwUm0ya1p4NlZHX0hYano4N1VzOUx3bmFOZ0VCeWxzUURxNWZPd1M0LTFCbllFV2FoN1pIeEhJMndBbjFLNDdxMndpR0tWdVhGbXBsWlJRU2I4Q1Q2Y2diMTducTZqdnlDeDJ6NEtSZkFnaEtjSzd1Zk9OSUdQLTJWY1BDN0NDeG5GY0IwbUJMZ1hQM0RIR2o0dTVBdGpCMA==; _ga=GA1.2.407811703.1566026452; endscreen-metadata-editor-gh=true; YSC=f3iEIrj7rJw; SID=nQcX7568RmCMv8E2J28bkGG2ozM0_apMwzAlCne9BL75S5h7rt8CtU23Q-UC_KWTtVfiHQ.; HSID=AKCRG5uz3iGSeGrZL; SSID=A7ZqbdupwLEp0tqJ9; APISID=KbBJa3MRg6SHmNXT/AT9-pcrQ7Sczh9XN3; SAPISID=AZdnbvdQiZ5rz_R2/AwvamY0YodklyiC2H; SIDCC=AN0-TYtVX8TzJN_TGiMgicBeJ2tRfuW-kOn1vhMhH0BCdsvHCaMLB14Ml3Y2VdJGkwFjIXJwido',
            'x-client-data: CIi2yQEIorbJAQipncoBCKijygEIsafKAQjiqMoBCPGpygEIzK7KAQ==',
            'x-youtube-ad-signals: dt=1567228023059&flash=0&frm&u_tz=480&u_his=2&u_java&u_h=1080&u_w=1920&u_ah=1018&u_aw=1920&u_cd=24&u_nplug=3&u_nmime=4&bc=31&bih=463&biw=1905&brdim=0%2C28%2C0%2C28%2C1920%2C28%2C1920%2C1018%2C1920%2C463&vis=1&wgl=true&ca_type=image','x-youtube-client-version: 1.20190830.05.01',
            'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'x-youtube-variants-checksum: 6091c57142724e61618580050c698edd',
            'content-type: application/x-www-form-urlencoded',
            'accept: */*',
            'referer: https://www.youtube.com/view_all_playlists?nv=1',
            'x-youtube-client-name: 1',
            'authority: www.youtube.com',
            'x-youtube-identity-token: QUFFLUhqbld6VjhQM3BlaFdCZUZGUXk3dldTQXhBTE9EQXw=',
            'dnt: 1',
        ]
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.HTTPHEADER, headers)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.SSL_VERIFYPEER, 0)
        c.setopt(c.SSL_VERIFYHOST, 0)
        c.setopt(c.POSTFIELDS, urllib.parse.urlencode(data))
        c.perform()
        c.close()

        body = buffer.getvalue()
        return body

    def set_playlist_description(self, data):
        url = 'https://www.youtube.com/playlist_edit_service_ajax?action_set_playlist_description=1'
        headers = [
            'origin: https://www.youtube.com',
            'accept-language: zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6,zh-HK;q=0.5,zh-TW;q=0.4',
            'x-youtube-page-label: youtube.ytfe.desktop_20190829_5_RC1',
            'x-youtube-page-cl: 266331450',
            'x-youtube-utc-offset: 480',
            'cookie: VISITOR_INFO1_LIVE=agupQC2ljlo; PREF=f1=50000000&al=zh-CN&f5=30; CONSENT=YES+HK.zh-CN+201905; LOGIN_INFO=AFmmF2swRgIhAIGYkZTnIhgFG-vyu8NN9MQUOYfbGnqRDW06Sy4ip0ugAiEA0kmFKKB1Tci9Dw24eXNsCI91WqpDogbRlIEcnZs_0yU:QUQ3MjNmd1BIanNpOEFLSzE0RmRNRTRlSWQ3aWFmOTMtLTk3VmJPNmlVbEJhb3pBa2F3c3NMd1VSMzVoRkxIc0lYZVlSbC1yb3RSbml3UjJ3WHMtTE0yczNuUXdMcmEwUm0ya1p4NlZHX0hYano4N1VzOUx3bmFOZ0VCeWxzUURxNWZPd1M0LTFCbllFV2FoN1pIeEhJMndBbjFLNDdxMndpR0tWdVhGbXBsWlJRU2I4Q1Q2Y2diMTducTZqdnlDeDJ6NEtSZkFnaEtjSzd1Zk9OSUdQLTJWY1BDN0NDeG5GY0IwbUJMZ1hQM0RIR2o0dTVBdGpCMA==; _ga=GA1.2.407811703.1566026452; endscreen-metadata-editor-gh=true; YSC=f3iEIrj7rJw; SID=nQcX7568RmCMv8E2J28bkGG2ozM0_apMwzAlCne9BL75S5h7rt8CtU23Q-UC_KWTtVfiHQ.; HSID=AKCRG5uz3iGSeGrZL; SSID=A7ZqbdupwLEp0tqJ9; APISID=KbBJa3MRg6SHmNXT/AT9-pcrQ7Sczh9XN3; SAPISID=AZdnbvdQiZ5rz_R2/AwvamY0YodklyiC2H; SIDCC=AN0-TYtw55DnzFOdsSxHVnQKB3IuOl-gukLG2bzisgzvD8Nlv4Mh1j5u4KUTyw-G8ZflfLpTENE',
            'x-client-data: CIi2yQEIorbJAQipncoBCKijygEIsafKAQjiqMoBCPGpygEIzK7KAQ==',
            'x-youtube-ad-signals: dt=1567236871787&flash=0&frm&u_tz=480&u_his=2&u_java&u_h=1080&u_w=1920&u_ah=1018&u_aw=1920&u_cd=24&u_nplug=3&u_nmime=4&bc=31&bih=673&biw=1905&brdim=0%2C28%2C0%2C28%2C1920%2C28%2C1920%2C1018%2C1920%2C673&vis=1&wgl=true&ca_type=image&bid=ANyPxKrLhRQiNDOfE3CCFV2DJk8UWlmuGCSN4M_pl3mx7n_RbmWVqlxEFNRL4I82ULdgiO2yIV84KCwwGJ4sSUOPcW71x8EnUA','x-youtube-client-version: 1.20190830.05.01',
            'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'x-youtube-variants-checksum: 6091c57142724e61618580050c698edd',
            'content-type: application/x-www-form-urlencoded',
            'accept: */*',
            'referer: https://www.youtube.com/playlist?list=PLljKjXpjNpgescmJPq-dgZACD2k5DY6F9&disable_polymer=true',
            'x-youtube-client-name: 1',
            'authority: www.youtube.com',
            'x-youtube-identity-token: QUFFLUhqbld6VjhQM3BlaFdCZUZGUXk3dldTQXhBTE9EQXw=',
            'dnt: 1',
        ]
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.HTTPHEADER, headers)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.SSL_VERIFYPEER, 0)
        c.setopt(c.SSL_VERIFYHOST, 0)
        c.setopt(c.POSTFIELDS, urllib.parse.urlencode(data))
        c.perform()
        c.close()

        body = buffer.getvalue()
        return body

    def playlists_update(self, authorization, data):
        url = "https://content.googleapis.com/youtube/v3/playlists?part=snippet%2Cstatus&alt=json&key=" + self.api_key
        headers = [
            'Authorization: ' + authorization,
            'dnt: 1',
            'referer: https://content.googleapis.com/static/proxy.html?usegapi=1&jsh=m%3B%2F_%2Fscs%2Fapps-static%2F_%2Fjs%2Fk%3Doz.gapi.zh_CN.ZwogFsKUz94.O%2Fam%3DwQE%2Fd%3D1%2Frs%3DAGLTcCMPx2FK7jpZcj3OzgpFLJQznoXsJA%2Fm%3D__features__',
            'Sec-Fetch-Mode: cors',
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'X-ClientDetails: appVersion=5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F76.0.3809.100%20Safari%2F537.36&platform=Win32&userAgent=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F76.0.3809.100%20Safari%2F537.36',
            'x-goog-encode-response-if-executable: base64',
            'x-javascript-user-agent: apix/3.0.0 google-api-javascript-client/1.1.0',
            'x-origin: https://explorer.apis.google.com',
            'x-referer: https://explorer.apis.google.com',
            'X-Requested-With: XMLHttpRequest',
            'accept-encoding: gzip, deflate, br',
        ]
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.HTTPHEADER, headers)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.SSL_VERIFYPEER, 0)
        c.setopt(c.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.ENCODING, 'gzip,deflate,br')  # 处理gzip内容
        c.setopt(pycurl.CUSTOMREQUEST, "PUT")
        c.setopt(c.POSTFIELDS, urllib.parse.urlencode(data))
        c.perform()
        c.close()

        body = buffer.getvalue()
        return body

    def playlists_items_list(self, authorization, playlist_id, next_page_token):
        url = "https://content.googleapis.com/youtube/v3/playlistItems?maxResults=50&part=snippet%2CcontentDetails&playlistId=" + playlist_id + "&key=" + self.api_key
        if next_page_token is not None:
            url += '&pageToken=' + next_page_token
        headers = [
            'Authorization: ' + authorization,
            'dnt: 1',
            'referer: https://content.googleapis.com/static/proxy.html?usegapi=1&jsh=m%3B%2F_%2Fscs%2Fapps-static%2F_%2Fjs%2Fk%3Doz.gapi.zh_CN.ZwogFsKUz94.O%2Fam%3DwQE%2Fd%3D1%2Frs%3DAGLTcCMPx2FK7jpZcj3OzgpFLJQznoXsJA%2Fm%3D__features__',
            'Sec-Fetch-Mode: cors',
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'X-ClientDetails: appVersion=5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F76.0.3809.100%20Safari%2F537.36&platform=Win32&userAgent=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F76.0.3809.100%20Safari%2F537.36',
            'x-goog-encode-response-if-executable: base64',
            'x-javascript-user-agent: apix/3.0.0 google-api-javascript-client/1.1.0',
            'x-origin: https://explorer.apis.google.com',
            'x-referer: https://explorer.apis.google.com',
            'X-Requested-With: XMLHttpRequest',
            'accept-encoding: gzip, deflate, br',
        ]
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.HTTPHEADER, headers)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.SSL_VERIFYPEER, 0)
        c.setopt(c.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.ENCODING, 'gzip,deflate,br')  # 处理gzip内容
        c.perform()
        c.close()

        body = buffer.getvalue()
        return body

    def playlists_items_insert(self, authorization,playlist_id, data):
        url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&key=" + self.api_key
        headers = [
            'Authorization: ' + authorization,
            'dnt: 1',
            'referer: https://content.googleapis.com/static/proxy.html?usegapi=1&jsh=m%3B%2F_%2Fscs%2Fapps-static%2F_%2Fjs%2Fk%3Doz.gapi.zh_CN.ZwogFsKUz94.O%2Fam%3DwQE%2Fd%3D1%2Frs%3DAGLTcCMPx2FK7jpZcj3OzgpFLJQznoXsJA%2Fm%3D__features__',
            'Sec-Fetch-Mode: cors',
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'X-ClientDetails: appVersion=5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F76.0.3809.100%20Safari%2F537.36&platform=Win32&userAgent=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F76.0.3809.100%20Safari%2F537.36',
            'x-goog-encode-response-if-executable: base64',
            'x-javascript-user-agent: apix/3.0.0 google-api-javascript-client/1.1.0',
            'x-origin: https://explorer.apis.google.com',
            'x-referer: https://explorer.apis.google.com',
            'X-Requested-With: XMLHttpRequest',
            'accept-encoding: gzip, deflate, br',
        ]
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.HTTPHEADER, headers)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.SSL_VERIFYPEER, 0)
        c.setopt(c.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.ENCODING, 'gzip,deflate,br')  # 处理gzip内容
        c.setopt(c.POSTFIELDS, urllib.parse.urlencode(data))
        c.perform()
        c.close()

        body = buffer.getvalue()
        return body

    def playlists_items_update(self, authorization, playlist_id, data):
        url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&key=" + self.api_key
        headers = [
            'Authorization: ' + authorization,
            'dnt: 1',
            'referer: https://content.googleapis.com/static/proxy.html?usegapi=1&jsh=m%3B%2F_%2Fscs%2Fapps-static%2F_%2Fjs%2Fk%3Doz.gapi.zh_CN.ZwogFsKUz94.O%2Fam%3DwQE%2Fd%3D1%2Frs%3DAGLTcCMPx2FK7jpZcj3OzgpFLJQznoXsJA%2Fm%3D__features__',
            'Sec-Fetch-Mode: cors',
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'X-ClientDetails: appVersion=5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F76.0.3809.100%20Safari%2F537.36&platform=Win32&userAgent=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F76.0.3809.100%20Safari%2F537.36',
            'x-goog-encode-response-if-executable: base64',
            'x-javascript-user-agent: apix/3.0.0 google-api-javascript-client/1.1.0',
            'x-origin: https://explorer.apis.google.com',
            'x-referer: https://explorer.apis.google.com',
            'X-Requested-With: XMLHttpRequest',
            'accept-encoding: gzip, deflate, br',
        ]
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.HTTPHEADER, headers)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.SSL_VERIFYPEER, 0)
        c.setopt(c.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.ENCODING, 'gzip,deflate,br')  # 处理gzip内容
        c.setopt(c.POSTFIELDS, urllib.parse.urlencode(data))
        c.setopt(pycurl.CUSTOMREQUEST, "PUT")
        c.perform()
        c.close()

        body = buffer.getvalue()
        return body

    def video_description_update(self, data):
        url = 'https://studio.youtube.com/youtubei/v1/video_manager/metadata_update?alt=json&key=AIzaSyBUPetSUmoZL-OhlxA7wSac5XinrygCqMo'
        headers = [
            'cookie: VISITOR_INFO1_LIVE=agupQC2ljlo; PREF=f1=50000000&al=zh-CN&f5=30; CONSENT=YES+HK.zh-CN+201905; LOGIN_INFO=AFmmF2swRgIhAIGYkZTnIhgFG-vyu8NN9MQUOYfbGnqRDW06Sy4ip0ugAiEA0kmFKKB1Tci9Dw24eXNsCI91WqpDogbRlIEcnZs_0yU:QUQ3MjNmd1BIanNpOEFLSzE0RmRNRTRlSWQ3aWFmOTMtLTk3VmJPNmlVbEJhb3pBa2F3c3NMd1VSMzVoRkxIc0lYZVlSbC1yb3RSbml3UjJ3WHMtTE0yczNuUXdMcmEwUm0ya1p4NlZHX0hYano4N1VzOUx3bmFOZ0VCeWxzUURxNWZPd1M0LTFCbllFV2FoN1pIeEhJMndBbjFLNDdxMndpR0tWdVhGbXBsWlJRU2I4Q1Q2Y2diMTducTZqdnlDeDJ6NEtSZkFnaEtjSzd1Zk9OSUdQLTJWY1BDN0NDeG5GY0IwbUJMZ1hQM0RIR2o0dTVBdGpCMA==; _ga=GA1.2.407811703.1566026452; endscreen-metadata-editor-gh=true; YSC=f3iEIrj7rJw; SID=nQcX7568RmCMv8E2J28bkGG2ozM0_apMwzAlCne9BL75S5h7rt8CtU23Q-UC_KWTtVfiHQ.; HSID=AKCRG5uz3iGSeGrZL; SSID=A7ZqbdupwLEp0tqJ9; APISID=KbBJa3MRg6SHmNXT/AT9-pcrQ7Sczh9XN3; SAPISID=AZdnbvdQiZ5rz_R2/AwvamY0YodklyiC2H; SIDCC=AN0-TYsbHEeb739jw92X88iusNEYOAZWSG7WLwmEFCzdlLWPw8QaZs5XmprG3MhXqaMHRgDDSIc',
            'origin: https://studio.youtube.com',
            'x-origin: https://studio.youtube.com',
            'accept-language: zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6,zh-HK;q=0.5,zh-TW;q=0.4',
            'authorization: SAPISIDHASH 1567259214_2279134851f77646f218a48ca37992f5a9e75172',
            'x-youtube-utc-offset: 480',
            'x-client-data: CIi2yQEIorbJAQipncoBCKijygEIsafKAQjiqMoBCPGpygEIzK7KAQ==',
            'x-goog-authuser: 0',
            'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'content-type: application/json',
            'accept: */*',
            'referer: https://studio.youtube.com/video/MR8w6Tpj2JM/edit',
            'x-youtube-client-name: 62',
            'authority: studio.youtube.com',
            'x-youtube-client-version: 1.20190828.0.0',
            'dnt: 1',
            'x-goog-visitor-id: CgthZ3VwUUMybGpsbyjD8qnrBQ%3D%3D',
        ]
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.HTTPHEADER, headers)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.SSL_VERIFYPEER, 0)
        c.setopt(c.SSL_VERIFYHOST, 0)
        c.setopt(c.POSTFIELDS, data)
        c.perform()
        c.close()

        body = buffer.getvalue()
        return body




