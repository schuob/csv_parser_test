<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<script type="text/javascript">
var media;
var redir_url;
function delveUploadWidgetCallback(data) 
{
  media = eval("media = " + unescape(data));
 
  document.getElementById('mediaId').innerHTML = media.media_id;
  document.getElementById('desc').innerHTML = media.description;
  document.getElementById('orgFilename').innerHTML = media.original_filename;
  document.getElementById('redirect_b').style.display = "block";
  
  redir_url = "http://web.llnw.jp/mchuob/?mediaId=" + media.media_id;
  
}
</script>

<body>
<?php
$access_key = "fWs5Zl7o+Ws05caJCUONJtORD/s=";
$secret = "kkJkWaU+9vrBiG43nXDulLKgrJg=";
$org_id = "3cdb0e0567264e3fbee117a5663df091";
$base_url = "http://api.videoplatform.limelight.com/rest/organizations/$org_id/";
$http_method = "post";
$upload_url = "${base_url}media";

$signed_request = RestRequest::authenticate_request($http_method, $upload_url, $access_key, $secret);



class RestRequest {

        function authenticate_request($http_verb, $resource_url, $access_key, $secret, $params = null) {
                $parsed_url = parse_url($resource_url);
                $str_to_sign = strtolower($http_verb . '|' . $parsed_url['host'] . '|' . $parsed_url['path']) . '|';
                $url = $resource_url . '?';

                if ($params == null) $params = array();
                if (!array_key_exists('expires', $params)) $params['expires'] = time() + 300;
                $params['access_key'] = $access_key;

                $keys = array_keys($params);
                sort($keys);

                foreach ($keys as $key) {
                        $str_to_sign .= $key . '=' .$params[$key] . '&';
                        $url .= rawurlencode($key) . '=' .rawurlencode($params[$key]) . '&';
                }

                $str_to_sign = chop($str_to_sign,'&');
                $signature = base64_encode(hash_hmac('sha256', $str_to_sign, $secret, true));
                $url .= 'signature=' . rawurlencode($signature);
				return $url;
		}

}

$signed_request = rawurlencode($signed_request);
$redirect = rawurlencode("");

echo '<object id="obj1" classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=8,5,0,0" height="400" width="500">';
echo '<param name="src" value="http://assets.delvenetworks.com/upload-widget/current.swf"/>';
echo '<param name="AllowScriptAccess" value="always"/>';
echo '<param name="flashvars" value="presigned_url=' . $signed_request . '&redirect_to=' . $redirect . '"/>';
echo '<embed name="obj2" pluginspage="http://www.macromedia.com/go/getflashplayer" AllowScriptAccess="always" src="http://assets.delvenetworks.com/upload-widget/current.swf" height="325" width="475" flashvars="presigned_url=' . $signed_request . '&redirect_to=' . $redirect . '"/>';
echo '</object>';

echo "<br /><br />";
echo "Details of the recently uploaded media: <br /><br />";
echo "Media ID = <span id='mediaId'></span>";
echo "<br />";
echo "Description = <span id='desc'></span>";
echo "<br />";
echo "Original Filename = <span id ='orgFilename'></span>";
echo "<br /><br />";
echo "<span id='redirect_b' style='display: none'>";
echo "<input type='button' onClick='javascript:window.location = redir_url;' value='Press to Redirect with New Media ID as a Query String'/>";
echo "</span>";



?>
</body>
</html>
