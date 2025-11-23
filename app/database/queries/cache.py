" A module that provides caching functionality for the application using the Dogpile cache library. "
from dogpile.cache import make_region

cache_region = make_region().configure(
    "dogpile.cache.memory",  # In-memory caching (other options available)
)
