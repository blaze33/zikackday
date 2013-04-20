
# thanks http://stackoverflow.com/a/10984286/343834
import base64
import uuid

# get a UUID - URL safe, Base64
def get_a_Uuid():
    r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    return r_uuid.replace('=', '')
