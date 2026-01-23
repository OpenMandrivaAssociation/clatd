%undefine _debugsource_template

Name:		clatd
Version:	2.1.0
Release:	2
Source0:	https://github.com/toreanderson/clatd/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Summary:	A 464XLAT CLAT implementation for Linux
URL:		https://github.com/toreanderson/clatd
License:	MIT
Group:		Network

BuildRequires:	make
BuildRequires:  perl-base
BuildRequires:  systemd

Requires:	tayga
Requires:	nftables
Requires:	iproute2
Requires:	perl-JSON
Requires:	perl-File-Temp
Requires:	perl-Net-DNS
Requires:	perl-Net-IP
Requires:	perl-IPC-Cmd
Requires:	perl
Requires:	networkmanager

%description
clatd implements the CLAT component of the 464XLAT network architecture specified in RFC 6877. It allows an IPv6-only host to have IPv4 connectivity that is translated to IPv6 before being routed to an upstream PLAT (which is typically a Stateful NAT64 operated by the ISP) and there translated back to IPv4 before being routed to the IPv4 internet. This is especially useful when local applications on the host requires actual IPv4 connectivity or cannot make use of DNS64 (for example because they use legacy AF_INET socket calls, or if they are simply not using DNS64).

clatd may also be used to implement an SIIT-DC Edge Relay as described in RFC 7756. In this scenario, the PLAT is in reality a SIIT-DC Border Relay (see RFC 7755) instead of a Stateful NAT64 (see RFC6146). When used as a SIIT-DC Edge Relay, you will probably want to manually configure the settings clat-v4-addr, clat-v6-addr, and plat-prefix to mirror the SIIT-DC Border Relay's configuration.

%prep
%autosetup -p1
sed -i 's,(SYSCONFDIR)/NetworkManager,(PREFIX)/lib/NetworkManager,g' Makefile
sed -i "s,%{_sbindir}/clatd,%{_sbindir}/clatd -c %{_sysconfdir}/%{name}.conf," scripts/*

%build
echo -e '# Default clatd.conf\n# See clatd(8) for a list of config directives' > %{name}.conf

%install
mkdir -p %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{_prefix}/lib/NetworkManager/dispatcher.d

%make_install
install -p -D -m0644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf
install -p -D -m0644 scripts/%{name}.systemd %{buildroot}%{_unitdir}/%{name}.service

%post
%systemd_post %{name}.service

%files
%doc README.pod
%license LICENCE # Upstream spelled LICENSE incorrectly, build will fail if they fix this
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_prefix}/sbin/%{name}
%{_prefix}/lib/NetworkManager/dispatcher.d/50-clatd
%{_mandir}/man8/*.8*
%{_unitdir}/%{name}.service

# Unfortunately, there is no NetworkManager subpackage providing these
%dir %{_prefix}/lib/NetworkManager
%dir %{_prefix}/lib/NetworkManager/dispatcher.d

%changelog
* Fri Jan 23 2026 Lee Talbert - 2.1.0-1
- Initial build for OpenMandriva.  From this point forward all changes can be found on the OM github.

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Sat Nov 08 2025 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.1.0-3
- Changed perl deps since last version, bz#2413482

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Mar 26 2025 Ingvar Hagelund <ingvar@redpill-linrpo.com> - 2.1.0-1
- New upstream release 2.1.0

* Thu Feb 13 2025 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.0.0-2
- Unified sbin/bin from f42

* Mon Feb 10 2025 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.0.0-1
- New upstream release 2.0.0
- Use more of upstream Makefile for build/install

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Mar 06 2023 Ingvar Hagelund <ingvar@redpill-linpro.com> - 1.6-1
- New upstream release
- Pulled support for el6

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 20 2021 Michal Josef Špaček <mspacek@redhat.com> - 1.5-7
- Remove patch files, which are in upstream
- Rewrite obsolete perl dependency (IO::Socket::INET6 to IO::Socket::IP)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Aug 22 2019 Lubomir Rintel <lkundrak@v3.sk> - 3.5-3
- Move the NetworkManager dispatcher script out of /etc

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 21 2019 Ingvar Hagelund <ingvar@redpill-linpro.com> - 1.5-1
- New upstream release
- Dropped patches included upstream

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 26 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> - 1.4-7
- Set a macro perl-interpreter for backwards compatibility for el6

* Tue Sep 26 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> - 1.4-6
- Readded requirement of Net::IP. By some reason, it is not added
  automatically in mock builds. Closes bz #1494867

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Petr Pisar <ppisar@redhat.com> - 1.4-4
- perl dependency renamed to perl-interpreter
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jun 28 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 1.4-2
- Fixes for bz#1302876, including
- Now BuildRequires pod2man
- Requires perl(Net::IP) is autogenerated, so not needed explicit
- clatd.conf is marked as config file
- Packaged 1.4 release tarball, and added changes from upstream as patches

* Tue Feb 23 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 1.4-1.3.20160128git1abcec1
- Package now (co)owns /etc/NetworkManager/dispatcher.d, and no longer
  requires initscripts (bz #1302876)

* Thu Jan 28 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 1.4-1.2.20160128git1abcec1
- First wrap for fedora and epel
