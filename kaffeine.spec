%bcond clang 1
%bcond xcb 1
%bcond gstreamer 1
%bcond xine 1
%bcond dvb 1
%bcond lame 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 3

%define tde_pkg kaffeine
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		0.8.8
Release:		%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:		Xine-based media player
Group:			Applications/Multimedia
URL:			http://kaffeine.sourceforge.net/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/multimedia/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz
Source1:		%{name}-rpmlintrc

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_prefix}/include/tde
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DWITH_ALL_OPTIONS=ON -DBUILD_ALL=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}
BuildOption:    -DWITH_DVB=%{?!with_dvb:OFF}%{?with_dvb:ON}
BuildOption:    -DWITH_LAME=%{?!with_lame:OFF}%{?with_lame:ON}
BuildOption:    -DWITH_XCB=%{?!with_xcb:OFF}%{?with_xcb:ON}

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	gettext

BuildRequires:	trinity-tde-cmake >= %{tde_version}

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig

# VORBIS support
BuildRequires:  pkgconfig(vorbis)

# CDDA support
BuildRequires:	pkgconfig(libcdio)
BuildRequires:	%{_lib}cdda-devel
BuildRequires:  pkgconfig(libcdio_cdda)

# X11 stuff
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xinerama)

# XCB support
%{?with_xcb:BuildRequires:  pkgconfig(xcb)}

# GSTREAMER support
%if %{with gstreamer}
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
%endif

# XINE support
%{?with_xine:BuildRequires:  pkgconfig(libxine)}

# LAME support
%{?with_lame:BuildRequires:  pkgconfig(lame)}

# WTF support
BuildRequires:	kernel-headers

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)

Requires: %{name}-libs = %{?epoch:%{epoch}:}%{version}-%{release}

%description
Kaffeine is a xine-based media player for TDE.  It plays back CDs,
and VCDs, and can decode all (local or streamed) multimedia formats 
supported by xine-lib.
Additionally, Kaffeine is fully integrated in TDE, it supports drag
and drop and provides an editable playlist, a bookmark system, a
Konqueror plugin, OSD and much more.

%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README.md TODO
%{tde_prefix}/bin/kaffeine
%{tde_prefix}/%{_lib}/libkaffeinepart.so
%{tde_prefix}/%{_lib}/trinity/lib*.*
%{tde_prefix}/share/appl*/*/*.desktop
%if %{with gstreamer}
%{tde_prefix}/share/apps/gstreamerpart/
%endif
%{tde_prefix}/share/apps/kaffeine/
%{tde_prefix}/share/apps/konqueror/servicemenus/*.desktop
%{tde_prefix}/share/apps/profiles/
%{tde_prefix}/share/icons/hicolor/*/*/*
%{tde_prefix}/share/mimelnk/*/*.desktop
%{tde_prefix}/share/service*/*.desktop
%{tde_prefix}/share/doc/tde/HTML/en/kaffeine/
%{tde_prefix}/share/man/man1/kaffeine.1*

##########

%package devel
Summary:		Development files for %{name}
Group:			Development/Libraries
Requires:		%{name}-libs = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		trinity-tdelibs-devel

%description devel
%{summary}.

%files devel
%defattr(-,root,root,-)
%{tde_prefix}/include/tde/kaffeine/
%{tde_prefix}/%{_lib}/lib*.so
%exclude %{tde_prefix}/%{_lib}/libkaffeinepart.so

##########

%package libs
Summary:		%{name} runtime libraries
Group:			System Environment/Libraries

# include to be paranoid, installing libs-only is still mostly untested -- Rex
Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libs
%{summary}.

%files libs
%defattr(-,root,root,-)
%{tde_prefix}/%{_lib}/lib*.so.*

%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"


%install -a
## File lists
# locale's
%find_lang %{tde_pkg}

# Unpackaged files
rm -f %{buildroot}/%{tde_prefix}/%{_lib}/lib*.la
rm -f %{buildroot}/%{tde_prefix}/share/mimelnk/application/x-mplayer2.desktop

