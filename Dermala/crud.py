from Dermala import get_model,storage
import json
from flask import make_response,Response
from flask import Blueprint, current_app, redirect, render_template, request, url_for

crud = Blueprint('crud', __name__)
# [START upload_image_file]
def upload_image_file(file):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not file:
        return None
    print(file['file'])

    public_url = storage.upload_file(
        file['file'],
        file['filename'],
        file['content_type']
    )
    print(public_url)
    current_app.logger.info(
        "Uploaded file %s as %s.", file['filename'], public_url)

    return public_url
# [END upload_image_file]
@crud.route("/album",methods=['GET', 'POST'])
def list():

    if request.method == 'POST':

        token = request.args.get('page_token', None)
        if token:
            token = token.encode('utf-8')

        books, next_page_token = get_model().list(cursor=token,kinds='photo')

        data = {}

        data['data'] = books

        data['success'] = True

        data['total'] = 8

        data = json.dumps(data)
        
        return Response(data)


# [START signup]

@crud.route("/user/login",methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = json.loads(request.get_data().decode('utf8'))

        print(data)

        filters = ('email',data['email'])

        print(filters)

        users = get_model().lookup('signup',filters)

        if users == []:
            return Response({'success':False})
        print('q')

        for user in users:
            if user['password'] == data['password']:
                return Response(json.dumps({'success':True}))
        print('w')
    
        return Response(json.dumps({'success':False}))
    return Response(json.dumps({'success':False}))
# [END signup]

 # [START add]
@crud.route('/user/signup', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        
        data = json.loads(request.get_data().decode('utf8'))

        userInfo = get_model().create(data,keys=data['key'])

        resp = {}

        resp['success'] = True

        resp['data'] = {"1":"2"}

        resp = json.dumps(resp)
        
        return Response(resp)

    return Response('2')
# [END add]

#[START add photos]
@crud.route('/addphoto', methods=['GET', 'POST'])
def addPhoto():

    if request.method == 'POST':

        data = json.loads(request.get_data().decode('utf8'))

        # If an image was uploaded, update the data to point to the new image.
        
        # [START image_url]
        print(data)
        image_url = upload_image_file(data)
        # [END image_url]

        print(image_url)

        # [START image_url2]
        if image_url:
            data['imgurl'] = image_url
        # [END image_url2]

        #userInfo = get_model().create(data)

        resp = {}

        resp['success'] = True

        resp['data'] = data

        resp = json.dumps(resp)

        return Response(resp)

    return Response('2')

#[END add photos]

@crud.route('/comments', methods=['GET', 'POST'])
def addAlbum():

    if request.method == 'POST':

        data = json.loads(request.get_data().decode('utf8'))

        userInfo = get_model().create(data,keys=data['key'])

        resp = {}

        resp['success'] = True

        resp['data'] = data

        resp = json.dumps(resp)

        return Response(resp)

    return Response('2')

#[END add photos]





