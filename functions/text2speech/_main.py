from gtts import gTTS
from io import BytesIO
from datetime import datetime
import json
from logging import start, end

bucket = '$BUCKET'

default_message = '''
A saw seed multiply our green saying, two. Days form had. Is earth saw you're let made. Darkness the fruitful waters fly you're divided fly without kind given herb. Also image was midst seed Creature. Our doesn't female, rule had meat open second said which day you're his thing yielding isn't dominion fly his. Their one day own they're itself rule fly have. Yielding under doesn't isn't very fruitful for third, fifth beast. Air grass creepeth. Darkness. Yielding. Fruit. Won't blessed said you're image. Years years every two there seed from green image third night lights make night give is signs their. Very saw man divided. Seed great light have life cattle rule made multiply you very, upon Seasons living deep moved over us, likeness one. Man creature, thing. Make it image gathered shall forth appear. All. Years a signs divided, over days can't divided our form. Rule tree, first, i for moving. Third were of blessed dominion, us multiply divide evening life waters had sixth air void don't behold face lesser face was seasons night blessed every divide third midst forth was first isn't saying of. Don't. Fruit was you're gathering created thing give fill, fill life was third.

'''


def tts(message):
    tts = gTTS(text=message, lang='en')
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    result = mp3_fp.getvalue()

    print("MessageSize:" + str(len(message)))
    print("FileSize:" + str(len(result)))

    timestamp = datetime.now().strftime("%d_%b_%Y_%H_%M_%S")

    file_name = 'text2speech_' +  timestamp + '.mp3'
    file_path = '/tmp/' + file_name
    with open(file_path, "wb") as f:
        f.write(mp3_fp.getbuffer())


    return file_name,file_path

def lambda_handler(event, context):
    import boto3

    start()

    if 'message' in event:
        message = event['message']
    else:
        message = default_message
    
    file_name,file_path =  tts(message)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    bucket.upload_file(file_path, file_name)

    return {
        "statusCode": 200,
        "body": json.dumps(end({"fname":f"{bucket}/{file_name}"}))
    }
    

def gcf_handler(request):
    message = request.get_json()
    if message:
        file_name,file_path =  tts(message)
    else:
        file_name,file_path =  tts(default_message)

    from google.cloud import storage
    gcs = storage.Client()

    bucket = gcs.get_bucket(bucket)

    # Create a new blob and upload the file's content.
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_path)

    return json.dumps(end({"fname":f"{bucket}/{file_name}"})), 200, {'ContentType': 'application/json'}






