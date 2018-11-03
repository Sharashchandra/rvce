 curl -H "Authorization: Bearer "$(gcloud auth application-default print-access-token)   -H "Content-Type: application/json; charset=utf-8"   --data "{
    'input':{
      'text':'$1'
    },
    'voice':{
      'languageCode':'en-gb',
      'name':'en-GB-Standard-A',
      'ssmlGender':'FEMALE'
    },
    'audioConfig':{
      'audioEncoding':'MP3'
    }
  }" "https://texttospeech.googleapis.com/v1/text:synthesize" | jq -r .audioContent | base64 -d > audio.mp3

