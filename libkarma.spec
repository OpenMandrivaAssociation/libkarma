Summary:   	Rio Karma tools
Name:      	libkarma
Version:   	0.0.6
Release:   	%mkrel 1
License:   	GPL
Group:     	System/Libraries
Url:	   	http://linux-karma.sourceforge.net/
Source:   	http://downloads.sourceforge.net/linux-karma/libkarma-%{version}.tar.bz2
Source1: http://bobcopeland.com/karma/banshee/20-rio-karma.fdi
Source2: http://bobcopeland.com/karma/banshee/preferences.fdi
Source3: http://bobcopeland.com/karma/banshee/multimedia-player-rio-karma.png
BuildRoot: 	%{_tmppath}/%name-root
BuildRequires: mono-devel
BuildRequires: taglib-devel
BuildRequires: libusb-devel
Requires: dkms-omfs

%description
Rio Karma access library

%package devel
Summary:   	Rio Karma tools
Group:     	Development/C

%description devel
Rio Karma tools


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
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make install PREFIX=$RPM_BUILD_ROOT/%_prefix
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

%post
%update_icon_cache hicolor
%postun
%clean_icon_cache hicolor

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ChangeLog COPYING INSTALL THANKS TODO README.urpmi
%config(noreplace) %_sysconfdir/hal/fdi/information/20-rio-karma.fdi
%config(noreplace) %_sysconfdir/hal/fdi/policy/preferences.fdi
%_bindir/riocp
%_bindir/chprop
%_bindir/playlist_show
%_libdir/libkarma.so
%attr(4755,root,root) %_bindir/karma_helper
%_datadir/icons/hicolor/32x32/devices/multimedia-player-rio-karma.png

%files devel
%defattr(-,root,root)
%_includedir/*
%_libdir/libkarma.a

%files -n karma-sharp
%defattr(-,root,root)
%_libdir/karma-sharp/*
%_libdir/pkgconfig/karma-sharp.pc


