# routers/__init__.py
# Export submodules so `from routers import auth, users, blogs, careers` works.
from . import auth, users, blogs, careers, setting
# No other logic here; just exposes routers as package attributes.
