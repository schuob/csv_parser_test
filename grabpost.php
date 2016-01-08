<?php

error_reporting(E_ALL);
ini_set('display_errors', 1);

date_default_timezone_set('America/Los_Angeles');

// listening for callbacks
$cb_payload = '';
$cb = fopen('php://input', 'r');
$cb_payload = fgets($cb);

// parsing $cb_payload into a array
$pieces = explode('&', $cb_payload);
foreach ($pieces as &$piece) {
        $callback = explode('=', $piece);
        // grabbing the event_type to trigger other events
        if ($callback[0] == "event_type") {
                $event_type = $callback[1];
        }
        // grabbing the filename to match against a database
        if ($callback[0] == "original_filename") {
                $original_filename = $callback[1];
        }
        // grabbing the media_id for use with an API if needed
        if ($callback[0] == "media_id") {
                $media_id = $callback[1];
        }
        $key = $callback[0];
        $value = $callback[1];
        $callback_array[$key] = $value;
}

// event trigger - can be used to call LVP API
switch (strtoupper($event_type)) {
        case 'MEDIA_CREATED':
                write_log($cb_payload);
                break;
        case 'MEDIA_PROCESSING_SUCCESS':
                write_log($cb_payload);
                break;
        case 'MEDIA_PROCESSING_ERROR':
                write_log($cb_payload);
				break;
        case 'MEDIA_METADATA_MODIFIED':
                write_log($cb_payload);
                break;
        case 'MEDIA_REPLACED':
                write_log($cb_payload);
                break;
        case 'MEDIA_DELETED':
                write_log($cb_payload);
                break;
        case 'CHANNEL_CREATED':
                write_log($cb_payload);
                break;
        case 'CHANNEL_METADATA_MODIFIED':
                write_log($cb_payload);
                break;
        case 'CHANNEL_CONTENTS_MODIFIED':
                write_log($cb_payload);
                break;
        case 'CHANNEL_DELETED':
                write_log($cb_payload);
                break;
        case 'CHANNEL_GROUP_CREATED':
                write_log($cb_payload);
                break;
        case 'CHANNEL_GROUP_METADATA_MODIFIED':
                write_log($cb_payload);
                break;
        case 'CHANNEL_GROUP_CONTENTS_MODIFIED':
                write_log($cb_payload);
                break;
        case 'CHANNEL_GROUP_DELETED':
                write_log($cb_payload);
                break;
}

// function to write the callback array to a txt file in a specific format
function write_log($str) {
        $logs = '/var/www/html/mchuob/callback_logs/callback_' . date('Y-m-d') . '.txt';
        $time = "log_time=" . date('Y-m-d H:i:s') . "&";
        $q = '"';
        $replace = $q . "&" . $q;
        $update_str = $q . $time . $str . $q;
        $update_str = str_replace('&', $replace, $update_str);
        $output_file = fopen($logs, 'a+');
        fwrite($output_file, $update_str . "\n");
        fclose($output_file);
}


?>