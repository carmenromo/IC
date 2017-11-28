import os

from hypothesis import settings
from hypothesis import Verbosity

# In addition to the 'default' profile, we provide
settings.register_profile("hard"      , settings(max_examples = 1000))
settings.register_profile("dev"       , settings(max_examples =   10))
settings.register_profile("hard_nocov", settings(max_examples = 1000, use_coverage=False))
settings.register_profile("dev_nocov" , settings(max_examples =   10, use_coverage=False))
settings.register_p
