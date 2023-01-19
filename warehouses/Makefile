.PHONY: build-infra init-packages clean
.DEFAULT_GOAL = build-infra

INFRA=$(subst env/,/var/lib/lxc/,$(wildcard env/warehouse-*))
PACKAGES=$(subst env/,/var/lib/lxc/,$(wildcard env/package-*))
RADIO=$(shell ls env/ | wc -l)

/usr/bin/lxc-create:
	apt-get install -qq lxc iw rsync
	systemctl start lxc.service

/var/lib/lxc/base-warehouse: scripts/lxc-base-warehouse.sh /usr/bin/lxc-create
	scripts/lxc-base-warehouse.sh

/var/lib/lxc/base-package: scripts/lxc-base-package.sh /usr/bin/lxc-create
	scripts/lxc-base-package.sh

/sys/module/mac80211_hwsim:
	modprobe mac80211_hwsim radios=$(RADIO)

/var/lib/lxc/warehouse-%: env/warehouse-% scripts/add-warehouse.sh /var/lib/lxc/base-warehouse /sys/module/mac80211_hwsim
	scripts/add-warehouse.sh -e $<

/var/lib/lxc/package-%: env/package-% scripts/add-package.sh /var/lib/lxc/base-package /sys/module/mac80211_hwsim
	scripts/add-package.sh -e $<

build-infra: $(INFRA)

init-packages: $(PACKAGES)

clean:
	modprobe -r mac80211_hwsim
