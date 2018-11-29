import re
import os
import requests
import csv

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
DIST_DIR = os.path.join(SCRIPT_DIR, '..', 'dist')

default_user_agent = """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"""
generic_user_agents = """
Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3
Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)
Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)
Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1
Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)
Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36
Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1
Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00
Mozilla/5.0 (Linux; U; Android 2.3.4; fr-fr; HTC Desire Build/GRJ22) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1
Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-N920C Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/6.2 Chrome/56.0.2924.87 Mobile Safari/537.36
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 BIDUBrowser/2.x Safari/537.31
Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; GT-I9500 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.0 QQ-URL-Manager Mobile Safari/537.36
Mozilla/5.0 (Android 8.0.0; Tablet; rv:57.0) Gecko/57.0 Firefox/57.0
Mozilla/5.0 (Android 8.1.0; Mobile; rv:61.0) Gecko/61.0 Firefox/61.0
"""


def update_scss_variables():
    url = "https://raw.githubusercontent.com/google/material-design-icons/master/iconfont/codepoints"
    r = requests.get(url)
    r.raise_for_status()
    # df = pandas.read_csv(r.text)
    # print(df)
    csv_f = csv.reader(r.text.splitlines(), delimiter=' ')
    variableFile = open("../src/_variables.scss", "w")
    variableFile.write("$material-icons-codepoints: () !default;\n")
    variableFile.write("$material-icons-codepoints: map-merge((\n")
    for row in csv_f:
        variableFile.write("	\"" + row[0] + "\": " + row[1] + ",\n")
    variableFile.write("), $material-icons-codepoints);")

    # print(r.text)


def download_file(url, file_path):
    r = requests.get(url, headers={"user-agent": default_user_agent})
    r.raise_for_status()
    print(url)
    with open(file_path, 'wb') as f:
        f.write(r.content)


def main():
    user_agents = generic_user_agents.splitlines()
    user_agents = map(lambda x: x, user_agents)

    font_urls = set()

    for user_agent in user_agents:
        url = 'https://fonts.googleapis.com/icon?family=Material+Icons'

        r = requests.get(url, headers={"user-agent": user_agent})
        r.raise_for_status()
        # print(r.text)
        urls = re.findall('url\((.*?)\)', r.text)
        urls = map(str, urls)
        urls = filter(str, urls)
        font_urls.update(urls)

    fonts_map = {font_url.split(
        '.')[-1].lower(): font_url for font_url in font_urls}

    file_name = 'MaterialIcons-Regular'

    for extension, url in fonts_map.items():
        file_path = os.path.join(DIST_DIR, 'fonts', '{file_name}.{extension}'.format(
            file_name=file_name, extension=extension))
        download_file(url, file_path)

    update_scss_variables()


if __name__ == '__main__':
    main()
