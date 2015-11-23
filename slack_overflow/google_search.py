"""Search should be imported from this module so that the patch
is ensured
"""

import google
from google.google import search

# The library normalizes the search query before sending it;
#  we do not want this as normalizing breaks
#  our site:stackoverflow.com/questions filter. Thus, we patch the
#  normalize query function to not do anything
google.modules.utils.normalize_query = lambda s: s

__all__ = ['search']
