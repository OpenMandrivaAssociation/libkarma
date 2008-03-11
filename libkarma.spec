%define major 0
%define libname %mklibname karma %major

Summary:   	Rio Karma tools
Name:      	libkarma
Version:   	0.1.0
Release:   	%mkrel 2
License:   	GPL
Group:     	System/Libraries
Url:	   	http://www.freakysoft.de/html/libkarma/
Source:   	http://www.freakysoft.de/html/libkarma/libkarma-%{version}.tar.bz2
Source1: http://bobcopeland.com/karma/banshee/20-rio-karma.fdi
Source2: http://bobcopeland.com/karma/banshee/preferences.fdi
Source3: http://bobcopeland.com/karma/banshee/multimedia-player-rio-karma.png
Source4: karma-sharp.dll.config
BuildRoot: 	%{_tmppath}/%name-root
BuildRequires: mono-devel
BuildRequires: taglib-devel
BuildRequires: libusb-devel
BuildRequires: zlib-devel
Requires: dkms-omfs
Requires: %libname >= %version
%define _requires_exceptions libkarma

%description
Rio Karma access library

%package -n %libname
Summary: Rio Karma access library
Group: System/Libraries

%description -n %libname
Rio Karma access library


%package -n %libname-devel
Summary:   	Rio Karma development files
Group:     	Development/C
Requires: %libname = %version
Provides: %name-devel = %version-%release
Obsoletes: %name-devel

%description -n %libname-devel
Rio Karma development files


%package -n karma-sharp
Summary:   	Rio Karma C# bindings
Group:     	Development/Other
Requires: %name = %version

%description -n karma-sharp
Rio Karma C# bindings


%prep
%setup -q -n libkarma-%{version}

%build
make PREFIX=$RPM_BUILD_ROOT/%_prefix

%install
rm -rf $RPM_BUILD_ROOT installed-docs
mkdir -p $RPM_BUILD_ROOT
make install PREFIX=$RPM_BUILD_ROOT/%_prefix CHOWNPROG=/bin/true CHGRPPROG=/bin/true
perl -pi -e "s^%buildroot^^" %buildroot%_prefix/lib/pkgconfig/karma-sharp.pc
%if %_lib != lib
mv %buildroot%_prefix/lib %buildroot%_libdir
perl -pi -e "s^/lib^/%_lib^" %buildroot%_libdir/pkgconfig/karma-sharp.pc
%endif


install -m 644 -D %SOURCE1 %buildroot%_sysconfdir/hal/fdi/information/20-rio-karma.fdi
install -m 644 -D %SOURCE2 %buildroot%_sysconfdir/hal/fdi/policy/preferences.fdi
install -m 644 -D %SOURCE3 %buildroot%_datadir/icons/hicolor/32x32/devices/multimedia-player-rio-karma.png

cat > README.urpmi << EOF
For automatic mounting, add the following line to your
/etc/fstab. Otherwise gnome-volume-manager will refuse to mount the
device, as it doesn't know about the Karma's proprietary filesystem.

/dev/disk/by-id/usb-Rio_Rio_Karma_0000000000000000-part2    /media/karma    omfs    user,noauto    0   0

EOF

install -m 644 %SOURCE4 %buildroot%_libdir/karma-sharp/karma-sharp.dll.config

mv %buildroot%_datadir/doc/libkarma installed-docs

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%post
%update_icon_cache hicolor
%postun
%clean_icon_cache hicolor

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc installed-docs/* README.urpmi
%config(noreplace) %_sysconfdir/hal/fdi/information/20-rio-karma.fdi
%config(noreplace) %_sysconfdir/hal/fdi/policy/preferences.fdi
%_bindir/riocp
%_bindir/chprop
%_mandir/man1/*.1*
%attr(4755,root,root) %_bindir/karma_helper
%_datadir/icons/hicolor/32x32/devices/multimedia-player-rio-karma.png

%files -n %libname
%defattr(-,root,root)
%_libdir/libkarma.so.%{major}*

%files -n %libname-devel
%defattr(-,root,root)
%_includedir/*
%_libdir/libkarma.a
%_libdir/libkarma.so

%files -n karma-sharp
%defattr(-,root,root)
%_libdir/karma-sharp/*
%_libdir/pkgconfig/karma-sharp.pc


