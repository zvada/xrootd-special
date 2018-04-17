%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%if %{?fedora}%{!?fedora:0} >= 21 || %{?rhel}%{!?rhel:0} >= 7
%global use_systemd 1
%else
%global use_systemd 0
%endif

%if %{?fedora}%{!?fedora:0} >= 22 || %{?rhel}%{!?rhel:0} >= 8
%global use_libc_semaphore 1
%else
%global use_libc_semaphore 0
%endif

%define _alphatag e341f47
%define _release 2

# e.g. '-rc3' or blank
%define _alphasuffix %{?_alphatag:-%{_alphatag}}

Name:		xrootd
Epoch:		1
Version:	4.8.2
Release:        %{?_alphatag:0.}%{_release}%{?_alphatag:.%{_alphatag}}%{?dist}
Summary:	Extended ROOT file server

Group:		System Environment/Daemons
License:	LGPLv3+
URL:		http://xrootd.org/
Source0:        %{name}-%{version}%{?_alphasuffix}.tar.gz

BuildRequires:	cmake
BuildRequires:	krb5-devel
BuildRequires:	libxml2-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	perl-generators
BuildRequires:	readline-devel
BuildRequires:	zlib-devel
BuildRequires:	fuse-devel
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	selinux-policy-devel
%if %{use_systemd}
BuildRequires:	systemd
%endif
BuildRequires:	python2-devel
%if %{?fedora}%{!?fedora:0} >= 13
BuildRequires:  python3-devel
%else
BuildRequires:  python34-devel
%endif

%if %{?_with_ceph:1}%{!?_with_ceph:0}
    %if %{?_with_ceph11:1}%{!?_with_ceph11:0}
BuildRequires: librados-devel >= 11.0
BuildRequires: libradosstriper-devel >= 11.0
    %else
BuildRequires: ceph-devel >= 0.87
    %endif
%endif

Requires:	%{name}-server%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-selinux = %{epoch}:%{version}-%{release}

%description
The Extended root file server consists of a file server called xrootd
and a cluster management server called cmsd.

The xrootd server was developed for the root analysis framework to
serve root files. However, the server is agnostic to file types and
provides POSIX-like access to any type of file.

The cmsd server is the next generation version of the olbd server,
originally developed to cluster and load balance Objectivity/DB AMS
database servers. It provides enhanced capability along with lower
latency and increased throughput.

%package server
Summary:	Xrootd server daemons
Group:		System Environment/Daemons
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-server-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	expect
Requires(pre):		shadow-utils
%if %{use_systemd}
Requires(pre):		systemd
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
%else
Requires(pre):		chkconfig
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts
%endif

%description server
This package contains the xrootd servers without the SELinux support.
Unless you are installing on a system without SELinux also install the
xrootd-selinux package.

%package selinux
Summary:	SELinux policy module for the xrootd server
Group:		System Environment/Daemons
BuildArch:	noarch
Requires:	selinux-policy
Requires(post):		policycoreutils
Requires(postun):	policycoreutils

%description selinux
This package contains SELinux policy module for the xrootd server package.

%package libs
Summary:	Libraries used by xrootd servers and clients
Group:		System Environment/Libraries
#		Java admin client no longer supported
Obsoletes:	%{name}-client-admin-java < 1:3.3.0
#		Perl admin client no longer supported
Obsoletes:	%{name}-client-admin-perl < 1:4.0.0

%description libs
This package contains libraries used by the xrootd servers and clients.

