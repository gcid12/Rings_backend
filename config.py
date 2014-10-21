# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

#Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
#CSRF_SESSION_KEY = os.environ['MYRING_CSRF_SESSION_KEY']
CSRF_SESSION_KEY = ''

# Secret key for signing cookies
#SECRET_KEY = os.environ['MYRING_SECRET_KEY']
SECRET_KEY = ''


