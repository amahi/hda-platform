<?php
/*
 * Amahi HDA API library for common things to do with HDAs for PHP apps
 * Carlos Puchol
 */

require "spyc/spyc.php";

class HDA {
	const DBINFO = "/var/hda/platform/html/config/database.yml";
	static private $DB = "";
	static private $HOST = "";
	static private $USERNAME = "";
	static private $PASSWORD = "";
	static private $db = "";

	function __construct() {
		$info = Spyc::YAMLLoad(self::DBINFO);
		$i = $info['production'];
		self::$DB = $i['database'];
		self::$HOST = $i['host'];
		self::$USERNAME = $i['username'];
		self::$PASSWORD = $i['password'];
		// print_r($info);
		// FIXME - connect to the DB and store it in $db
	}

	function share_paths_with($tags) {
		// print_r(self::$db);
		// FIXME - get all shares with the given list tags, return them 
		// FIXME - return their paths in an array
	}
}

$hda = new HDA;
$hda->shares_with("");
?>
