CONTENT_OWNER_ID = '1plZnEOEotdurzlq_UkMrQ'
MUSIC_INFO_COLUMNS = ['artist', 'track', 'video_id', 'isrc']
API_YOUTUBE_DATA_KEY = 'AIzaSyBIAiykLEvl_LcarQLctsSqEmKzXsV8Gzc'
TABLE_SCHEMA_THUMBNAIL = [
                {'name': 'artist', 'type': 'STRING'},
                {'name': 'title', 'type': 'STRING'},
                {'name': 'track', 'type': 'STRING'},
                {'name': 'video_id', 'type': 'STRING'},
                {'name': 'thumbnail', 'type': 'STRING'},
                {'name': 'duration', 'type': 'TIME'},
                {'name': 'published_at', 'type': 'STRING'},
                {'name': 'related_video', 'type': 'FLOAT'}]

TABLE_SCHEMA_YT_ANALYTICS = [
                {'name': 'video_id', 'type': 'STRING'},
                {'name': 'channel_id', 'type': 'STRING'},
                {'name': 'date', 'type': 'DATE'},
                {'name': 'traffic_source_type', 'type': 'INTEGER'},
                {'name': 'views', 'type': 'INTEGER'},
                {'name': 'average_view_duration_percentage', 'type': 'FLOAT'}]

NAME2JOB_ID = {'basic': 'f6a0c40e-0fd2-4cc6-8d0d-55e9853f2025',
               'os_device_tf_source': 'e0f0034b-cd6a-4952-ab9d-ddb4bc5d3207',
               'ad_revenue': '98326f28-4273-452e-b44f-330d11526a4b',
               'all_revenue': 'a4220f64-b833-4fd2-b686-495055cff9a3',
               }

PLAYBACK_LOCATION_TYPE = {'0': 'Link or app', '1': 'Website', '2': 'Channel Page', '5': 'Outros', '7': 'Home Page',
                          '8': 'Search', '10': 'Youtube Shorts'}

TRAFFIC_SOURCE_TYPE = {'0': 'Direct or Unknown', '1': 'Advertising', '3': 'History or subscriptions section',
                       '4': 'Channel page', '5': 'Search', '7': 'Related video', '8': 'Others',
                       '9': 'Link external', '11': 'Cards', '14': 'Playlists',
                       '17': 'Notifications', '18': 'List all videos from playlist',
                       '19': 'Content owner used to promote', '20': 'End screen', '23': 'Stories', '24': 'Shorts',
                       '25': 'Product pages', '26': 'Hashtag pages', '27': 'Short sound pages', '28':'Live redirect'}

DEVICE_TYPE = {'100': 'Unknown', '101': 'Computer', '102': 'TV', '103': 'Game Console', '104': 'Cell phone',
               '105': 'Tablet'}

OS = {'1': 'Other', '2': 'Windows', '3': 'Windows Phone', '4': 'Android', '5': 'iOS', '6': 'Symbian', '7': 'Blackberry',
      '9': 'Macintosh', '10': 'Playstation', '11': 'Bada', '12': 'WebOS', '13': 'Linux', '14': 'Hiptop', '15': 'MeeGo',
      '16': 'Wii', '17': 'Xbox', '18': 'Playstation Vita', '19': 'Smart TV', '20': 'Nintendo 3DS', '21': 'Chromecast',
      '22': 'Tizer', '23': 'Firefox', '24': 'RealMedia', '25': 'KaiOS', '26': 'Roku', '27': 'Nintendo Switch',
      '28': 'Apple tvOS', '29': 'Fire OS', '30': 'ChromeOS', '31': 'Vidaa'}

AD_TYPE ={'1': 'Skippable AD', '2': 'Banner AD Right from Video', '3': 'Non-Skippable AD', '5': 'Display AD Fixed CPM',
          '6': 'Non-Skippable AD Fixed CPM', '13': 'Unknown', '15': 'Skippable AD Fixed CPM',
          '19': 'Short AD Non-Skippable', '20': 'Short AD Non-Skippable Fixed CPM'}

