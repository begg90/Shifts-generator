# the only heavy tests, done with realistic data.
# we should try and keep them as small as possible to keep the pipeline fast
# we could also choose to run them only once a week, for example, instead of at each PR.
# Though, there are consequences to this type of choice. Perhaps, if we are worried about github actions runners time, 
# we could run these locally before each PR. 
# It will depend on how heavy and slow they are