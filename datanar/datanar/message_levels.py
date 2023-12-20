from django.contrib.messages import constants as messages

SHORT_LINK = 42
LOADING_LINKS = 43

MESSAGE_TAGS = {
    SHORT_LINK: "short_link",
    LOADING_LINKS: "loading_links",
}

messages.DEFAULT_TAGS.update(MESSAGE_TAGS)
