#
# spec file for package butt
#
# Copyright (c) 2017 - 2020 Radio Bern RaBe
#                           https://rabe.ch
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public 
# License as published  by the Free Software Foundation, version
# 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License  along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
# Please submit enhancements, bugfixes or comments via GitHub:
# https://github.com/radiorabe/centos-rpm-butt
#

# Conditional build support
# add --with aac option, i.e. disable AAC by default
%bcond_with aac

# add --without flac option, i.e. enable FLAC by default
%bcond_without flac

# add --without opus option, i.e. enable Opus by default
%bcond_without opus

# add --without lame option, i.e. enable Lame/MP3 by default
%bcond_without lame

# add --without vorbis option, i.e. enable Vorbis by default
%bcond_without vorbis

# icons root directory
%global iconsdir %{_datadir}/icons

Name:           butt
Version:        0.1.19
Release:        1%{?dist}
Summary:        butt is an easy to use, multi OS streaming tool

License:        GPLv2 
URL:            http://danielnoethen.de/butt/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  dbus-devel
BuildRequires:  fltk-devel
BuildRequires:  gcc-c++
BuildRequires:  libsamplerate-devel
BuildRequires:  portaudio-devel

%if %{with aac}
BuildRequires:  fdk-aac-devel
%endif

%if %{with flac}
BuildRequires:  flac-devel
%endif

%if %{with lame}
BuildRequires:  lame-devel
%endif

%if %{with opus}
BuildRequires:  opus-devel
%endif

%if %{with vorbis}
BuildRequires:  libvorbis-devel
BuildRequires:  libogg-devel
%endif


%description
butt (broadcast using this tool) is an easy to use, multi OS streaming tool.
It supports SHOUTcast and Icecast and runs on Linux, Mac OS X and Windows.
The main purpose of butt is to stream live audio data from your computers Mic
or Line input to an Shoutcast or Icecast server. Recording is also possible.
It is NOT intended to be a server by itself or automatically stream a set of
audio files.


%prep
%setup -q


%build
# The configure script currently seems to have some issues while detecting the
# X11 and fltk libraries as it doesn't add them to the linker. We help it here
# a bit to avoid the following compile errors:
# /bin/ld: FLTK/Fl_My_Native_File_Chooser.o: undefined reference to symbol 'XNextEvent'
# /bin/ld: FLTK/flgui.o: undefined reference to symbol '_ZN16Fl_Double_Window4hideEv'
%configure LIBS="-lX11 -lfltk" %{!?with_aac:--disable-aac}
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install

# The desktop menu category "Sound" is invalid, replace it with appropriate
# categories in accordance with the "Desktop Menu Specification"
# https://specifications.freedesktop.org/menu-spec/latest/apa.html
desktop-file-install \
    --remove-category="Sound" \
    --add-category="AudioVideo;Audio" \
    --dir=%{buildroot}%{_datadir}/applications \
    usr/share/applications/%{name}.desktop \

# Install the various icons according to the "Icon Theme Specification"
# https://specifications.freedesktop.org/icon-theme-spec/icon-theme-spec-latest.html
for size in 16 22 24 32 48 64 96 128 256 512; do
    format="${size}x${size}"
    install -d %{buildroot}%{iconsdir}/hicolor/${format}/apps
    install icons/icon_${format}.png \
            %{buildroot}%{iconsdir}/hicolor/${format}/apps/%{name}.png
done

install -d %{buildroot}%{iconsdir}/hicolor/scalable/apps
install icons/icon_scalable.svg \
        %{buildroot}%{iconsdir}/hicolor/scalable/apps/%{name}.png


%post
# https://fedoraproject.org/wiki/Packaging:Scriptlets#Icon_Cache
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
# https://fedoraproject.org/wiki/Packaging:Scriptlets#Icon_Cache
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
# https://fedoraproject.org/wiki/Packaging:Scriptlets#Icon_Cache
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc ChangeLog NEWS README KNOWN_BUGS
%{_bindir}/*
%{_datadir}/applications/*.desktop
%attr(0644, -, -) %{iconsdir}/*/*/*/*.png


%changelog
* Sat Jan 04 2020 Christian Affolter <c.affolter@purplehaze.ch> - 0.1.19-1
- Bump to 0.1.19
- Updated project website URL

* Sun May 12 2019 Christian Affolter <c.affolter@purplehaze.ch> - 0.1.18-1
- Bump to 0.1.18

* Tue Apr 16 2019 Lucas Bickel <hairmare@rabe.ch> - 0.1.17-1
- Bump to 0.1.17
- Disable AAC in default build

* Thu Sep 21 2017 Christian Affolter <c.affolter@purplehaze.ch> - 0.1.16-3
- Initial release
