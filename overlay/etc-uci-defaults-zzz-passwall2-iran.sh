#!/bin/sh
# =============================================================================
# First-boot setup for the Iran build of OpenWrt + Passwall2 (Google WiFi/Gale)
#
# Runs ONCE automatically on first boot, then OpenWrt deletes it (exit 0).
#
# IMPORTANT: the filename starts with "zzz-" on purpose. uci-defaults scripts
# run in sorted order, and Passwall2's own "luci-passwall2" script is what
# copies /usr/share/passwall2/0_default_config into /etc/config/passwall2
# (creating the "rulenode" shunt node). "zzz-..." sorts AFTER "luci-..." so by
# the time we run, the shunt node already exists and we can attach our rule to
# it. (The old name "99-custom-passwall2" sorted BEFORE it, which silently
# blocked Passwall2's defaults from ever loading.)
#
# It does three things:
#   1. Creates the "Iran Bypass" shunt rule (Iranian domains + IPs).
#   2. Attaches that rule to the active shunt node as Direct, so Iranian
#      traffic bypasses the proxy out of the box -- no clicks needed.
#   3. Removes the broken Passwall feed URLs from the on-device package feed
#      list, so `apk update` no longer fails with "error 8 / unexpected end of
#      file" and no duplicate feeds are left behind.
# =============================================================================

[ -x /sbin/uci ] || exit 0

# --- 0) Safety net: make sure Passwall2's default config is present ----------
# Normally luci-passwall2 already did this. If for any reason it did not, load
# the defaults now so the shunt node ("rulenode") exists before we touch it.
if [ ! -s /etc/config/passwall2 ] && [ -f /usr/share/passwall2/0_default_config ]; then
	cp -f /usr/share/passwall2/0_default_config /etc/config/passwall2
fi

# --- 1) Create the "Iran Bypass" shunt rule ----------------------------------
# Domain side: any .ir domain, the Persian IDN TLD (.ایران), and the Iran
#              geosite category from the embedded geosite_IR.dat.
# IP side    : the Iran geoip category from the embedded geoip_IR.dat.
# Both .dat files are shipped at /usr/share/v2ray/ (Xray "ext:" asset path).
DOMAIN_LIST='regexp:.*\.ir$
regexp:.*\.xn--mgba3a4f16a$
ext:geosite_IR.dat:ir'

IP_LIST='ext:geoip_IR.dat:ir'

# Recreate cleanly so re-runs stay idempotent.
uci -q delete passwall2.IranBypass 2>/dev/null

uci set passwall2.IranBypass='shunt_rules'
uci set passwall2.IranBypass.remarks='Iran Bypass'
uci set passwall2.IranBypass.network='tcp,udp'
uci set passwall2.IranBypass.domain_list="$DOMAIN_LIST"
uci set passwall2.IranBypass.ip_list="$IP_LIST"

# --- 2) Attach the rule to every shunt node as Direct (bypass) ---------------
# On a Passwall2 shunt node, each shunt rule is stored as an option whose KEY
# is the rule's section name. Value "_direct" = Direct Connection (bypass).
# We loop over all "_shunt" nodes so it works even if the node was renamed.
SHUNT_NODES=$(uci show passwall2 2>/dev/null \
	| sed -n "s/^passwall2\.\([^.]*\)\.protocol='_shunt'\$/\1/p")
[ -z "$SHUNT_NODES" ] && SHUNT_NODES="rulenode"

for node in $SHUNT_NODES; do
	uci -q set "passwall2.$node.IranBypass"='_direct'
done

uci commit passwall2

# --- 3) Remove the broken Passwall feeds from the on-device feed list --------
# These two URLs do not exist on downloads.openwrt.org, so `apk update` errors.
# They may appear in the apk feed list (25.x) and/or the opkg one (older).
for feed_file in \
	/etc/apk/repositories.d/distfeeds.list \
	/etc/apk/repositories \
	/etc/opkg/distfeeds.conf \
	/etc/opkg/customfeeds.conf
do
	[ -f "$feed_file" ] || continue
	# '#' used as sed delimiter so we don't have to escape the '/' in the path.
	sed -i -e '\#/passwall2/#d' -e '\#/passwall_packages/#d' "$feed_file"
done

# --- refresh LuCI caches so the new rule shows immediately -------------------
rm -f /tmp/luci-indexcache /tmp/luci-indexcache.* 2>/dev/null
rm -rf /tmp/luci-modulecache/ 2>/dev/null
killall -HUP rpcd 2>/dev/null

exit 0