%package devel
Summary:	Development files for xrootd
Group:		Development/Libraries
Provides:	%{name}-libs-devel = %{epoch}:%{version}-%{release}
Provides:	%{name}-libs-devel%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes:	%{name}-libs-devel < %{epoch}:%{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
This package contains header files and development libraries for xrootd
development.

%package client-libs
Summary:	Libraries used by xrootd clients
Group:		System Environment/Libraries
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description client-libs
This package contains libraries used by xrootd clients.

%package client-devel
Summary:	Development files for xrootd clients
Group:		Development/Libraries
Provides:	%{name}-cl-devel = %{epoch}:%{version}-%{release}
Provides:	%{name}-cl-devel%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes:	%{name}-cl-devel < %{epoch}:%{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description client-devel
This package contains header files and development libraries for xrootd
client development.

%package server-libs
Summary:	Libraries used by xrootd servers
Group:		System Environment/Libraries
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description server-libs
This package contains libraries used by xrootd servers.

%package server-devel
Summary:	Development files for xrootd servers
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-devel%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-server-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description server-devel
This package contains header files and development libraries for xrootd
server development.

%package private-devel
Summary:	Legacy xrootd headers
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description private-devel
This package contains some private xrootd headers. The use of these
headers is strongly discouraged. Backward compatibility between
versions is not guaranteed for these headers.

%package client
Summary:	Xrootd command line client tools
Group:		Applications/Internet
Provides:	%{name}-cl = %{epoch}:%{version}-%{release}
Provides:	%{name}-cl%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes:	%{name}-cl < %{epoch}:%{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description client
This package contains the command line tools used to communicate with
xrootd servers.

%package fuse
Summary:	Xrootd FUSE tool
Group:		Applications/Internet
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	fuse

%description fuse
This package contains the FUSE (file system in user space) xrootd mount
tool.

%if %{?fedora}%{!?fedora:0} >= 22
%package ceph
Summary:	Ceph back-end plug-in for xrootd
Group:		Development/Tools
Requires:	%{name}-server%{?_isa} = %{epoch}:%{version}-%{release}

%description ceph
This package contains a ceph back-end plug-in for xrootd.
%endif

#-------------------------------------------------------------------------------
# python2
#-------------------------------------------------------------------------------
%package -n python2-%{name}
Summary:       Python 2 bindings for XRootD
Group:         Development/Libraries
%if %{?fedora}%{!?fedora:0} >= 13
%{?python_provide:%python_provide python2-%{name}}
%else
Provides:      python-%{name}
%endif
Provides:      %{name}-python = %{epoch}:%{version}-%{release}
Obsoletes:     %{name}-python < 1:4.8.0-1
Requires:      %{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description -n python2-xrootd
Python 2 bindings for XRootD

#-------------------------------------------------------------------------------
# python3
#-------------------------------------------------------------------------------
%package -n python3-%{name}
Summary:       Python 3 bindings for XRootD
Group:         Development/Libraries
%if %{?fedora}%{!?fedora:0} >= 13
%{?python_provide:%python_provide python3-%{name}}
%endif
Requires:      %{name}-client-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description -n python3-xrootd
Python 3 bindings for XRootD

%package doc
Summary:	Developer documentation for the xrootd libraries
Group:		Documentation
BuildArch:	noarch

%description doc
This package contains the API documentation of the xrootd libraries.

%prep
%setup -n %{name}-%{version}%{?_alphasuffix}

%build
# Koji build machines at Wisc are unhappy when doing osg3.3 --el6 build
# https://github.com/xrootd/xrootd/issues/573
%ifarch i386                                                                                                                       
%global optflags %__global_cflags -m32 -march=i686 -mtune=atom -fasynchronous-unwind-tables                                        
%endif

mkdir build

pushd build
%cmake -DUSE_LIBC_SEMAPHORE:BOOL=%{use_libc_semaphore} ..
make %{?_smp_mflags}
#make -j1
popd

pushd packaging/common
make -f /usr/share/selinux/devel/Makefile
popd

doxygen Doxyfile

# build python3 bindings
pushd build/bindings/python
%py3_build
popd

%install

pushd build
make install DESTDIR=%{buildroot}
cat PYTHON_INSTALLED | sed -e "s|%{buildroot}||g" > PYTHON_INSTALLED_FILES
popd

# Service start-up scripts / unit files
%if %{use_systemd}
mkdir -p %{buildroot}%{_unitdir}
install -m 644 packaging/common/xrootd@.service %{buildroot}%{_unitdir}
install -m 644 packaging/common/cmsd@.service %{buildroot}%{_unitdir}
install -m 644 packaging/common/frm_xfrd@.service %{buildroot}%{_unitdir}
install -m 644 packaging/common/frm_purged@.service %{buildroot}%{_unitdir}
install -m 644 packaging/common/xrdhttp@.socket %{buildroot}%{_unitdir}
install -m 644 packaging/common/xrootd@.socket %{buildroot}%{_unitdir}

# tmpfiles.d
mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 packaging/rhel/xrootd.tmpfiles %{buildroot}%{_tmpfilesdir}/%{name}.conf

%else
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -p packaging/rhel/xrootd.init %{buildroot}%{_initrddir}/xrootd
install -p packaging/rhel/cmsd.init %{buildroot}%{_initrddir}/cmsd
install -p packaging/rhel/frm_purged.init %{buildroot}%{_initrddir}/frm_purged
install -p packaging/rhel/frm_xfrd.init %{buildroot}%{_initrddir}/frm_xfrd
install -p packaging/rhel/xrootd.functions %{buildroot}%{_initrddir}/xrootd.functions

sed s/%{name}.functions/%{name}-functions/ -i %{buildroot}%{_initrddir}/*
install -m 644 -p packaging/rhel/%{name}.functions \
    %{buildroot}%{_initrddir}/%{name}-functions
install -m 644 -p packaging/rhel/%{name}.sysconfig \
    %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%endif

# Server config
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -m 644 -p packaging/common/%{name}-clustered.cfg \
    %{buildroot}%{_sysconfdir}/%{name}/%{name}-clustered.cfg
install -m 644 -p packaging/common/%{name}-standalone.cfg \
    %{buildroot}%{_sysconfdir}/%{name}/%{name}-standalone.cfg
install -m 644 packaging/common/%{name}-filecache-clustered.cfg \
    %{buildroot}%{_sysconfdir}/%{name}/%{name}-filecache-clustered.cfg
install -m 644 packaging/common/%{name}-filecache-standalone.cfg \
    %{buildroot}%{_sysconfdir}/%{name}/%{name}-filecache-standalone.cfg
%if %{use_systemd}
install -m 644 packaging/common/%{name}-http.cfg %{buildroot}%{_sysconfdir}/%{name}/%{name}-http.cfg
%endif

# Client config
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/client.plugins.d
install -m 644 -p packaging/common/client.conf \
    %{buildroot}%{_sysconfdir}/%{name}/client.conf
install -m 644 -p packaging/common/client-plugin.conf.example \
    %{buildroot}%{_sysconfdir}/%{name}/client.plugins.d

chmod 644 %{buildroot}%{_datadir}/%{name}/utils/XrdCmsNotify.pm

sed 's!/usr/bin/env perl!/usr/bin/perl!' -i \
    %{buildroot}%{_datadir}/%{name}/utils/netchk \
    %{buildroot}%{_datadir}/%{name}/utils/XrdCmsNotify.pm \
    %{buildroot}%{_datadir}/%{name}/utils/XrdOlbMonPerf

%if %{?fedora}%{!?fedora:0} >= 22
rm %{buildroot}%{_libdir}/libXrdCephPosix.so
%endif

chmod 755 %{buildroot}%{python_sitearch}/pyxrootd/client.so

mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
mkdir -p %{buildroot}%{_localstatedir}/run/%{name}
mkdir -p %{buildroot}%{_localstatedir}/spool/%{name}

mkdir %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 -p packaging/common/%{name}.logrotate \
    %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

mkdir -p %{buildroot}%{_datadir}/selinux/packages/%{name}
install -m 644 -p packaging/common/%{name}.pp \
    %{buildroot}%{_datadir}/selinux/packages/%{name}

# install python3 bindings
pushd build/bindings/python
%py3_install
popd

# Documentation
mkdir -p %{buildroot}%{_pkgdocdir}
cp -pr doxydoc/html %{buildroot}%{_pkgdocdir}

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post client-libs -p /sbin/ldconfig
%postun client-libs -p /sbin/ldconfig

%post server-libs -p /sbin/ldconfig
%postun server-libs -p /sbin/ldconfig

%if %{?fedora}%{!?fedora:0} >= 22
%post ceph -p /sbin/ldconfig
%postun ceph -p /sbin/ldconfig
%endif

%pre server
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
	useradd -r -g %{name} -c "XRootD runtime user" \
	-s /sbin/nologin -d %{_localstatedir}/spool/%{name} %{name}

# Remove obsolete service
/sbin/service olbd stop >/dev/null 2>&1 || :
/sbin/chkconfig --del olbd >/dev/null 2>&1 || :

%if %{use_systemd}
# Remove old init config when systemd is used
/sbin/service xrootd stop >/dev/null 2>&1 || :
/sbin/service cmsd stop >/dev/null 2>&1 || :
/sbin/service frm_purged stop >/dev/null 2>&1 || :
/sbin/service frm_xfrd stop >/dev/null 2>&1 || :
/sbin/chkconfig --del xrootd >/dev/null 2>&1 || :
/sbin/chkconfig --del cmsd >/dev/null 2>&1 || :
/sbin/chkconfig --del frm_purged >/dev/null 2>&1 || :
/sbin/chkconfig --del frm_xfrd >/dev/null 2>&1 || :
%endif

%if %{use_systemd}

%post server
if [ $1 -eq 1 ] ; then
    systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun server
if [ $1 -eq 0 ] ; then
    for DAEMON in xrootd cmsd frm_purged frm xfrd; do
	for INSTANCE in `systemctl | grep $DAEMON@ | awk '{print $1;}'`; do
	    systemctl --no-reload disable $INSTANCE > /dev/null 2>&1 || :
	    systemctl stop $INSTANCE > /dev/null 2>&1 || :
	done
    done
fi

%postun server
if [ $1 -ge 1 ] ; then
    systemctl daemon-reload >/dev/null 2>&1 || :
    for DAEMON in xrootd cmsd frm_purged frm xfrd; do
	for INSTANCE in `systemctl | grep $DAEMON@ | awk '{print $1;}'`; do
	    systemctl try-restart $INSTANCE >/dev/null 2>&1 || :
	done
    done
fi

%else

%post server
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add xrootd
    /sbin/chkconfig --add cmsd
    /sbin/chkconfig --add frm_purged
    /sbin/chkconfig --add frm_xfrd
fi

%preun server
if [ $1 -eq 0 ]; then
    /sbin/service xrootd stop >/dev/null 2>&1 || :
    /sbin/service cmsd stop >/dev/null 2>&1 || :
    /sbin/service frm_purged stop >/dev/null 2>&1 || :
    /sbin/service frm_xfrd stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del xrootd
    /sbin/chkconfig --del cmsd
    /sbin/chkconfig --del frm_purged
    /sbin/chkconfig --del frm_xfrd
fi

%postun server
if [ $1 -ge 1 ]; then
    /sbin/service xrootd condrestart >/dev/null 2>&1 || :
    /sbin/service cmsd condrestart >/dev/null 2>&1 || :
    /sbin/service frm_purged condrestart >/dev/null 2>&1 || :
    /sbin/service frm_xfrd condrestart >/dev/null 2>&1 || :
fi

%endif

%post selinux
/usr/sbin/semodule -i %{_datadir}/selinux/packages/%{name}/%{name}.pp >/dev/null 2>&1 || :

%postun selinux
if [ $1 -eq 0 ] ; then
    /usr/sbin/semodule -r %{name} >/dev/null 2>&1 || :
fi

%files
# Empty

%files server
%{_bindir}/cconfig
%{_bindir}/cmsd
%{_bindir}/cns_ssi
%{_bindir}/frm_admin
%{_bindir}/frm_purged
%{_bindir}/frm_xfragent
%{_bindir}/frm_xfrd
%{_bindir}/mpxstats
%{_bindir}/wait41
%{_bindir}/XrdCnsd
%{_bindir}/xrdmapc
%{_bindir}/xrdpfc_print
%{_bindir}/xrdacctest
%{_bindir}/xrdpwdadmin
%{_bindir}/xrdsssadmin
%{_bindir}/xrootd
%{_mandir}/man8/cmsd.8*
%{_mandir}/man8/cns_ssi.8*
%{_mandir}/man8/frm_admin.8*
%{_mandir}/man8/frm_purged.8*
%{_mandir}/man8/frm_xfragent.8*
%{_mandir}/man8/frm_xfrd.8*
%{_mandir}/man8/mpxstats.8*
%{_mandir}/man8/XrdCnsd.8*
%{_mandir}/man8/xrdpfc_print.8*
%{_mandir}/man8/xrdpwdadmin.8*
%{_mandir}/man8/xrdsssadmin.8*
%{_mandir}/man8/xrootd.8*
%{_datadir}/%{name}
%if %{use_systemd}
%{_unitdir}/*
%{_tmpfilesdir}/%{name}.conf
%else
%{_initrddir}/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%endif
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(-,xrootd,xrootd) %config(noreplace) %{_sysconfdir}/%{name}/*.cfg
%attr(-,xrootd,xrootd) %{_localstatedir}/log/%{name}
%attr(-,xrootd,xrootd) %{_localstatedir}/run/%{name}
%attr(-,xrootd,xrootd) %{_localstatedir}/spool/%{name}

%files selinux
%{_datadir}/selinux/packages/%{name}/%{name}.pp

%files libs
%{_libdir}/libXrdAppUtils.so.*
%{_libdir}/libXrdCrypto.so.*
%{_libdir}/libXrdCryptoLite.so.*
%{_libdir}/libXrdUtils.so.*
%{_libdir}/libXrdXml.so.*
# Plugins
%{_libdir}/libXrdCks*-4.so
%{_libdir}/libXrdCryptossl-4.so
%{_libdir}/libXrdSec*-4.so
%{_libdir}/libXrdClProxyPlugin-4.so
%doc COPYING* LICENSE

%files devel
%{_bindir}/xrootd-config
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/XProtocol
%{_includedir}/%{name}/Xrd
%{_includedir}/%{name}/XrdCks
%{_includedir}/%{name}/XrdNet
%{_includedir}/%{name}/XrdOuc
%{_includedir}/%{name}/XrdSec
%{_includedir}/%{name}/XrdSys
%{_includedir}/%{name}/XrdVersion.hh
%{_includedir}/%{name}/XrdXml/XrdXmlReader.hh
%{_libdir}/libXrdAppUtils.so
%{_libdir}/libXrdCrypto.so
%{_libdir}/libXrdCryptoLite.so
%{_libdir}/libXrdUtils.so
%{_libdir}/libXrdXml.so

%files client-libs
%{_libdir}/libXrdCl.so.*
%{_libdir}/libXrdClient.so.*
%{_libdir}/libXrdFfs.so.*
%{_libdir}/libXrdPosix.so.*
%{_libdir}/libXrdPosixPreload.so.*
# This lib may be used for LD_PRELOAD so the .so link needs to be included
%{_libdir}/libXrdPosixPreload.so
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/client.conf
%dir %{_sysconfdir}/%{name}/client.plugins.d
%config(noreplace) %{_sysconfdir}/%{name}/client.plugins.d/client-plugin.conf.example

%files client-devel
%{_bindir}/xrdgsitest
%{_includedir}/%{name}/XrdCl
%{_includedir}/%{name}/XrdClient
%{_includedir}/%{name}/XrdPosix
%{_libdir}/libXrdCl.so
%{_libdir}/libXrdClient.so
%{_libdir}/libXrdFfs.so
%{_libdir}/libXrdPosix.so
%{_mandir}/man1/xrdgsitest.1*

%files server-libs
%{_libdir}/libXrdServer.so.*
# Plugins
%{_libdir}/libXrdBlacklistDecision-4.so
%{_libdir}/libXrdBwm-4.so
%{_libdir}/libXrdFileCache-4.so
%{_libdir}/libXrdHttp-4.so
%{_libdir}/libXrdOssSIgpfsT-4.so
%{_libdir}/libXrdPss-4.so
%{_libdir}/libXrdThrottle-4.so
%{_libdir}/libXrdXrootd-4.so
%{_libdir}/libXrdN2No2p-4.so
%{_libdir}/libXrdSsi-4.so
%{_libdir}/libXrdSsiLib.so.*
%{_libdir}/libXrdSsiLog-4.so
%{_libdir}/libXrdSsiShMap.so.*

%files server-devel
%{_includedir}/%{name}/XrdAcc
%{_includedir}/%{name}/XrdCms
%{_includedir}/%{name}/XrdFileCache
%{_includedir}/%{name}/XrdOss
%{_includedir}/%{name}/XrdSfs
%{_includedir}/%{name}/XrdXrootd
%{_includedir}/%{name}/XrdHttp
%{_libdir}/libXrdServer.so

%files private-devel
%{_includedir}/%{name}/private
%{_libdir}/libXrdSsiLib.so
%{_libdir}/libXrdSsiShMap.so

%files client
%{_bindir}/xprep
%{_bindir}/xrd
%{_bindir}/xrdadler32
%{_bindir}/xrdcopy
%{_bindir}/xrdcp
%{_bindir}/xrdcp-old
%{_bindir}/xrdfs
%{_bindir}/xrdgsiproxy
%{_bindir}/xrdstagetool
%{_mandir}/man1/xprep.1*
%{_mandir}/man1/xrd.1*
%{_mandir}/man1/xrdadler32.1*
%{_mandir}/man1/xrdcopy.1*
%{_mandir}/man1/xrdcp.1*
%{_mandir}/man1/xrdcp-old.1*
%{_mandir}/man1/xrdfs.1*
%{_mandir}/man1/xrdgsiproxy.1*
%{_mandir}/man1/xrdstagetool.1*

%files fuse
%{_bindir}/xrootdfs
%{_mandir}/man1/xrootdfs.1*

%if %{?fedora}%{!?fedora:0} >= 22
%files ceph
%{_libdir}/libXrdCeph-4.so
%{_libdir}/libXrdCephXattr-4.so
%{_libdir}/libXrdCephPosix.so.*
%endif

%files -n python2-%{name} -f build/PYTHON_INSTALLED_FILES
%defattr(-,root,root,-)
%{python2_sitearch}/*

%files -n python3-%{name}
%defattr(-,root,root,-)
%{python3_sitearch}/*

%files doc
%doc %{_pkgdocdir}

%changelog
* Fri Apr 06 2018 Marian Zvada <marian.zvada@cern.ch> - 1:4.8.2-0.2.e341f47
- special request from Derek create build from current master, EL7 OSG3.4

* Tue Mar 20 2018 Marian Zvada <marian.zvada@cern.ch> - 1:4.8.2-0.1.rc3
- update to RC3, includes patch from previous build
- SOFTWARE-3173

* Fri Mar 09 2018 Marian Zvada <marian.zvada@cern.ch> - 1:4.8.2-0.1.rc1
- using patch requested by BrianB along rc1 candidate
- https://github.com/xrootd/xrootd/pull/664
- SOFTWARE-3173

* Fri Feb 16 2018 Marian Zvada <marian.zvada@cern.ch> - 1:4.8.0-2
- backport fix to OSG33 for tmpfile creation according to SOFTWARE-3114

* Thu Feb 01 2018 Marian Zvada <marian.zvada@cern.ch> - 1:4.8.1-1
- Update to 4.8.1 (SOFTWARE-3104)
- tmpfile creation fix for RHEL7 (SOFTWARE-3114)

* Thu Dec 14 2017 Marian Zvada <marian.zvada@cern.ch> - 1:4.8.0-1
- Update to 4.8.0 (SOFTWARE-3033)
- clean up EL5-specific conditional according to SOFTWARE-3050

* Fri Dec 01 2017 Marian Zvada <marian.zvada@cern.ch> - 1:4.8.0-0.1.rc1
- Update to 4.8.0-rc1 (SOFTWARE-3033)
- Add python3 sub-package; Rename python sub-package

* Wed Nov 01 2017 Mátyás Selmeci <matyas@cs.wisc.edu> - 1:4.7.1-1
- Update to 4.7.1 (SOFTWARE-2933)

* Mon Oct 30 2017 Marian Zvada <marian.zvada@cern.ch> - 1:4.7.1-0.1.rc3
- Update to 4.7.1.rc3 SOFTWARE-2933

* Mon Oct 23 2017 Marian Zvada <marian.zvada@cern.ch> - 1:4.7.1-0.1.rc2
- patch for ignore -Wunused-result included
- Update to 4.7.1.rc2 SOFTWARE-2933

* Tue Aug 22 2017 Marian Zvada <marian.zvada@cern.ch> - 1:4.7.0-1
- Update to 4.7.0 SOFTWARE-2874

* Fri May 12 2017 Marian Zvada <marian.zvada@cern.ch> - 1:4.6.1-1
- Update to 4.6.1 SOFTWARE-2669
- includes rc3

* Mon Apr 24 2017 Marian Zvada <marian.zvada@cern.ch> - 1:4.6.1-0.2.rc3
- Bumped to rc3; Update to 4.6.1.rc2 SOFTWARE-2669

* Fri Apr 21 2017 Marian Zvada <marian.zvada@cern.ch> - 1:4.6.1-0.1.rc2
- Update to 4.6.1.rc2 SOFTWARE-2669

* Thu Feb 9 2017 Edgar Fajardo <emfajard@ucsd.edu> - 1:4.6.0-1
- Update to 4.6.0 SOFTWARE-2597
- File caching proxy V2
- Add non-blocking sends to avoid slow links

* Tue Dec 20 2016 Edgar Fajardo <emfajard@ucsd.edu> - 1:4.5.0-2
- Updated Changelog SOFTWARE-2549

* Thu Dec 15 2016 Edgar Fajardo <emfajard@ucsd.edu> - 1:4.5.0-1
- Update to 4.5.0 SOFTWARE-2549
- Allow specifying a different timeout for null cached entries
- Implement request signing
- Add ZIP extracting capability to xrdcp
- Include the release number in client Login request cgi.
- Add support for spaces in file names for mv operation.

* Fri Jul 29 2016 Mattias Ellert <mattias.ellert@physics.uu.se> - 1:4.4.0-1
- Update to version 4.4.0
- Drop patch xrootd-deprecated.patch

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.3.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Apr 21 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.3.0-3
- Backport upstream's fix for the deprecation of readdir_r

* Sat Feb 27 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.3.0-2
- Workaround deprecation of readdir_r in glibc 2.24

* Fri Feb 26 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.3.0-1
- Update to version 4.3.0
- Drop patches accected upstream or that were previously backported:
  xrootd-selinux.patch, xrootd-pth-cancel.patch, xrootd-link.patch,
  xrootd-c++11.patch, xrootd-doxygen.patch, xrootd-autoptr.patch,
  xrootd-indent.patch, xrootd-throw-dtor.patch and xrootd-sockaddr.patch

* Wed Feb 17 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.2.3-6
- Fix strict aliasing issues with struct sockaddr

* Fri Feb 12 2016 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.2.3-5
- Use upstream's patch for the pthread segfault
- Backport fixes for gcc 6 from upstream

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 23 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.2.3-3
- Fix for c++11 usage in ceph (backport from upstream git)
- Doxygen fixes

* Wed Dec 23 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.2.3-2
- Fix segfault due to pthread clean-up functions

* Tue Sep 08 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.2.3-1
- Update to version 4.2.3

* Fri Jul 31 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.2.2-1
- Update to version 4.2.2
- Drop patch xrootd-narrowing.patch (accepted upstream)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 02 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.2.1-2
- Fix narrowing conversion error on ppc64 (EPEL 7)

* Tue Jun 02 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.2.1-1
- Update to version 4.2.1
- New subpackages ceph (F22+) and python

* Fri Apr 17 2015 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.1.1-2
- Rebuilt for gcc C++ ABI change

* Mon Dec 08 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.1.1-1
- Update to version 4.1.1
- Drop patch xrootd-signed-char.patch (accepted upstream)

* Fri Nov 28 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.1.0-1
- Update to version 4.1.0
- Install systemd unit files (F21+, EPEL7+)

* Sat Nov 01 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.0.4-1
- Update to version 4.0.4

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 08 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.0.3-1
- Update to version 4.0.3

* Fri Jul 11 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.0.1-1
- Update to version 4.0.1
- Split main package into server and selinux
- New main package installs server and selinux
- Drop patches accepted upstream (-32bit, -range, -narrowing)

* Sun Jun 29 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:4.0.0-1
- Update to version 4.0.0
- Remove the perl package - no longer part of upstream sources

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 30 2014 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.3.6-1
- Update to version 3.3.6

* Tue Dec 03 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.3.5-1
- Update to version 3.3.5

* Tue Nov 19 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.3.4-1
- Update to version 3.3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.3.3-1
- Update to version 3.3.3
- Change License tag to LGPLv3+ due to upstream license change

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1:3.3.2-2
- Perl 5.18 rebuild

* Sun Apr 28 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.3.2-1
- Update to version 3.3.2

* Wed Mar 06 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.3.1-1
- Update to version 3.3.1
- Remove the java package - no longer part of upstream sources
- Drop patches fixed upstream: xrootd-cryptoload.patch, xrootd-init.patch and
  xrootd-perl.patch
- Drop obsolete patch: xrootd-java.patch
- Add private-devel package for deprecated header files

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.2.7-1
- Update to version 3.2.7
- Split libs package into libs, client-libs and server-libs
- Split devel package into devel, client-devel and server-devel

* Fri Oct 12 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.2.5-1
- Update to version 3.2.5

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.2.2-1
- Update to version 3.2.2

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1:3.2.1-2
- Perl 5.16 rebuild

* Thu May 17 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.2.1-1
- Update to version 3.2.1

* Sat Mar 17 2012 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.1.1-1
- Update to version 3.1.1

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.5-3
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 05 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.5-1
- Update to version 3.0.5

* Mon Jul 18 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.4-2.1
- Rebuild for new gridsite (EPEL 5 only)

* Tue Jun 28 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.4-2
- Add missing BuildRequires ncurses-devel

* Tue Jun 28 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.4-1.1
- Remove xrootdfs man page on EPEL 4

* Mon Jun 27 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.4-1
- Update to version 3.0.4
- Drop patches fixed upstream: xrootd-man.patch, xrootd-rhel5-no-atomic.patch
- Drop the remaining man-pages copied from root - now provided by upstream

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:3.0.3-3
- Perl mass rebuild

* Mon May 02 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.3-2
- Proper fix for the atomic detection on ppc - no bug in gcc after all

* Sun Apr 24 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.3-1.1
- Workaround for broken gcc on RHEL5 ppc (rhbz #699149)

* Fri Apr 22 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.3-1
- Update to version 3.0.3
- Use upstream's manpages where available (new in this release)
- Use upstream's start-up scripts (new in this release)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 30 2011 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.2-1
- Update to version 3.0.2
- Patch XrdCms makefile to make the Xmi interface public

* Fri Dec 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.0-2
- Rebuilt for updated gridsite package

* Mon Dec 13 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 1:3.0.0-1
- Update to version 3.0.0
- New subpackage - xrootd-fuse
- New version scheme inroduced by upstream - add epoch

* Wed Sep 01 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 20100315-5
- Disable threads in doxygen - causes memory corruption on ppc

* Wed Sep 01 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 20100315-4
- Add startup scripts for cmsd service that replaces the deprecated
  olbd service

* Fri Jul 09 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 20100315-3
- Fix broken jar

* Mon Jun 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 20100315-2
- Add LGPLv2+ to License tag due to man pages
- Better package description

* Wed Jun 09 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 20100315-1
- Initial packaging
