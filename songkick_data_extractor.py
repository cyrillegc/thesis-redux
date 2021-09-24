import requests
import time
import pickle
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
import os

BASE_URL = 'https://www.songkick.com'
DATA_FOLDER = 'data/'
CRAWL_FOLDER = 'crawl/songkick/'
TESTING = False


def main():
    #get_venues()
    get_venues_from_local_files()


def save_search_pages():
    # save the search result pages locally to html files

    query = 'switzerland'
    query_url = 'https://www.songkick.com/search?per_page=10&query=' + query + '&type=venues&page='
    page_nbr = 1

    error_counter = 0
    folder_path = CRAWL_FOLDER + 'songkick_search_html/'
    base_filename = 'songkick_search_page_'

    while page_nbr < 933:
        time.sleep(1)
        query_page_url = query_url + str(page_nbr)
        response = requests.get(query_page_url)
        filename = folder_path + base_filename + str(page_nbr) + '.html'

        if response.status_code != 200:
            print('error', query_page_url, response.status_code)
            error_counter += 1
            continue

        with open(filename, mode='w', encoding='utf-8') as entry:
            entry.write(response.text)
            print(filename)

        if page_nbr % 10 == 0:
            print('-----------', page_nbr)

        page_nbr += 1


def get_venues_from_local_files():
    # get the list of venues when querying "switzerland"

    folder_path = 'songkick_search_html/'
    resumed_process = False
    resume_page_nbr = 850

    # get concerts data previously crawled
    try:
        concerts_dict = pickle.load(open(CRAWL_FOLDER + 'dump_concerts.p', 'rb'))
        dumped_concerts_count = len(concerts_dict)
        print('Dump found. Concerts:', dumped_concerts_count)
    except FileNotFoundError:
        concerts_dict = dict()
        dumped_concerts_count = 0

    # get venues data previously crawled
    try:
        venues_dict = pickle.load(open(CRAWL_FOLDER + 'dump_venues.p', 'rb'))
        dumped_venues_count = len(venues_dict)
        print('Dump found. Venues:', dumped_venues_count)
    except FileNotFoundError:
        venues_dict = dict()
        dumped_venues_count = 0

    # go through every search results pages stored locally
    for html_page_path in os.listdir(folder_path):
        page_nbr = re.findall(r'[0-9]+', html_page_path)[0]

        if int(page_nbr) != resume_page_nbr and resumed_process is False:
            print(page_nbr)
            continue
        else:
            resumed_process = True

        print('-------------- venues page', page_nbr)

        # open and parse the html file
        with open(folder_path + html_page_path, encoding='utf-8') as page:
            data_html = page.read()
            soup = BeautifulSoup(data_html, 'html.parser')

        no_result = soup.find('div', {'class': 'no-results'})
        if no_result:
            break

        venue_list = soup.find_all('li', {'class': 'venue'})

        for venue in venue_list:
            venue_short_url = venue.a.get('href')
            venue_id = re.findall(r'(?<=\/)[0-9]+(?=-)', venue_short_url)[0]
            venue_idx = '/venues/' + str(venue_id)

            if venue_idx not in venues_dict.keys():
                print(venue_idx)

                # get the metadata from a given venue
                concerts_dict, venues_dict = get_venue_data(
                    concerts_dict, venues_dict, venue_idx,
                )

        current_concerts_count = len(concerts_dict)
        current_venues_count = len(venues_dict)

        if current_concerts_count > dumped_concerts_count and current_venues_count > dumped_venues_count:
            # save temp data
            save_temp_data(concerts_dict, 'concerts')
            save_temp_data(venues_dict, 'venues')
            pickle.dump(concerts_dict, open(CRAWL_FOLDER + 'dump_concerts.p', 'wb'))
            pickle.dump(venues_dict, open(CRAWL_FOLDER + 'dump_venues.p', 'wb'))

        print('After page', str(page_nbr), ': Venues:', current_venues_count, '- Concerts:', current_concerts_count)

    print('XXXXX COMPLETE XXXXX')
    print('Venues:', len(venues_dict))
    print('Concerts:', len(concerts_dict))
    save_data(concerts_dict, 'concerts')
    save_data(venues_dict, 'venues')


