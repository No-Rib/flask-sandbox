"""Provides tag driver class to Redis database."""
from collections import defaultdict

from app import redis


class TagsDriver(object):
    __db__ = redis

    __fi_prefix__ = "post"
    __ri_prefix__ = "tag"

    @classmethod
    def _get_fi_key(cls, post_id):
        """Compiles forward index db key based on prefix."""

        return ":".join([cls.__fi_prefix__, str(post_id)])

    @classmethod
    def _get_ri_key(cls, tag):
        """Compiles reverse index db key based on prefix."""

        return ":".join([cls.__ri_prefix__, tag])

    @classmethod
    def set_tags(cls, post_id, tags):
        """Sets tags for post.

        Add tags as value to post record.
        Add post ID as value to tag records
        """

        cls.__db__.delete(cls._get_fi_key(post_id))
        cls.__db__.sadd(cls._get_fi_key(post_id), *tags)

        for tag in tags:
            cls.__db__.sadd(cls._get_ri_key(tag), post_id)

    @classmethod
    def get_posts(cls, tag):
        """Gets IDs of posts, associated with given tag.

        rtype: set"""

        return cls.__db__.smembers(cls._get_ri_key(tag))

    @classmethod
    def get_tags(cls, post_id):
        """Get tags, set on given post.

        rtype: set
        """

        return cls.__db__.smembers(cls._get_fi_key(post_id))

    @classmethod
    def search_posts(cls, tags):
        """Search posts by tags.

        Post that have multiple tags from query are prioritized.

        rvalue: (bool, iterator) --- <has_posts, post_ids>
        """

        result = defaultdict(int)
        for tag in tags:
            posts_ids = cls.get_posts(tag)
            for post_id in posts_ids:
                result[post_id] += 1

        return bool(result), (key for key, value in sorted(result.iteritems(), key=lambda (k, v): (v, k)))
