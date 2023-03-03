#################################################
#                                               #
#   ItsBlueTiger2's Best YouTube Videos Ranker  #
#   Utilizes scrapetube module by  ...          #
#                                               #
#################################################

import requests
import scrapetube
from colorama import *
import datetime
from itertools import islice
from math import ceil
from json import loads
from time import perf_counter

DEVELOPER_KEY = input("Type your developer key \n").strip()

def videos_id_formatter(sublist_of_50):
    string = ""
    for videoid in sublist_of_50:
        string = string + str(videoid) + ","
    string = string[:len(string)-1]
    return string



def sublists_of_50(videos):
    length_to_split = list()
    # list of length in which we have to split
    number_of_50 = ceil(len(videos) / 50)

    for number in range(number_of_50):
        length_to_split.append(50)

    # Using islice
    Inputt = iter(videos)
    Output = [list(islice(Inputt, elem))
              for elem in length_to_split]

    return Output

def main():

    type = input("What is the type ? \n"
                 "Channel : type 1 \n"
                 "Playlist : type 2 \n")



    if int(type) == 1:  # Channel
        channel = input("What is channel ID ? It should look like this : UCCezIgC97PvUuR4_gbFUs5g\n").strip()
        tic = perf_counter() #Program timer start

        videos = scrapetube.get_channel(channel)
        videos_list = list()

        for video in videos:    # Ajouter toutes les vidéos de la playlist dans une liste
            videos_list.append(video['videoId'])

        videos_list = sublists_of_50(videos_list)
        json_requests = list()

        for sublist_of_50 in videos_list:
            r = requests\
                .get(f"https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet&id={videos_id_formatter(sublist_of_50)}&key={DEVELOPER_KEY}")
            text = r.text
            json_requests.append(loads(text))

        data_dict = dict()

        for json in json_requests:
            for video in json['items']:
                videoID = video['id']

                title = video['snippet']['title']
                upload_date = video['snippet']['publishedAt']
                views = float(video['statistics']['viewCount'])

                data_dict[videoID] = dict()

                data_dict[videoID]['title'] = title
                data_dict[videoID]['upload_date'] = upload_date
                data_dict[videoID]['views'] = views

        for videoID in data_dict:
            date = data_dict[videoID]['upload_date']
            data_dict[videoID]['upload_date'] = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
            upload_date = data_dict[videoID]['upload_date']

            current_date = datetime.datetime.utcnow()
            elapsed_time = current_date - upload_date
            data_dict[videoID]['elapsed_seconds'] = float(elapsed_time.total_seconds())

            data_dict[videoID]['views_per_second'] = \
            data_dict[videoID]['views'] / data_dict[videoID]['elapsed_seconds']
        print(f"{Style.BRIGHT}{Fore.BLACK}{Back.LIGHTWHITE_EX}ItsBlueTiger2's Best YouTube Videos Ranker")

        print(f"{Style.BRIGHT}{Fore.LIGHTYELLOW_EX}{Back.BLACK}\
{'RANKING'} \t\t {Fore.LIGHTMAGENTA_EX}{'VIEWS PER SECOND'} \t\t {Fore.LIGHTCYAN_EX}{'TITLE'} \t\t {Fore.LIGHTRED_EX}{'VIEWS'} \t\t {Fore.LIGHTWHITE_EX}{'UPLOAD DATE'}")


        ordered_dict = dict(sorted(
            data_dict.items(),
            key=lambda item: item[1]['views_per_second'],
            reverse=True))



        for index, videoID in enumerate(ordered_dict, 1):
            title = data_dict[videoID]['title']
            views_per_second = data_dict[videoID]['views_per_second']
            views = data_dict[videoID]['views']
            upload_date = data_dict[videoID]['upload_date']
            print(f"""{Style.BRIGHT}{Fore.LIGHTYELLOW_EX}{Back.BLACK}\
{index} \t\t {Fore.LIGHTMAGENTA_EX}{views_per_second} \t\t {Fore.LIGHTCYAN_EX}{title} \t\t {Fore.LIGHTRED_EX}{views} \t\t {Fore.LIGHTWHITE_EX}{upload_date}""")
        toc = perf_counter() #Program timer stop
        print(Fore.BLACK + Back.LIGHTWHITE_EX + f"Program took {toc - tic:0.1f} seconds to finish.")
























    elif int(type) == 2:  # Playlist
        playlist = \
            input("What is playlist ID ? It should look like this : PLrV16pC7dwvzQn5z-aIbZj9Gtj3njScyq\n") \
                .strip()
        tic = perf_counter()  # Program timer start

        videos = scrapetube.get_playlist(playlist)
        videos_list = list()

        for video in videos:    # Ajouter toutes les vidéos de la playlist dans une liste
            videos_list.append(video['videoId'])

        videos_list = sublists_of_50(videos_list)
        json_requests = list()

        for sublist_of_50 in videos_list:
            r = requests \
                .get(
                f"https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet&id={videos_id_formatter(sublist_of_50)}&key={DEVELOPER_KEY}")
            text = r.text
            json_requests.append(loads(text))

        data_dict = dict()

        for json in json_requests:
            for video in json['items']:
                videoID = video['id']

                title = video['snippet']['title']
                upload_date = video['snippet']['publishedAt']
                views = float(video['statistics']['viewCount'])

                data_dict[videoID] = dict()

                data_dict[videoID]['title'] = title
                data_dict[videoID]['upload_date'] = upload_date
                data_dict[videoID]['views'] = views

        for videoID in data_dict:
            date = data_dict[videoID]['upload_date']
            data_dict[videoID]['upload_date'] = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
            upload_date = data_dict[videoID]['upload_date']

            current_date = datetime.datetime.utcnow()
            elapsed_time = current_date - upload_date
            data_dict[videoID]['elapsed_seconds'] = float(elapsed_time.total_seconds())

            data_dict[videoID]['views_per_second'] = \
                data_dict[videoID]['views'] / data_dict[videoID]['elapsed_seconds']

        print(f"{Style.BRIGHT}{Fore.BLACK}{Back.LIGHTWHITE_EX}ItsBlueTiger2's Best YouTube Videos Ranker")

        print(f"{Style.BRIGHT}{Fore.LIGHTYELLOW_EX}{Back.BLACK}\
{'RANKING'} \t\t {Fore.LIGHTMAGENTA_EX}{'VIEWS PER SECOND'} \t\t {Fore.LIGHTCYAN_EX}{'TITLE'} \t\t {Fore.LIGHTRED_EX}{'VIEWS'} \t\t {Fore.LIGHTWHITE_EX}{'UPLOAD DATE'}")

        ordered_dict = dict(sorted(
            data_dict.items(),
            key=lambda item: item[1]['views_per_second'],
            reverse=True))

        for index, videoID in enumerate(ordered_dict, 1):
            title = data_dict[videoID]['title']
            views_per_second = data_dict[videoID]['views_per_second']
            views = data_dict[videoID]['views']
            upload_date = data_dict[videoID]['upload_date']
            print(f"""{Style.BRIGHT}{Fore.LIGHTYELLOW_EX}{Back.BLACK}\
{index} \t\t {Fore.LIGHTMAGENTA_EX}{views_per_second} \t\t {Fore.LIGHTCYAN_EX}{title} \t\t {Fore.LIGHTRED_EX}{views} \t\t {Fore.LIGHTWHITE_EX}{upload_date}""")
        toc = perf_counter()  # Program timer stop
        print(Fore.BLACK + Back.LIGHTWHITE_EX + f"Program took {toc - tic:0.1f} seconds to finish.")


    else:
        print("You didn't typed 1 or 2.")


if __name__ == "__main__":
    main()