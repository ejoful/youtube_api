#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pycurl
import json
import time
from io import BytesIO
import logging

class YoutubeApi:
    'Youtube api'

    def __init__(self, channel_id, api_key):
        self.base_url = "https://www.googleapis.com/youtube/v3/"
        self.channel_id = channel_id
        self.api_key = api_key
        self.authorization_file = './authorization.txt'


    def get_authorization(self):
        authorization_dict = None

        with open(self.authorization_file, 'r+') as f:
            authorization_dict = json.load(f)
        if (len(authorization_dict) == 0) or ((len(authorization_dict) > 0) and (authorization_dict['expires_time'] < time.time())):
            url = 'https://accounts.google.com/o/oauth2/iframerpc?action=issueToken&response_type=token&login_hint=AJDLj6KgV9kdAd77_xP7rgZrlfgtRsMzUCYtWNP_GEe92U4cXyANvheUfzLs1QJ_MlFS57aZkDztLv5PtK7PvwI97itrMFmJDrz0xQ02LYE1Nus2rMY7EgAy4cRYhCo5Yq5gY0x6iynQ&client_id=292824132082.apps.googleusercontent.com&origin=https%3A%2F%2Fexplorer.apis.google.com&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.force-ssl&ss_domain=https%3A%2F%2Fexplorer.apis.google.com&include_granted_scopes=false'
            headers = [
                'cookie: SMSV=ADHTe-DEhuda2ixl64a7vzmQdP8ClN4g7tkwNPijHdc2p0s2fvFkk-wp_ihE_FXu1IlhXsp54LOiSB25oLLXcgYQyB1GZkJTPtOBMOZwnjM3xZryusAoOQE; CONSENT=YES+HK.zh-CN+201905; ACCOUNT_CHOOSER=AFx_qI56srSJnCNUkMX5cJA22EYdYH_fAeI1qIu01nq23CCUJi72vS5Aj3queSeXXCnLZqi2Mpg2liFQk87ZCZ9TJ4X3WU-ielEyNoCabFeUpd7HvvDRxSWF3gHBMDvGJhARpDwhmRiGLAylQZHtJs79m3mWV7yI31h3IWKpvqq9Zq_4eZ8-_Lx3C1ZqQH-wsZnPDuvIIE0MRv-_jkvLEFUzb9WYQFpBAb26gU957iNEWPjgEXAFgv-CF-YT7F_AkYtZH69lrtmPznb4ULI_AkK_dCj1F-NhcCfde_0GrepgEaPO6MJrsT9Tav-E5lYueZhvZj7wjFggCYdlD2qs1xtxouqGggtzxEWeqUgOICOS4gWwshjkEIMiTteQ901Wm4yN7YBOk07uEsYUfzzLkBkF4MCX8ZPOIMMITDy5XMy46SEwwRLUyfIyWjSU9MjnQLbicnW_mNlZ; SID=nAcX7y2ndjx_Z8w-e0qO_Ix-ykDqhFhbU2WjnsYuX-e9p5AssujaOMO6tiwHHiztYjy1Hg.; LSID=CPanel|adsense|doritos|lso|o.console.cloud.google.com|o.console.developers.google.com|o.mail.google.com|o.myaccount.google.com|o.takeout.google.com|s.HK|s.youtube|sitemaps|ss|wise:nAcX7xVP6QPv2MJlBdseMipo8jjoUirfV2-P_rclumrhdEm2lgizNM37w3xcQXIAes8lvA.; HSID=AX8sdhqxM95h7ooz7; SSID=AiOcuXiPPq0Q6-xTq; APISID=E6D4VVrWkGnfnTys/AXf3ePYG8XECc6pdZ; SAPISID=1Ugl32n8sARZChz3/AwMCV5nqiwkS4vOzz; ANID=AHWqTUkOThDB87Ck0_bEZk-NKcQNDFWELh-5uZuHclUrJAkJA1AYupw-6I0Q_BrJ; OCAK=kAG7G8xhj49Y5YVVqS72s3v2j2ZQyCb2lQqtoBZYAIw; user_id=115823145306655450326; LSOLH=EwyYh5XzVvwZYDgTgHYcB0um_kwCyhY:26100929:62b3; 1P_JAR=2019-08-18-05; SEARCH_SAMESITE=CgQIzo0B; NID=188=a4PzCPDnMDAtaXqEao6nQwlCxAxR4yAvWZI6Ywi3s2tYQSornoU53uxNd5UHaQofiEAokZJp5SzD6PMGQb2_YDF2kWY66PvFO53nAQZPOKZeIVwXOr4TQQMaKNfP4D3aV6Eb76X5YSuLtC9uyIavffhWykb-OiYuAypJQG4A8zIPQjZl1s7wU-KaseAIzKc5yE2sr84VHSOIxNa9VoCIKQpWpKgWm6ahehQTn2mS6yQpgebV-xUWpltI9C0aAq3aKZhsXQAQWAoXMItA6YfHvomzSBvbCki2-Z-se9RsmL9z1JUVbmnS5-9wrnyhtH094b5sMDyQVzvff879c51lyO0-r2zYbRop5JrR_jiXd1sq-ciukPTa9XuKZ0yxxPTZqM5kKsgKDuuJzvQasf4f3-YR5R-1RiduFEC0Y-aaAXzUmA; GAPS=1:B13NFYORUo_XALJu64KSrDa3C5u64vVnTJhb1If392C0mvWCqy1VkUVTqi30flrL3EPlNotduPvdFlKQR08IbkNswUseISGY4hBM2g4mAezgF8shHQvnSVJXS2VqfA:R4PLFt4kdY3pDkyj; SIDCC=AN0-TYtvAz9OvmWpp-q4cKk5i1S6ka5a_UfmKPMEUNHFsv_dov4D-OOpfFWmi0WRrR62YYRL5FQC',
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
                with open(self.authorization_file, "w") as f:
                    new_dict = {'access_token': res_dict.get('access_token'), 'expires_time': time.time() + res_dict.get('expires_in')}
                    json.dump(new_dict, f)
                    return res_dict.get('access_token')
            else:
                print(res_str)
                logging.error(res_str)
                exit(1)
        else:
            return authorization_dict['access_token']

    def search(self):
        url = self.base_url + "search?part=%20snippet&channelId=" + self.channel_id
        url += "&maxResults=50&type=video&key=" + self.api_key
        authorization = self.get_authorization()
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

        body = buffer.getvalue()
        return body

    def update_video(self):
        # TODO
        print('1')

    def playlists(self):
        # TODO
        print('1')

    def playlists_items(self):
        # TODO
        print('1')


    def update_playlist(self):
        # TODO
        print('1')

    def create_playlist(self):
        # TODO
        print('1')

channel_id = "UCAEDC_Ku-K6zTVpGi6kLS1g"
api_key = "AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM"
authorization = "Bearer ya29.GmBoB1eEjIUDNAISKuNXjt4K9Dw7jaj35aRGiSOID68oJ0vMIoZ8TAHrjvUEkBBj_zAByPhLw6VviQaXAjxNGiGeQY3b4aOZSNQCly6as3Ag5qp0XumMjh6z1Zkd89kZP1s"
x = YoutubeApi(channel_id, api_key, authorization)
y = x.search()
print(y)

