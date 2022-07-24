import requests
import json
import glob
import functools

def getbookmarks():
    url = 'https://twitter.com/i/api/graphql/DtY7ITw1NhpU1CcuOhx41Q/Bookmarks?variables=%7B%22count%22%3A150%2C%22includePromotedContent%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withDownvotePerspective%22%3Atrue%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22__fs_responsive_web_like_by_author_enabled%22%3Afalse%2C%22__fs_dont_mention_me_view_api_enabled%22%3Atrue%2C%22__fs_interactive_text_enabled%22%3Atrue%2C%22__fs_responsive_web_uc_gql_enabled%22%3Afalse%2C%22__fs_responsive_web_edit_tweet_api_enabled%22%3Afalse%7D'

    headers = {
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAA',
        'x-twitter-client-language' : 'fr',
        'x-csrf-token' : '',
        'x-twitter-auth-type' : 'OAuth2Session',
        'x-twitter-active-user' : 'yes',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'content-type' : 'application/json',
        'Accept' : '*/*',
        'Sec-GPC' : '1',
        'host' : 'twitter.com'
    }

    cookies = {
        'auth_token' : '',
        'ct0' : '',
        'd_prefs' : '',
        'des_opt_in' : 'N',
        'dnt' : '1',
        'g_state' : '{"i_p":,"i_l":1}',
        'guest_id' : 'v1%',
        'kdt' : ''
    }

    r = requests.get(url, headers=headers, cookies=cookies)
    print(" - Tentative d'accès à l'url...")
    if r.status_code == 200:
        print(" - Tentative réussie.")
        data = r.json()
        txt = json.dumps(data)
        f = open('JSONBookmarks/signets.json', 'w')
        f.write(txt)
        f.close()
        print(" - Signets sauvegardés avec succès ! ")
    else:
        print("Erreur dans l'accès à l'url")
        exit(1)

getbookmarks()

signets = []
md_file = open("bookmarks.txt", "w+", encoding="utf-8")

files = [file for file in glob.glob("JSONBookmarks/*")]
for file_name in files:
    with open(file_name, encoding="utf-8") as bk:
        data = json.load(bk)
        signets.append(data)

def constructUrl(tweet_id, username):
    return "https://twitter.com/" + str(username) + "/status/" + str(tweet_id)
    #Création du lien du signet

def deep_get(dictionary, keys, default=None):
    return functools.reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)

for data in signets:
    instructions_list = deep_get(data, "data.bookmark_timeline.timeline.instructions")
    tweet_entries_list = deep_get(instructions_list[0], "entries")
    for tweet_entry in tweet_entries_list:
        result = deep_get(tweet_entry, "content.itemContent.tweet_results.result")
        username = deep_get(result, "core.user_results.result.legacy.screen_name")
        text = deep_get(result, "legacy.full_text")
        tweet_id = deep_get(result, "rest_id")
        url = constructUrl(tweet_id, str(username))
        extrait = 'TWEET : ' + str(text).replace('\n', '') + ';;;' + 'AUTEUR : ' + str(username).replace('\n','') + ';;;' + 'URL : ' + url.replace('\n', '') + ';;;\n'
        md_file.write(str(extrait))
    print(" --- Génération du fichier CSV terminée ! --- ")
