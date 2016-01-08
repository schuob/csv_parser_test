<?php

// LvpAuthUtil v1.1 10-Feb-11
// This file is offered as a convenient utility to authenticate requests

// Updated by Steven Chuob to include an execute function that will execute the URL
// with CURL and the proper http_method based on switch

	class RestRequest
	{
		
		function authenticate_request($http_verb, $resource_url, $access_key, $secret, $params = null)
		{
			$parsed_url = parse_url($resource_url);
			$str_to_sign = strtolower($http_verb . '|' . $parsed_url['host'] . '|' . $parsed_url['path']) . '|';
			$url = $resource_url . '?';
	
			if ($params == null) $params = array();
			if (!array_key_exists('expires', $params)) $params['expires'] = time() + 300;
			$params['access_key'] = $access_key;
	
			$keys = array_keys($params);
			sort($keys);
	
			foreach ($keys as $key)
			{
				$str_to_sign .= $key . '=' .$params[$key] . '&';
				$url .= rawurlencode($key) . '=' .rawurlencode($params[$key]) . '&';
			}
	
			$str_to_sign = chop($str_to_sign,'&');
			$signature = base64_encode(hash_hmac('sha256', $str_to_sign, $secret, true));
			$url .= 'signature=' . rawurlencode($signature);
	
			return $url;
		}
		
		public function execute ($http_verb, $signed_url, $params=array())  
	    {
			$curl = new RestRequest;
			$ch = curl_init($signed_url);
						
			try
			{
				switch (strtoupper($http_verb))
				{
					case 'GET':
						$curl->setCurlOpts($ch);
						$output = curl_exec($ch);
						$contentype = curl_getinfo($ch, CURLINFO_CONTENT_TYPE);
						$httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
						if(curl_errno($ch)) {
					        $output = curl_error($ch);
					        }
						curl_close($ch);
			        	break;
			  		case 'POST':
						curl_setopt($ch, CURLOPT_POST, true);
						curl_setopt($ch, CURLOPT_POSTFIELDS, $params);  
			  			$curl->setCurlOpts($ch);
						$output = curl_exec($ch);
						$contentype = curl_getinfo($ch, CURLINFO_CONTENT_TYPE);
						$httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
						curl_close($ch);
			            break;
				    case 'PUT':
				  		curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'PUT');
						curl_setopt($ch, CURLOPT_POSTFIELDS, $params);  
			            $curl->setCurlOpts($ch); 
						$output = curl_exec($ch);
						$contentype = curl_getinfo($ch, CURLINFO_CONTENT_TYPE);
						$httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
						curl_close($ch); 
			            break;  
			        case 'DELETE':
						curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'DELETE');
						$curl->setCurlOpts($ch);
						$output = curl_exec($ch);
						$contentype = curl_getinfo($ch, CURLINFO_CONTENT_TYPE);
						$httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
						if(curl_errno($ch)) {
							$output = curl_error($ch);
					        }
						curl_close($ch);
			            break;  
			        default:  
			            throw new InvalidArgumentException('Current verb (' . $http_verb . ') is an invalid REST verb.');  
			        }  
			    }  
			    catch (InvalidArgumentException $e)  
			    {  
			        curl_close($ch);  
			        throw $e;  
			    }  
			    catch (Exception $e)  
			    {  
			        curl_close($ch);  
			        throw $e;  
			    }
			return array($output,$contentype,$httpcode);  

	    }
			
		protected function setCurlOpts (&$curlHandle)  
	    {
			curl_setopt($curlHandle, CURLOPT_RETURNTRANSFER, true);
			curl_setopt($curlHandle, CURLOPT_HEADER, false);
			curl_setopt($curlHandle, CURLOPT_VERBOSE, 1);
	    }		

	}   

?>