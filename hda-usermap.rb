#!/usr/bin/env ruby

# mute any warnings
STDERR.reopen '/dev/null'

# FIXME: this script is way too slow - should do something faster

require '/var/hda/platform/html/config/boot'
require 'environment'

def usage
	puts "hda-usermap: \"User Name\""
	puts "\treturns the unix/samba name of the user"
	exit -1
end

def main
	usage if ARGV.length != 1
	username = ARGV[0]
	u = User.find_by_name username
	puts u.login unless u.nil?
	return unless u.nil?
	u = User.find_by_login username
	return if u.nil?
	puts u.login
end

main
