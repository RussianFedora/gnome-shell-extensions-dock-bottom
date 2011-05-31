%global commit g63dd27c

Name:           gnome-shell-extensions-dock-bottom
Version:        3.0.2
Release:        1.%{commit}git%{?dist}
Summary:        Modify and extend GNOME Shell functionality and behavior
Group:          User Interface/Desktops
License:        GPLv2+ 
URL:            http://live.gnome.org/GnomeShell/Extensions

#  using git archive since upstream hasn't created tarballs.  Picking up a snapshot from master for a couple of minor but relevant changes
#  git archive --format=tar --prefix=gnome-shell-extensions/ git_commithash | xz > gnome-shell-extensions-<git_commithash_abbr>.tar.xz
Source0:        gnome-shell-extensions-%{commit}.tar.xz
Patch0:		gnome-shell-extensions-dock-can-be-bottom.patch

# since we build from a git checkout
BuildRequires:  gnome-common
BuildRequires:  intltool
BuildRequires:  glib2-devel

Requires:       gnome-shell >= 3.0.1
BuildArch:      noarch

Conflicts:	gnome-shell-extensions-dock

%description
Shows a dock-style task switcher on the right side of the screen permanently.

%prep
%setup -q -n gnome-shell-extensions
%patch0 -p1 -b .extensions-dock-can-be-bottom

# with any 3.0.x release
sed -i "s|3.0.1|3.0|g" configure.ac

%build
# since we build from a git checkout
[ -x autogen.sh ] && NOCONFIGURE=1 ./autogen.sh 

%configure  --enable-extensions="dock"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale


%posttrans
glib-compile-schemas --allow-any-name %{_datadir}/glib-2.0/schemas || :


%postun
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files
%defattr(-,root,root,-)
%{_datadir}/glib-2.0/schemas/org.gnome.shell.extensions.dock.gschema.xml
%{_datadir}/gnome-shell/extensions/dock*


%changelog
* Tue May 31 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 3.0.2-1.g63dd27cgit
- dock can be bottom
