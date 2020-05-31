# News_App
A simple news app

# Testing saved articles feature
** Handle with care **

1) Indicates on `/news_api_test` that an article has been saved.
2) User must be authenticated to access the save button on `/<int:title>` (article) page.
3) Currently updates backend using an AJAX payload.
4) We don't have unsave articles, `F` in the github issues chat bois.
5) Still go to `/test` to check out saved articles

# Tag counter for articles viewed by each user

* Tables involved: Tag, User
* Secondary table has been replaced by a relationship class to model tag_count
* Each tag element has access to the list of users using `tag_record.users`
* We can retrieve all the tags associated with a user using `user_record.tags`
* The relationship class holds the tag_count which can be easily retrieved

# Immediate TODOs

* Somehow automate updating the tag_count
