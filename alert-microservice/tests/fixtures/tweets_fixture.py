# tests/fixtures/tweet_fixtures
import pytest


@pytest.fixture
def sample_tweets_on_same_day():
    return [
        {
            "account_name": "T1 Sydney Trains",
            "date": "2025-10-03",
            "text": ("this is tweet 1 on same day"),
        },
        {
            "account_name": "T1 Sydney Trains",
            "date": "2025-10-03",
            "text": ("this is tweet 2 on same day"),
        },
        {
            "account_name": "T1 Sydney Trains",
            "date": "2025-10-04",
            "text": ("this is tweet on another day"),
        },
    ]


@pytest.fixture
def sample_collated_tweets_on_same_date():
    return [
        {
            "account_name": "T1 Sydney Trains",
            "date": "2025-10-03",
            "master_text": (
                "this is tweet 1 on same dayEOT\nthis is tweet 2 on same day"
            ),
        },
        {
            "account_name": "T1 Sydney Trains",
            "date": "2025-10-04",
            "master_text": ("this is tweet on another day"),
        },
    ]


@pytest.fixture
def sample_parsed_tweet():
    """Expected output after parse_tweets on sample_tweet_raw_response."""
    return [
        {
            "account_name": "T1 Sydney Trains",
            "date": "2026-02-02",
            "master_text": (
                "Allow extra travel time due to an issue with a freight train "
                "at Werrington. \n\nStops may change at short notice and "
                "you may "
                "have to change trains to continue your trip. \n\n Check "
                "transport apps or information screens for service updates. "
                "https://t.co/b5pREumZ9Q"
            ),
        }
    ]


@pytest.fixture
def sample_extracted_tweet():
    return [
        {
            "account_name": "T1 Sydney Trains",
            "date": "2026-02-02",
            "text": (
                "Allow extra travel time due to an issue with a freight train "
                "at Werrington. \n\nStops may change at short notice and "
                "you may "
                "have to change trains to continue your trip. \n\n Check "
                "transport apps or information screens for service updates. "
                "https://t.co/b5pREumZ9Q"
            ),
        }
    ]


@pytest.fixture
def sample_tweet_raw_response():
    return {
        "type": "tweet",
        "id": "2018116021341540824",
        "url": ("https://x.com/T1SydneyTrains/status/2018116021341540824"),
        "twitterUrl": (
            "https://twitter.com/T1SydneyTrains/status/2018116021341540824"
        ),
        "text": (
            "Allow extra travel time due to an issue with a freight train "
            "at Werrington. \n\nStops may change at short notice and you may "
            "have to change trains to continue your trip. \n\n Check "
            "transport apps or information screens for service updates. "
            "https://t.co/b5pREumZ9Q"
        ),
        "source": "Twitter for iPhone",
        "retweetCount": 0,
        "replyCount": 1,
        "likeCount": 0,
        "quoteCount": 0,
        "viewCount": 433,
        "createdAt": "Mon Feb 02 00:15:28 +0000 2026",
        "lang": "en",
        "bookmarkCount": 0,
        "isReply": False,
        "inReplyToId": None,
        "conversationId": "2018116021341540824",
        "displayTextRange": [0, 235],
        "inReplyToUserId": None,
        "inReplyToUsername": None,
        "author": {
            "type": "user",
            "userName": "T1SydneyTrains",
            "url": "https://x.com/T1SydneyTrains",
            "twitterUrl": "https://twitter.com/T1SydneyTrains",
            "id": "2238323790",
            "name": "T1 Sydney Trains",
            "isVerified": False,
            "isBlueVerified": False,
            "verifiedType": None,
            "profilePicture": (
                "https://pbs.twimg.com/profile_images/"
                "934914287864225792/Na6JG-TS_normal.jpg"
            ),
            "coverPicture": (
                "https://pbs.twimg.com/profile_banners/2238323790/1691036025"
            ),
            "description": "",
            "location": "Sydney, New South Wales",
            "followers": 35791,
            "following": 18,
            "status": "",
            "canDm": True,
            "canMediaTag": True,
            "createdAt": "Tue Dec 10 00:04:11 +0000 2013",
            "entities": {"description": {"urls": []}, "url": {}},
            "fastFollowersCount": 0,
            "favouritesCount": 790,
            "hasCustomTimelines": True,
            "isTranslator": False,
            "mediaCount": 13859,
            "statusesCount": 57514,
            "withheldInCountries": [],
            "affiliatesHighlightedLabel": {},
            "possiblySensitive": False,
            "pinnedTweetIds": [],
            "profile_bio": {
                "description": (
                    "Official updates for Sydney Trains North Shore & "
                    "Western Line.\n\nMonitored between 6am and 10pm, "
                    "7 days a week"
                ),
                "entities": {
                    "description": {
                        "hashtags": [],
                        "symbols": [],
                        "urls": [],
                        "user_mentions": [],
                    },
                    "url": {
                        "urls": [
                            {
                                "display_url": "transportnsw.info",
                                "expanded_url": "https://transportnsw.info",
                                "indices": [0, 23],
                                "url": "https://t.co/8XmJlNvvjR",
                            }
                        ]
                    },
                },
            },
            "isAutomated": False,
            "automatedBy": None,
        },
        "extendedEntities": {
            "media": [
                {
                    "display_url": "pic.twitter.com/b5pREumZ9Q",
                    "expanded_url": (
                        "https://twitter.com/T1SydneyTrains/status/"
                        "2018116021341540824/photo/1"
                    ),
                    "ext_media_availability": {"status": "Available"},
                    "features": {
                        "large": {"faces": []},
                        "orig": {"faces": []},
                    },
                    "id_str": "2018116000709828608",
                    "indices": [236, 259],
                    "media_key": "3_2018116000709828608",
                    "media_results": {
                        "id": (
                            "QXBpTWVkaWFSZXN1bHRzOgwAAQoAARwByc9p12AACgACHAHJ1DeWUdgAAA=="
                        ),
                        "result": {
                            "__typename": "ApiMedia",
                            "id": (
                                "QXBpTWVkaWE6DAABCgABHAHJz2nXYAAKAAIcAcnUN5ZR2AAA"
                            ),
                            "media_key": "3_2018116000709828608",
                        },
                    },
                    "media_url_https": (
                        "https://pbs.twimg.com/media/HAHJz2nXYAAVG4M.png"
                    ),
                    "original_info": {
                        "focus_rects": [
                            {"h": 450, "w": 804, "x": 0, "y": 0},
                            {"h": 450, "w": 450, "x": 0, "y": 0},
                            {"h": 450, "w": 395, "x": 0, "y": 0},
                            {"h": 450, "w": 225, "x": 45, "y": 0},
                            {"h": 450, "w": 900, "x": 0, "y": 0},
                        ],
                        "height": 450,
                        "width": 900,
                    },
                    "sizes": {"large": {"h": 450, "w": 900}},
                    "type": "photo",
                    "url": "https://t.co/b5pREumZ9Q",
                }
            ]
        },
        "card": None,
        "place": {},
        "entities": {
            "hashtags": [],
            "symbols": [],
            "timestamps": [],
            "urls": [],
            "user_mentions": [],
        },
        "quoted_tweet": None,
        "retweeted_tweet": None,
        "isLimitedReply": False,
        "article": None,
    }
