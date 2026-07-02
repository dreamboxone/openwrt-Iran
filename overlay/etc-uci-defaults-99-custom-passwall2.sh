#!/bin/sh
# First-boot script: creates the "Iran Bypass" shunt rule inside Passwall2
# under Services -> Passwall2 -> Rule Manage, exactly as requested, then
# commits it (equivalent to pressing Save in LuCI).
# This runs once automatically and OpenWrt removes it after success.

[ -x /sbin/uci ] || exit 0

DOMAIN_LIST='regexp:.*\.ir$
regexp:.*\.xn--mgba3a4f16a$
ext:geosite_IR.dat:ir'

IP_LIST='ext:geoip_IR.dat:ir'

uci -q delete passwall2.IranBypass 2>/dev/null

uci set passwall2.IranBypass='shuntrules'
uci set passwall2.IranBypass.remarks='Iran Bypass'
uci set passwall2.IranBypass.network='tcp,udp'
uci set passwall2.IranBypass.domain_list="$DOMAIN_LIST"
uci set passwall2.IranBypass.iplist="$IP_LIST"

uci commit passwall2

exit 0
