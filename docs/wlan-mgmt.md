# Wlan managment

## Wlan interfaces

```bash
# Create 6 wlan virtual interfaces
modprobe mac80211_hwsim radios=6

# Remove virtual interfaces
modprobe -r mac80211_hwsim
```

```bash
# Get global wlan config
iwconfig

# Get phy associated to wlan devives
iw dev
```

## Network namespaces

```bash
# Create new namespace named net1
ip netns add net1

# List netns
ip netns list
```

```bash
# Add wlan associate to phy4 interface in netns net1
iw phy phy4 set netns "$(ip netns exec net1 sh -c 'sleep 1 >&- & echo "$!"')"

# Move phy4 back to the root netns
ip netns exec net1 iw phy phy4 set netns 1
```

## References

- [mac80211_hwsim - software simulator of 802.11 radio(s) for mac80211](https://www.kernel.org/doc/html/latest/networking/mac80211_hwsim/mac80211_hwsim.html)