def get_venues():
    # get the list of venues when querying "switzerland"

    query = 'switzerland'
    query_url = 'https://www.songkick.com/search?per_page=10&query=' + query + '&type=venues&page='
    page_nbr = 1
    start_time = time.time()

    try:
        concerts_dict = pickle.load(open(CRAWL_FOLDER + 'dump_concerts.p', 'rb'))
        print('Dump found. Concerts:', len(concerts_dict))
    except FileNotFoundError:
        concerts_dict = dict()

    try:
        venues_dict = pickle.load(open(CRAWL_FOLDER + 'dump_venues.p', 'rb'))
        print('Dump found. Venues:', len(venues_dict))
    except FileNotFoundError:
        venues_dict = dict()

    while True:
        print('-------------- venues page', str(page_nbr))

        start_time = sleep_timer(start_time)
        response = requests.get(query_url + str(page_nbr))
        print(query_url + str(page_nbr))

        soup = BeautifulSoup(response.content, 'html.parser')
        no_result = soup.find('div', {'class': 'no-results'})
        if no_result:
            break

        venue_list = soup.find_all('li', {'class': 'venue'})

        for venue in venue_list:
            venue_short_url = venue.a.get('href')
            venue_id = re.findall(r'(?<=\/)[0-9]+(?=-)', venue_short_url)[0]

            # get the metadata from a given venue
            concerts_dict, venues_dict, start_time = get_venue_data(
                concerts_dict, venues_dict, venue_id, start_time,
            )

        # save temp data
        #save_temp_data(concerts_dict, 'concerts')
        save_temp_data(venues_dict, 'venues')
        pickle.dump(concerts_dict, open(CRAWL_FOLDER + 'dump_concerts.p', 'wb'))
        pickle.dump(venues_dict, open(CRAWL_FOLDER + 'dump_venues.p', 'wb'))

        print('After page', str(page_nbr), ': Venues:', len(venues_dict), '- Concerts:', len(concerts_dict))
        page_nbr += 1

        if page_nbr > 2 and TESTING:
            break

    print('XXXXX COMPLETE XXXXX')
    print('Venues:', len(venues_dict))
    print('Concerts:', len(concerts_dict))
    #save_data(concerts_dict, 'concerts')
    save_data(venues_dict, 'venues')


def get_venue_data(concerts_dict, venues_dict, venue_idx):
    # get the metadata from a given venue

    venue_data_dict = dict()
    venue_url = BASE_URL + venue_idx

    start_time = time.time()
    response = requests.get(venue_url)
    print(venue_url)

    soup = BeautifulSoup(response.content, 'html.parser')
    page_scripts = soup.find_all('script', {'type': 'application/ld+json'})

    for page_script in page_scripts:
        venue_metadata = json.loads(page_script.string)[0]
        if venue_metadata['@type'] == 'MusicVenue':
            # check if the venue is in Switzerland
            venue_country = venue_metadata['address']['addressCountry']

            if venue_country == 'Switzerland':
                # get the past concerts at this venue
                concerts_dict, start_time = get_venue_concerts(
                    concerts_dict, venue_idx, start_time)

                # get the data about the venue
                venue_data_dict['venue'] = venue_metadata['name']
                venue_data_dict['locality'] = venue_metadata['address']['addressLocality']
                venue_data_dict['postal_code'] = venue_metadata['address']['postalCode']
                venue_data_dict['street'] = venue_metadata['address']['streetAddress']
                venue_data_dict['country'] = venue_metadata['address']['addressCountry']

                # some venues don't have geo coordinates
                try:
                    venue_data_dict['latitude'] = venue_metadata['geo']['latitude']
                    venue_data_dict['longitude'] = venue_metadata['geo']['longitude']
                except KeyError:
                    venue_data_dict['latitude'] = ''
                    venue_data_dict['longitude'] = ''

                # some venues don't have a website
                try:
                    venue_data_dict['venue_website'] = venue_metadata['sameAs']
                except KeyError:
                    print('venue website error')
                    venue_data_dict['venue_website'] = ''

                venues_dict[venue_idx] = venue_data_dict
            else:
                # display error message if the venue is in another country
                print('Not in Switzerland:', venue_country)

    return concerts_dict, venues_dict


