%global debug_package %{nil}

Name:		clatd
Version:	2.1.0
Release:	1
Source0:	https://github.com/toreanderson/clatd/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Summary:	A 464XLAT CLAT implementation for Linux
URL:		https://github.com/toreanderson/clatd
License:	MIT
Group:		Network

BuildRequires:	make

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

%build
%make_build

%install
%make_install

%files
%doc README.pod
%{_prefix}/sbin/%{name}
