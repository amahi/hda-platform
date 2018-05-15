VERSION=10.6.2
RPMBASE=$(HOME)/rpmbuild

all: rpm

rpm: update-header dist
	(cd release && rpmbuild -ta hda-platform-$(VERSION).tar.gz)
	mv $(RPMBASE)/RPMS/*/hda-platform-$(VERSION)-*.rpm release/
	mv $(RPMBASE)/SRPMS/hda-platform-$(VERSION)-*.src.rpm release/

deb: update-header dist
	(cd release && ln -sf hda-platform-$(VERSION).tar.gz hda-platform_$(VERSION).orig.tar.gz)
	(cd release && tar -zxf hda-platform_$(VERSION).orig.tar.gz)
	(cd release/hda-platform-$(VERSION)/debian && debuild -us -uc && debuild -S -us -uc)

bundle:
	(cd html && make bundle)

dist: bundle clean
	(mkdir -p html/tmp/cache && cd html/tmp/cache/ && rm -rf *)
	(mkdir -p release && cd release && mkdir -p hda-platform-$(VERSION))
	(mkdir -p html/log && cd html/log && echo -n > production.log && echo -n > development.log && echo -n > test.log)
	rsync -a --exclude=.git debian pdc hda-usermap hda-gems-install hda-platform.spec hda-create-db-and-user html fonts \
		hda-refresh-shares webapps hda-diskmount amahi-download \
		hda-add-apache-sudoers release/hda-platform-$(VERSION)/
	(cd release && tar -czvf hda-platform-$(VERSION).tar.gz hda-platform-$(VERSION))
	(cd release && rm -rf hda-platform-$(VERSION))

update-header:
	sed -i -e 's/^Version:\s*[0-9.]*\s*$$/Version: $(VERSION)/' hda-platform.spec

install: rpm
	(cd release && sudo rpm -Uvh hda-platform-$(VERSION)-*.rpm)

clean:
	find . -name '._*' -exec rm '{}' \;
	# Fedora stores the gems in html/vendor/bundle/ruby/gems
	(cd html/vendor/bundle/ruby/ && \
		find . -type f -exec grep -l '/this/will/be/overwritten/or/wrapped/anyways/do/not/worry/ruby' {} \; | \
		xargs sed -i -e 's|/this/will/be/overwritten/or/wrapped/anyways/do/not/worry/ruby|/usr/bin/ruby|') || true
	# Ubuntu stores the gems in html/vendor/bundle/ruby/1.9.1/gems
	# (where 1.9.1 is the ABI version)
	#(cd html/vendor/bundle/ruby/1.9.1/gems/unicorn-* && \
	#find . -type f -exec grep -l '/this/will/be/overwritten/or/wrapped/anyways/do/not/worry/ruby' {} \; | \
	#xargs sed -i -e 's|/this/will/be/overwritten/or/wrapped/anyways/do/not/worry/ruby|/usr/bin/ruby|') || true

# for a clean bundle, prior to release
distclean:
	        (cd html/vendor/bundle/ && rm -rf ruby)

# separate make target to install what's needed rpm-wise to build the dist
rpm-devel-deps:
	sudo dnf -y install ruby-devel gcc-c++ libxml2-devel libxslt-devel rubygem-bundler mariadb-devel sqlite-devel redhat-rpm-config tar rsync rpm-build

