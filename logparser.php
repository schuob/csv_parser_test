<?php

date_default_timezone_set("America/Los_Angeles");
error_reporting(E_ALL);
ini_set('display_errors', 1);

$path = '/var/www/html/mchuob/callback_logs';

if ($handle = opendir($path)) {
        $files = array();
        while (false !== ($entry = readdir($handle)) && $entry != ".." && $entry != ".") {
                if (is_dir($path . '/' . $entry)){
                } else {
                       array_push($files, $entry);
                }
        }

        closedir($handle);
        rsort($files);
}

// variables
$current_log = $path . '/' . $files[0];

$handle = fopen($current_log, "r");
if ($handle) {
    $resp = array();
    $count = 0;
    while (($buffer = fgets($handle, 4096)) !== false) {
        $pieces = explode('&', $buffer);
        foreach ($pieces as &$piece) {
                $piece = str_replace('"', "", $piece);
                $piece = str_replace("\n", "", $piece);
                $callback = explode('=', $piece);
                $key = $callback[0];
                $value = $callback[1];
                $resp['items'][$count][$key] = $value;
        }
        $count += 1;
    }
    if (!feof($handle)) {
        echo "Error: unexpected fgets() fail\n";
    }
    fclose($handle);
}

$json_file = '/var/www/html/mchuob/callback_logs/json/response.json';
$fp = fopen($json_file, 'w');
fwrite($fp, json_encode($resp));
fclose($fp);

?>