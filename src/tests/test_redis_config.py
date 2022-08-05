import os
import unittest


class TestRedisConfig(unittest.TestCase):
    def setUp(self):
        os.environ.update(
            {
                "CACHE_TYPE": "cache_type_val",
                "CACHE_REDIS_HOST": "cache_redis_host_val",
                "CACHE_REDIS_PORT": "cache_redis_port_val",
                "CACHE_REDIS_DB": "cache_redis_db_val",
                "CACHE_REDIS_URL": "cache_redis_url_val",
                "CACHE_DEFAULT_TIMEOUT": "cache_default_timeout_val",
            }
        )

    def test_redis_config(self):
        from redis_config import RedisConfig

        assert RedisConfig.CACHE_TYPE == "cache_type_val"
        assert RedisConfig.CACHE_REDIS_HOST == "cache_redis_host_val"
        assert RedisConfig.CACHE_REDIS_PORT == "cache_redis_port_val"
        assert RedisConfig.CACHE_REDIS_DB == "cache_redis_db_val"
        assert RedisConfig.CACHE_REDIS_URL == "cache_redis_url_val"
        assert RedisConfig.CACHE_DEFAULT_TIMEOUT == "cache_default_timeout_val"
