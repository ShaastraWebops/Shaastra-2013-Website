import urllib2, urllib

API_SSL_SERVER="https://api-secure.recaptcha.net"
API_SERVER="http://api.recaptcha.net"
VERIFY_SERVER="api-verify.recaptcha.net"

customized_output_for_userportal = """
    <script>
var RecaptchaOptions = {
   theme: 'custom',
   lang: 'en',
   custom_theme_widget: 'recaptcha_widget'
};
</script>

<div id="recaptcha_widget" style="display:none">

    <div id="recaptcha_image" style="height: 48px; width: 250px; border:1px solid #0050F2"></div>
    <input type="text" id="recaptcha_response_field" name="recaptcha_response_field" />

    <div><a href="javascript:Recaptcha.reload(),SmallImage2()">Get another CAPTCHA</a><a>&nbsp &nbsp</a><a href="javascript:Recaptcha.showhelp()">Help</a></div>

</div>
   
<script type="text/javascript" src="%(ApiServer)s/challenge?k=%(PublicKey)s%(ErrorParam)s"></script>

<noscript>
  <iframe src="%(ApiServer)s/noscript?k=%(PublicKey)s%(ErrorParam)s" height="300" width="500" frameborder="0"></iframe><br />
  <textarea name="recaptcha_challenge_field" rows="3" cols="40"></textarea>
  <input type='hidden' name='recaptcha_response_field' value='manual_challenge' />
</noscript>

<script>
function SmallImage(){
    document.getElementById("recaptcha_image").childNodes[0].width = 225;
    document.getElementById("recaptcha_image").childNodes[0].height = 43;
    document.getElementById("recaptcha_image").style.width = "225px";
    document.getElementById("recaptcha_image").style.height = "43px";
}
function SmallImage2(){
    var t1 = setTimeout('SmallImage()',500);
    var t2 = setTimeout('SmallImage()',1000);
    var t3 = setTimeout('SmallImage()',1500);
    var t4 = setTimeout('SmallImage()',2000);
    var t5 = setTimeout('SmallImage()',3000);
    var t6 = setTimeout('SmallImage()',5000); //these are for slower connections
}
SmallImage();
</script>"""

default_output = """<script type="text/javascript" src="%(ApiServer)s/challenge?k=%(PublicKey)s%(ErrorParam)s"></script>

<noscript>
  <iframe src="%(ApiServer)s/noscript?k=%(PublicKey)s%(ErrorParam)s" height="300" width="500" frameborder="0"></iframe><br />
  <textarea name="recaptcha_challenge_field" rows="3" cols="40"></textarea>
  <input type='hidden' name='recaptcha_response_field' value='manual_challenge' />
</noscript>
""" 
        
class RecaptchaResponse(object):
    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code

def displayhtml (public_key,
                 use_ssl = False,
                 error = None):
    """Gets the HTML to display for reCAPTCHA

    public_key -- The public api key
    use_ssl -- Should the request be sent over ssl?
    error -- An error message to display (from RecaptchaResponse.error_code)"""

    error_param = ''
    if error:
        error_param = '&error=%s' % error

    if use_ssl:
        server = API_SSL_SERVER
    else:
        server = API_SERVER

    return customized_output_for_userportal % {'ApiServer' : server,'PublicKey' : public_key,'ErrorParam' : error_param,}

def submit (recaptcha_challenge_field,
            recaptcha_response_field,
            private_key,
            remoteip):
    """
    Submits a reCAPTCHA request for verification. Returns RecaptchaResponse
    for the request

    recaptcha_challenge_field -- The value of recaptcha_challenge_field from the form
    recaptcha_response_field -- The value of recaptcha_response_field from the form
    private_key -- your reCAPTCHA private key
    remoteip -- the user's ip address
    """

    if not (recaptcha_response_field and recaptcha_challenge_field and
            len (recaptcha_response_field) and len (recaptcha_challenge_field)):
        return RecaptchaResponse (is_valid = False, error_code = 'incorrect-captcha-sol')
    

    def encode_if_necessary(s):
        if isinstance(s, unicode):
            return s.encode('utf-8')
        return s

    params = urllib.urlencode ({
            'privatekey': encode_if_necessary(private_key),
            'remoteip' :  encode_if_necessary(remoteip),
            'challenge':  encode_if_necessary(recaptcha_challenge_field),
            'response' :  encode_if_necessary(recaptcha_response_field),
            })

    request = urllib2.Request (
        url = "http://%s/verify" % VERIFY_SERVER,
        data = params,
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "User-agent": "reCAPTCHA Python"
            }
        )
    
    httpresp = urllib2.urlopen (request)

    return_values = httpresp.read ().splitlines ();
    httpresp.close();

    return_code = return_values [0]

    if (return_code == "true"):
        return RecaptchaResponse (is_valid=True)
    else:
        return RecaptchaResponse (is_valid=False, error_code = return_values [1])


