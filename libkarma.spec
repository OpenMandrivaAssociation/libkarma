%define major 0
%define libname %mklibname karma %major

Summary:   	Rio Karma tools
Name:      	libkarma
Version:   	0.1.2
Release:   	4
License:   	GPLv2+
Group:     	System/Libraries
Url:	   	http://www.freakysoft.de/libkarma/
Source0:   	http://www.freakysoft.de/libkarma/libkarma-%{version}.tar.gz
Source2:	http://bobcopeland.com/karma/banshee/preferences.fdi
Source3:	http://bobcopeland.com/karma/banshee/multimedia-player-rio-karma.png
Source4:	karma-sharp.dll.config
Source100:	%name.rpmlintrc
BuildRequires:	mono-devel
BuildRequires:	taglib-devel
BuildRequires:	libusb-devel
BuildRequires:	zlib-devel
Requires:	%libname = %version-%release

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
Requires:	%libname = %version-%release
Provides:	%name-devel = %{EVRD}

%description -n %libname-devel
Rio Karma development files


%package -n karma-sharp
Summary:   	Rio Karma C# bindings
Group:     	Development/Other
Requires:	%name = %version-%release

%description -n karma-sharp
Rio Karma C# bindings


%prep
%setup -q -n libkarma-%{version}

%build
make PREFIX=%{buildroot}/%_prefix CC="%__cc"

%install
rm -rf %{buildroot} installed-docs
mkdir -p %{buildroot}
make install PREFIX=%{buildroot}/%_prefix CHOWNPROG=/bin/true CHGRPPROG=/bin/true CC="%__cc"
perl -pi -e "s^%buildroot^^" %buildroot%_prefix/lib/pkgconfig/karma-sharp.pc
%if %_lib != lib
mv %buildroot%_prefix/lib %buildroot%_libdir
perl -pi -e "s^/lib^/%_lib^" %buildroot%_libdir/pkgconfig/karma-sharp.pc
%endif


install -m 644 -D libkarma.fdi %buildroot%_sysconfdir/hal/fdi/information/20-rio-karma.fdi
install -m 644 -D %SOURCE2 %buildroot%_sysconfdir/hal/fdi/policy/preferences.fdi
install -m 644 -D %SOURCE3 %buildroot%_datadir/icons/hicolor/32x32/devices/multimedia-player-rio-karma.png

cat > README.urpmi << EOF
For automatic mounting, add the following line to your
/etc/fstab. Otherwise gnome-volume-manager will refuse to mount the
device, as it doesn't know about the Karma's proprietary filesystem.

/dev/disk/by-id/usb-Rio_Rio_Karma_0000000000000000-part2    /media/karma    omfs    user,noauto    0   0

EOF

install -m 644 %SOURCE4 %buildroot%_libdir/karma-sharp/karma-sharp.dll.config

# Drop double slash
sed -i 's%//usr%/usr%' %buildroot%_libdir/pkgconfig/karma-sharp.pc

# Workaround for chprop, riocp and karma_helper all getting the same build-id
%__strip %buildroot%_bindir/riocp %buildroot%_bindir/chprop

%files
%doc THANKS TODO README.urpmi
%config(noreplace) %_sysconfdir/hal/fdi/information/20-rio-karma.fdi
%config(noreplace) %_sysconfdir/hal/fdi/policy/preferences.fdi
%_bindir/riocp
%_bindir/chprop
%_mandir/man1/*.1*
%attr(4755,root,root) %_bindir/karma_helper
%_datadir/icons/hicolor/32x32/devices/multimedia-player-rio-karma.png

%files -n %libname
%_libdir/libkarma.so.%{major}*

%files -n %libname-devel
%_includedir/*
%_libdir/libkarma.a
%_libdir/libkarma.so

%files -n karma-sharp
%_libdir/karma-sharp/*
%_libdir/pkgconfig/karma-sharp.pc




%changelog
* Sat Apr 23 2011 Götz Waschk <waschk@mandriva.org> 0.1.2-1mdv2011.0
+ Revision: 657324
- update to new version 0.1.2

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-2mdv2011.0
+ Revision: 520874
- rebuilt for 2010.1

* Mon Jun 08 2009 Götz Waschk <waschk@mandriva.org> 0.1.1-1mdv2010.0
+ Revision: 383902
- new version
- use upstream fdi file

* Fri May 15 2009 Götz Waschk <waschk@mandriva.org> 0.1.0-5mdv2010.0
+ Revision: 376115
- update license
- drop dep on dkms-omfs

* Fri Jul 25 2008 Thierry Vignaud <tv@mandriva.org> 0.1.0-4mdv2009.0
+ Revision: 248840
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Mar 11 2008 Götz Waschk <waschk@mandriva.org> 0.1.0-2mdv2008.1
+ Revision: 185026
- fix automatic deps of karma-sharp

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 0.1.0-1mdv2008.1
+ Revision: 140924
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat May 19 2007 Götz Waschk <waschk@mandriva.org> 0.1.0-1mdv2008.0
+ Revision: 28467
- fix buildrequires
- new version
- new URL
- split out library package
- add dll mapping for karma-sharp


* Wed Dec 13 2006 Götz Waschk <waschk@mandriva.org> 0.0.6-1mdv2007.0
+ Revision: 96209
- add README.urpmi about fstab setup
- add icon
- Import libkarma

* Wed Dec 13 2006 Götz Waschk <waschk@mandriva.org> 0.0.6-1mdv2007.1
- initial package

