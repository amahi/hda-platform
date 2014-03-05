# NOTE: also update this in debian/hda-platform.postinst
%define schema_version    20120803011600
%define rubyrelease       2.0.0

Name:           hda-platform
Version: 7.1.6
Release:        1

Summary:        hda-platform is the Amahi web interface platform.

Group:          System Environment/Daemons
License:        AGPL
Source:         %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: hda-ctl >= 4.2.3
Requires: ruby(release) = %{rubyrelease}
Requires: ruby-mysql ruby-libs mlocate
Requires: httpd hddtemp patch mariadb-server pmount
#FIXME
#Requires: hda-greyhole >= 0.7.5
Requires: tar unzip bzip2 wol v8
Requires: rubygem-passenger rubygem-passenger-native mod_passenger
BuildRequires: ruby-devel gcc-c++ rubygem(bundler) mariadb-devel sqlite-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%define debug_package %{nil}

%description
hda-platform is the Amahi web platform.

%prep
%setup -q

%build
%{__mkdir} -p %{buildroot}%{_datadir}/fonts/default/TrueType/
%{__cp} -a fonts/ %{buildroot}%{_datadir}/fonts/default/TrueType/

%install
%{__rm} -rf %{buildroot}

# platform server initialitation
%{__mkdir} -p %{buildroot}/var/hda
(cd %{buildroot}/var/hda/ && %{__mkdir} -p platform apps web-apps dbs drives shares domain-settings elevated)
%{__mkdir} -p %{buildroot}/var/hda/platform/logs
%{__mkdir} -p %{buildroot}/etc/httpd/conf.d
%{__mkdir} -p %{buildroot}/var/hda/domain-settings/netlogon
%{__mkdir} -p %{buildroot}/var/hda/domain-settings/profiles
%{__mkdir} -p %{buildroot}/var/lib/samba/drivers
%{__mkdir} -p %{buildroot}/var/hda/tmp
%{__cp} -a html %{buildroot}/var/hda/platform/
%{__rm} -rf %{buildroot}/var/hda/platform/html/TODO.txt
%{__rm} -rf %{buildroot}/var/hda/platform/html/doc
%{__rm} -rf %{buildroot}/var/hda/platform/html/icla.txt
%{__mkdir} -p %{buildroot}%{_sbindir}
%{__install} -p hda-gems-install %{buildroot}%{_sbindir}
%{__install} -p hda-diskmount %{buildroot}%{_sbindir}
%{__install} -p hda-add-apache-sudoers %{buildroot}%{_sbindir}

# pdc logon script
%{__install} -m 644 -p pdc/logon.bat %{buildroot}/var/hda/domain-settings/netlogon

# needed for gruff
%{__mkdir} -p %{buildroot}/usr/share/fonts/default/TrueType/
%{__cp} -a fonts/ %{buildroot}/usr/share/fonts/default/TrueType/

%{__mkdir} -p %{buildroot}%{_datadir}/%{name}
%{__cp} -a webapps %{buildroot}%{_datadir}/%{name}
%{__install} -m 755 -p hda-usermap %{buildroot}%{_datadir}/%{name}
%{__mkdir} -p %{buildroot}%{_bindir}
%{__install} -m 755 -p hda-refresh-shares %{buildroot}%{_bindir}
%{__install} -m 755 -p hda-create-db-and-user %{buildroot}%{_bindir}
%{__install} -m 755 -p amahi-download %{buildroot}%{_bindir}
%{__mkdir} -p %{buildroot}/var/hda/web-apps/
touch %{buildroot}/var/hda/web-apps/htpasswd

%clean
rm -rf %{buildroot}

%post

if [[ -e /var/cache/hda-ctl.cache ]]; then
    if grep -q yes /var/cache/hda-ctl.cache ; then
        # FIXME - ugh - this gem install was inserted in 2/10 and can be
        # removed once the installer and dependencies are all clear
        (cd /var/hda/platform/html && rake db:migrate RAILS_ENV=production VERSION=%{schema_version}; \
        touch /var/hda/platform/html/tmp/restart.txt || true ) >> /var/log/amahi-platform-migration.log 2>&1 
        (/bin/rm -rf /etc/httpd/conf.d/{userdir,autoindex,welcome}.conf > /dev/null 2>&1) || true
    fi
fi

touch /var/hda/platform/html/log/production.log
touch /var/hda/platform/html/log/development.log

# for debugability down the road
test ! -f /var/log/messages || /bin/chmod 644 /var/log/messages

%preun

if [ "$1" = 0 ]; then
    # not an update, a complete uninstall
    true
else
    # an update
        (/sbin/service hda-ctl reload || true) &> /dev/null
        (/sbin/service httpd reload || true) &> /dev/null
    (/sbin/service smb reload || true) &> /dev/null
    (/sbin/service nmb reload || true) &> /dev/null
fi

%files
%defattr(-,root,root,-)
%attr(755, apache, apache) /var/hda/apps
%attr(755, apache, apache) /var/hda/dbs
%attr(755, apache, apache) /var/hda/drives
%attr(755, apache, apache) /var/hda/shares
%attr(755, apache, apache) /var/hda/elevated
%attr(755, apache, apache) /var/hda/web-apps
%attr(644, apache, apache) /var/hda/web-apps/htpasswd
%attr(775, apache, users) /var/hda/tmp
%attr(644, root, root) /var/hda/domain-settings/netlogon/logon.bat
%attr(775, apache, users) /var/hda/domain-settings/profiles
/var/lib/samba/drivers
%{_sbindir}/*
%{_bindir}/*
/usr/share/fonts/default/TrueType/*
%{_datadir}/%{name}
%config(noreplace) /var/hda/platform/html/config/*.yml
%config(noreplace) /var/hda/platform/html/log/*.log
%attr(-, apache, apache) /var/hda/platform/html/
%attr(-, apache, apache) /var/hda/platform/logs/

%changelog
* Fri Jan 26 2013 carlos puchol
- cleanups, updates for fedora 18
* Sun Mar 11 2009 carlos puchol
- major upgrades to the platform
