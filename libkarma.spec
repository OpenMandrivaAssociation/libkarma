%define major	0
%define libname %mklibname karma %{major}
%define devname %mklibname karma -d

Summary:	Rio Karma tools
Name:		libkarma
Version:	0.1.2
Release:	10
License:	GPLv2+
Group:		System/Libraries
Url:		http://www.freakysoft.de/libkarma/
Source0:	http://www.freakysoft.de/libkarma/%{name}-%{version}.tar.gz
Source2:	http://bobcopeland.com/karma/banshee/preferences.fdi
Source3:	http://bobcopeland.com/karma/banshee/multimedia-player-rio-karma.png
Source4:	karma-sharp.dll.config
Source100:	libkarma.rpmlintrc

BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(mono)
BuildRequires:	pkgconfig(taglib)
BuildRequires:	pkgconfig(zlib)
Requires:	%{libname} = %{version}-%{release}

%description
Rio Karma access library

%package -n %{libname}
Summary:	Rio Karma access library
Group:		System/Libraries

%description -n %{libname}
Rio Karma access library

%package -n %{devname}
Summary:	Rio Karma development files
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}karma0-devel < 0.1.2-5

%description -n %{devname}
Rio Karma development files

%package -n karma-sharp
Summary:	Rio Karma C Sharp bindings
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description -n karma-sharp
Rio Karma C Sharp bindings

%prep
%setup -q

%build
make PREFIX=%{buildroot}/%{_prefix} CC="%__cc"

%install
rm -rf %{buildroot} installed-docs
mkdir -p %{buildroot}
make install PREFIX=%{buildroot}/%{_prefix} CHOWNPROG=/bin/true CHGRPPROG=/bin/true CC="%__cc"
sed -i -e "s^%{buildroot}^^" %{buildroot}%{_prefix}/lib/pkgconfig/karma-sharp.pc
%if %_lib != lib
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
sed -i -e "s^/lib^/%_lib^" %{buildroot}%{_libdir}/pkgconfig/karma-sharp.pc
%endif

install -m 644 -D libkarma.fdi %{buildroot}%{_sysconfdir}/hal/fdi/information/20-rio-karma.fdi
install -m 644 -D %SOURCE2 %{buildroot}%{_sysconfdir}/hal/fdi/policy/preferences.fdi
install -m 644 -D %SOURCE3 %{buildroot}%{_datadir}/icons/hicolor/32x32/devices/multimedia-player-rio-karma.png

cat > README.urpmi << EOF
For automatic mounting, add the following line to your
/etc/fstab. Otherwise gnome-volume-manager will refuse to mount the
device, as it doesn't know about the Karma's proprietary filesystem.

/dev/disk/by-id/usb-Rio_Rio_Karma_0000000000000000-part2    /media/karma    omfs    user,noauto    0   0

EOF

install -m 644 %SOURCE4 %{buildroot}%{_libdir}/karma-sharp/karma-sharp.dll.config

# Drop double slash
sed -i 's%//usr%/usr%' %{buildroot}%{_libdir}/pkgconfig/karma-sharp.pc

# Workaround for chprop, riocp and karma_helper all getting the same build-id
%__strip %{buildroot}%{_bindir}/riocp %{buildroot}%{_bindir}/chprop

rm -f %{buildroot}%{_libdir}/libkarma.a

%files
%doc THANKS TODO README.urpmi
%config(noreplace) %{_sysconfdir}/hal/fdi/information/20-rio-karma.fdi
%config(noreplace) %{_sysconfdir}/hal/fdi/policy/preferences.fdi
%{_bindir}/riocp
%{_bindir}/chprop
%attr(4755,root,root) %{_bindir}/karma_helper
%{_datadir}/icons/hicolor/32x32/devices/multimedia-player-rio-karma.png
%{_mandir}/man1/*.1*

%files -n %{libname}
%{_libdir}/libkarma.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/libkarma.so

%files -n karma-sharp
%{_libdir}/karma-sharp/*
%{_libdir}/pkgconfig/karma-sharp.pc

