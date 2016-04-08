# Get twitter follower info via API

import csv
import time
from requests_oauthlib import OAuth1Session


def main():
    host = 'https://api.twitter.com'

    # get authentication parameters from local file
    local_file = '/Users/nbrodnax/Indiana/CEWIT/twitter_auth.txt'
    with open(local_file) as txtfile:
        contents = txtfile.readline()
        credentials = eval(contents.strip('\n'))

    # api OAuth 1.0 authentication
    twitter = OAuth1Session(
        credentials.get('consumer_key'),
        client_secret=credentials.get('consumer_secret'),
        resource_owner_key=credentials.get('access_token'),
        resource_owner_secret=credentials.get('access_secret')
    )

    # api GET request for user ids of followers
    get_path = '/1.1/followers/ids.json'
    url = host + get_path
    response = twitter.get(url)

    # print(response)
    data = response.json()

    followers = data['ids']

    # api GET request for users
    get_path = '/1.1/users/lookup.json'
    url = host + get_path

    # need to loop through followers to limit requests
    # 100 per call, up to 180 calls per 15 min
    batch_num = (len(followers) // 100)
    i = 0
    row_begin = 0
    row_end = 100
    user_data = []  # to store the user info
    while i <= batch_num:
        print('\nBatch ' + str(i + 1) + ' of ' + str(batch_num + 1))
        # get a batch of 100 users/followers
        if i < batch_num:
            users = followers[row_begin:row_end]
            print('Processing Rows ' + str(row_begin) + '-' + str(row_end-1))
        else:
            users = followers[row_begin:]
            print('Processing Rows ' + str(row_begin) + '-' +
                  str(len(followers)))
        # get user data for the batch from the api
        response = twitter.get(url, params={'user_id': users})
        print('API: ' + str(response))
        # add users to list of all users
        try:
            for user in response.json():  # returns a list of json objects
                user_data.append(user)
        except ValueError:
            print('There was a problem obtaining the data.')
        row_begin += 100
        row_end += 100
        i += 1
        time.sleep(5)
    print('\nTotal followers requested from API: ' + str(len(user_data)))

    # add users/followers to a csv file
    fieldnames = ['screen_name', 'name', 'description', 'location',
                  'friends_count', 'followers_count', 'statuses_count']
    with open('cewit_twitter_followers.csv', 'w', encoding='utf-8',
              errors='ignore') as csvfile:
        counter = 0
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in user_data:
            temp = {}
            for field in fieldnames:
                temp[field] = user.get(field)
            writer.writerow(temp)
            counter += 1
    print('Total followers added to file: ' + str(counter))


if __name__ == '__main__':
    main()