def get_venue_concerts(concerts_dict, venue_idx, start_time):
    # get the past concerts at a given venue

    venue_concerts_url = BASE_URL + venue_idx + '/gigography?page='
    page_nbr = 1
    concerts_count = 0

    while True:
        start_time = sleep_timer(start_time)
        response = requests.get(venue_concerts_url + str(page_nbr))
        print(venue_concerts_url + str(page_nbr))

        # if the response has history, then it's been redirected, meaning it's over the max page number for this venue
        if response.history:
            print(response.history)
            break

        print('....... concerts page', page_nbr)
        soup = BeautifulSoup(response.content, 'html.parser')
        concerts_list = soup.find_all(class_='artists summary')

        for concert in concerts_list:
            concert_short_url = concert.a.get('href')
            concert_url = BASE_URL + concert_short_url
            concert_id = re.findall(r'(?<=\/)[0-9]+(?=-)', concert_short_url)[0]

            # # get data from a given concert in a venue
            concert_data_dict, start_time = get_concert_data(concert_url, venue_idx, start_time)

            # get short url of the concert (only event type and concert id) for Dataframe index
            event_type = concert_data_dict['type']
            concert_idx = '/' + event_type + 's/' + concert_id
            concerts_dict[concert_idx] = concert_data_dict

            concerts_count += 1

            if concerts_count > 0 and TESTING:
                break

        page_nbr += 1

        if page_nbr > 1 and TESTING:
            break

    return concerts_dict, start_time


def get_concert_data(concert_url, venue_idx, start_time):
    # get data from a given concert in a venue

    concert_data_dict = dict()

    start_time = sleep_timer(start_time)
    response = requests.get(concert_url)
    print(concert_url)

    soup = BeautifulSoup(response.content, 'html.parser')
    event_type = soup.find('a', attrs={'data-analytics-page-type': True})['data-analytics-page-type']
    concert_data_dict['type'] = event_type  # event can be festival or concert

    page_scripts = soup.find_all('script', {'type': 'application/ld+json'})
    for page_script in page_scripts:
        concert_metadata = json.loads(page_script.string)[0]
        if concert_metadata['@type'] == 'MusicEvent':
            # name of the concert
            concert_data_dict['name'] = concert_metadata['name']

            # location of the concert
            concert_data_dict['venue'] = concert_metadata['location']['name']
            concert_data_dict['locality'] = concert_metadata['location']['address']['addressLocality']
            concert_data_dict['venue_id'] = venue_idx

            # date of the concert
            concert_data_dict['startDate'] = concert_metadata['startDate'][:10]
            concert_data_dict['endDate'] = concert_metadata['endDate']

            # artists of the concert
            performers_list = concert_metadata['performer']
            performer_count = 1
            for performer in performers_list:
                artist_key = 'artist_' + str(performer_count)
                artist_url_key = 'artist_url_' + str(performer_count)
                concert_data_dict[artist_key] = performer['name']

                # remove useless part in artist url
                artist_url = performer['sameAs']
                artist_url = re.sub(r'\?utm_medium=organic&utm_source=microformat', '', artist_url)
                artist_url = re.sub(r'https:\/\/www\.songkick\.com', '', artist_url)
                concert_data_dict[artist_url_key] = artist_url

                performer_count += 1

    return concert_data_dict, start_time


def sleep_timer(start_time):
    # WARNING: function makes the connection unstable
    # pause the program to have at least 1 sec between each request to www.songkick.com

    # get elapsed time since last request
    elapsed_time = time.time() - start_time
    # if elapsed time is more than 1 sec, do not pause the program
    if elapsed_time > 1:
        sleep_time = 0
    # else, pause the program to get at least 1 sec
    else:
        sleep_time = 1 - elapsed_time

    #time.sleep(sleep_time)  # not using the function due to instability
    time.sleep(1)
    new_start_time = time.time()

    return new_start_time


def save_data(data_dict, name):
    # save complete data

    # convert dict to dataframe
    data_df = pd.DataFrame.from_dict(data_dict, orient='index')
    data_filename = 'data_' + name + '.csv'

    # save to csv file
    data_df.to_csv(data_filename, encoding='utf-8')


def save_temp_data(data_dict, name):
    # save incomplete concerts data during process

    # convert dict to dataframe
    temp_concerts_df = pd.DataFrame.from_dict(data_dict, orient='index')
    csv_filename = CRAWL_FOLDER + 'temp_data_' + name + '.csv'

    temp_concerts_df.to_csv(csv_filename, encoding='utf-8')
    print(csv_filename)


if __name__ == '__main__':
    main()