TABLE_SCHEMA_REPORT_BASIC = [
                {'name': 'video_id', 'type': 'STRING'},
                {'name': 'date', 'type': 'DATE'},
                {'name': 'subscribed_status', 'type': 'STRING'},
                {'name': 'country_code', 'type': 'STRING'},
                {'name': 'likes', 'type': 'INTEGER'},
                {'name': 'dislikes', 'type': 'INTEGER'},
                {'name': 'comments', 'type': 'INTEGER'},
                {'name': 'shares', 'type': 'INTEGER'},
                {'name': 'subscribed_gained', 'type': 'INTEGER'},
                {'name': 'subscribed_lost', 'type': 'INTEGER'},
                {'name': 'videos_added_to_playlists', 'type': 'INTEGER'},
                {'name': 'videos_removed_from_playlists', 'type': 'INTEGER'}]

TABLE_SCHEMA_REPORT_OS_DEVICE_TF_SOURCE = [
                {'name': 'video_id', 'type': 'STRING'},
                {'name': 'channel_id', 'type': 'STRING'},
                {'name': 'title', 'type': 'STRING'},
                {'name': 'date', 'type': 'DATE'},
                {'name': 'subscribed_status', 'type': 'STRING'},
                {'name': 'live_or_on_demand', 'type': 'STRING'},
                {'name': 'country_code', 'type': 'STRING'},
                {'name': 'playback_location_type', 'type': 'STRING'},
                {'name': 'traffic_source_type', 'type': 'STRING'},
                {'name': 'device_type', 'type': 'STRING'},
                {'name': 'operating_system', 'type': 'STRING'},
                {'name': 'views', 'type': 'INTEGER'},
                {'name': 'red_views', 'type': 'INTEGER'},
                {'name': 'average_view_duration_seconds', 'type': 'FLOAT'},
                {'name': 'red_average_view_duration', 'type': 'FLOAT'}]

TABLE_SCHEMA_REPORT_AD_REVENUE = [
                {'name': 'video_id', 'type': 'STRING'},
                {'name': 'channel_id', 'type': 'STRING'},
                {'name': 'claimed_status', 'type': 'STRING'},
                {'name': 'uploader_type', 'type': 'STRING'},
                {'name': 'date', 'type': 'DATE'},
                {'name': 'country_code', 'type': 'STRING'},
                {'name': 'ad_type', 'type': 'STRING'},
                {'name': 'estimated_youtube_ad_revenue', 'type': 'FLOAT'},
                {'name': 'ad_impressions', 'type': 'INTEGER'},
                {'name': 'estimated_cpm', 'type': 'FLOAT'}]

TABLE_SCHEMA_REPORT_ALL_REVENUE = [
                {'name': 'video_id', 'type': 'STRING'},
                {'name': 'channel_id', 'type': 'STRING'},
                {'name': 'claimed_status', 'type': 'STRING'},
                {'name': 'uploader_type', 'type': 'STRING'},
                {'name': 'date', 'type': 'DATE'},
                {'name': 'country_code', 'type': 'STRING'},
                {'name': 'estimated_partner_revenue', 'type': 'FLOAT'},
                {'name': 'estimated_partner_ad_revenue', 'type': 'FLOAT'},
                {'name': 'estimated_partner_ad_auction_revenue', 'type': 'FLOAT'},
                {'name': 'estimated_partner_ad_reserved_revenue', 'type': 'FLOAT'},
                {'name': 'estimated_youtube_ad_revenue', 'type': 'FLOAT'},
                {'name': 'estimated_monetized_playbacks', 'type': 'INTEGER'},
                {'name': 'estimated_playback_based_cpm', 'type': 'FLOAT'},
                {'name': 'ad_impressions', 'type': 'INTEGER'},
                {'name': 'estimated_cpm', 'type': 'FLOAT'},
                {'name': 'estimated_partner_red_revenue', 'type': 'FLOAT'},
                {'name': 'estimated_partner_transaction_revenue', 'type': 'FLOAT'}]

TABLE_SCHEMA_REPORT = {'basic': TABLE_SCHEMA_REPORT_BASIC,
                        'os_device_tf_source': TABLE_SCHEMA_REPORT_OS_DEVICE_TF_SOURCE,
                        'ad_revenue': TABLE_SCHEMA_REPORT_AD_REVENUE, 'all_revenue': TABLE_SCHEMA_REPORT_ALL_REVENUE}

TOKEN_TELEGRAM = '5393351877:AAGUfRG3WY5sbQcp2aaGB_9Qx2dkXDeJF9o'
CHAT_ID_TELEGRAM = '@onitifications_devs'
