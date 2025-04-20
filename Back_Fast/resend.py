import resend

resend.api_key = "re_Hsg6A2Hq_HPqdbLFGzPPzyW6uEGdur4RA"

r = resend.Emails.send({
    "from": "CrackSchoolg@wasa.dev",
    "to": "jhosuepin@hotmail.com",
    "subject": "Hello World",
    "html": "<p>Algo een bbbbbb wasa</p>"
})
