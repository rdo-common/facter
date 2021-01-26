%if 0%{?rhel} && 0%{?rhel} <= 7
%global boost_suffix 169
%global cmake_suffix 3
%global cmake %%cmake%{?cmake_suffix}
%endif

Name:           facter
Version:        3.14.7
Release:        7%{?dist}
Summary:        Command and ruby library for gathering system information

License:        ASL 2.0
URL:            https://puppetlabs.com/facter
Source0:        https://downloads.puppetlabs.com/%{name}/%{name}-%{version}.tar.gz
Source1:        https://downloads.puppetlabs.com/%{name}/%{name}-%{version}.tar.gz.asc
Source2:        gpgkey-6F6B15509CF8E59E6E469F327F438280EF8D349F.gpg
Patch0:         shared_cpp_hcon.patch
Patch1:         %{name}-gcc11.patch

BuildRequires:  gnupg2
BuildRequires:  cmake%{?cmake_suffix}
BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  libcurl-devel
BuildRequires:  leatherman-devel
BuildRequires:  boost%{?boost_suffix}-devel
BuildRequires:  ruby-devel >= 1.9
BuildRequires:  yaml-cpp-devel
BuildRequires:  openssl-devel
BuildRequires:  libblkid-devel
BuildRequires:  cpp-hocon-devel
#BuildRequires:  whereami-devel

# autoreq is not picking this one up so be specific
Requires: leatherman%{?_isa}

%package devel
Summary:        Development libraries for building against facter
Requires:       %{name}%{?_isa} = %{version}-%{release}

%package -n ruby-%{name}
Summary:        Ruby bindings for facter
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ruby%{?_isa}

%description
Facter is a lightweight program that gathers basic node information about the
hardware and operating system. Facter is especially useful for retrieving
things like operating system names, hardware characteristics, IP addresses, MAC
addresses, and SSH keys.

Facter is extensible and allows gathering of node information that may be
custom or site specific. It is easy to extend by including your own custom
facts. Facter can also be used to create conditional expressions in Puppet that
key off the values returned by facts.

%description devel
The headers to link against libfacter in other applications.

%description -n ruby-%{name}
The ruby bindings for libfacter.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

%build
%cmake . -B%{_target_platform} \
  -DBOOST_INCLUDEDIR=%{_includedir}/boost%{?boost_suffix} \
  -DBOOST_LIBRARYDIR=%{_libdir}/boost%{?boost_suffix} \
  -DLeatherman_DIR=%{_libdir}/cmake%{?cmake_suffix}/leatherman \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  %{nil}
%make_build -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%check
# Tests depend too much on environment
# 1: -------------------------------------------------------------------------------
# 1: Scenario: using the filesystem resolver
# 1:       When: populating facts
# 1:       Then: non-tmpfs mounts should exist
# 1: -------------------------------------------------------------------------------
# 1: /builddir/build/BUILD/facter-3.14.2/lib/tests/facts/linux/filesystem_resolver.cc:37
# 1: ...............................................................................
# 1: 
# 1: /builddir/build/BUILD/facter-3.14.2/lib/tests/facts/linux/filesystem_resolver.cc:38: FAILED:
# 1:   REQUIRE( facts.query<facter::facts::map_value>("mountpoints./") )
# 1: with expansion:
# 1:   NULL
#make_build -C %{_target_platform} test

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
# Note that leatherman has a hardcoded libfacter.so path for the installation
# of the library for the bindings: https://tickets.puppetlabs.com/browse/FACT-1772
%{_libdir}/lib%{name}.so.*
%{_libdir}/lib%{name}.so
%{_mandir}/man8/%{name}*

%files devel
%{_includedir}/%{name}/

%files -n ruby-%{name}
%{ruby_vendorlibdir}/%{name}.rb

%ldconfig_scriptlets

%changelog
* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Jonathan Wakely <jwakely@redhat.com> - 3.14.7-6
- Rebuilt for Boost 1.75

* Sat Jan  9 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 3.14.7-5
- Rebuild for cpp-hocon 0.3.0

* Wed Nov 04 2020 Jeff Law <law@redhat.com> - 3.14.7-4
- Fix missing #includes for gcc-11

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 03 2020 Jonathan Wakely <jwakely@redhat.com> - 3.14.7-2
- Rebuild for Boost 1.73.0

* Tue Jan 28 2020 Adam Tkac <vonsch@gmail.com> - 3.14.7-1
- update to 3.14.7

* Fri Oct 18 2019 Richard Shaw <hobbes1069@gmail.com> - 3.14.2-2
- Rebuild for yaml-cpp 0.6.3.

* Wed Aug 14 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.14.2-1
- Update to 3.14.2

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 14 2018 Richard Shaw <hobbes1069@gmail.com> - 3.9.3-4
- Rebuild for yaml-cpp 0.6.0.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Jonathan Wakely <jwakely@redhat.com> - 3.9.3-2
- Rebuilt for Boost 1.66

* Tue Nov 07 2017 James Hogarth <james.hogarth@gmail.com> - 3.9.3-1
- new upstream release 3.9.3

* Wed Oct 25 2017 James Hogarth <james.hogarth@gmail.com> - 3.9.2-3
- Point to correct leatherman directory on cmake3 for epel7

* Thu Oct 19 2017 James Hogarth <james.hogarth@gmail.com> - 3.9.2-2
- rebuilt

* Wed Oct 04 2017 James Hogarth <james.hogarth@gmail.com> - 3.9.2-1
- Update to latest upstream version 3.9.2

* Mon Oct 02 2017 James Hogarth <james.hogarth@gmail.com> - 3.9.0-1
- Update to latest upstream version 3.9.0

* Wed Aug 30 2017 James Hogarth <james.hogarth@gmail.com> - 3.8.0-1
- Update to latest upstream version 3.8.0

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 20 2015 Orion Poplawski <orion@cora.nwra.com> - 2.4.4-1
- Update to 2.4.4

* Thu Apr 2 2015 Orion Poplawski <orion@cora.nwra.com> - 2.4.3-1
- Update to 2.4.3

* Fri Feb 13 2015 Orion Poplawski <orion@cora.nwra.com> - 2.4.1-1
- Update to 2.4.1

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Tue Jan 06 2015 Orion Poplawski <orion@cora.nwra.com> - 2.3.0-1
- Update to 2.3.0

* Fri Oct 10 2014 Michael Stahnke <stahnma@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0 as per bz#1108041

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 05 2014 Lubomir Rintel <lkundrak@v3.sk> - 2.0.1-2
- Fix el7 conditionals as suggested by Orion Poplawski (BZ #1087946)

* Tue Apr 29 2014 Sam Kottler <skottler@fedoraproject.org> - 2.0.1-1
- Update to to 2.0.1

* Tue Jan 28 2014 Todd Zullinger <tmz@pobox.com> - 1.7.4-1
- Update to 1.7.4
- Create /etc/facter/facts.d for external facts
- Send dmiddecode errors to /dev/null in the virtual fact (FACT-86)

* Tue Oct 8 2013 Sam Kottler <skottler@fedoraproject.org> - 1.7.3-1
- Update to 1.7.3 (BZ #1016817)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Sam Kottler <skottler@fedoraproject.org> 1.6.18-4
- Apply upstream patch to ensure the first non-127.0.0.1 interface

* Wed Apr 03 2013 Todd Zullinger <tmz@pobox.com> - 1.6.18-3
- Avoid warnings when virt-what produces no output

* Tue Apr 02 2013 Todd Zullinger <tmz@pobox.com> - 1.6.18-2
- Apply upstream patch to filter virt-what warnings from virtual fact

* Mon Mar 18 2013 Todd Zullinger <tmz@pobox.com> - 1.6.18-1
- Update to 1.6.18
- Restart puppet in %%postun (#806370)
- Require virt-what for improved KVM detection (#905592)
- Ensure man page is installed on EL < 7

* Tue Mar 12 2013 Vít Ondruch <vondruch@redhat.com> - 1.6.17-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Mon Feb 25 2013 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.6.17-1
- New upstream version, fixes rhbz #892734

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 04 2012 Michael Stahnke <stahnma@puppetlabs.com> - 1.6.16-1
- Update to 1.6.16

* Wed Nov 28 2012 Michael Stahnke <stahnma@puppetlabs.com> -  1.6.15-1
- Rebase to 1.6.15
- Put asc file back as Source1

* Fri Nov 09 2012 Michael Stahnke <stahnma@puppetlabs.com> - 1.6.13-2
- Add patch for ec2 fix
- Rebase to 1.6.14 via bz 871211

* Mon Oct 29 2012 Michael Stahnke <stahnma@puppetlabs.com> - 1.6.13-1
- Rebase to 1.6.13

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 05 2012 Todd Zullinger <tmz@pobox.com> - 1.6.6-1
- Update to 1.6.6

* Sun Feb 19 2012 Todd Zullinger <tmz@pobox.com> - 1.6.5-5
- Disable useless debuginfo generation (#795106, thanks to Ville Skyttä)
- Update summary and description
- Remove INSTALL from %%doc

* Wed Feb 15 2012 Todd Zullinger <tmz@pobox.com> - 1.6.5-4
- Only run rspec checks on Fedora >= 17

* Mon Feb 13 2012 Todd Zullinger <tmz@pobox.com> - 1.6.5-3
- Make spec file work for EPEL and Fedora
- Drop BuildArch: noarch and make dmidecode/pciutils deps arch-specific
- Make ec2 facts work on CentOS again (#790849, thanks to Jeremy Katz)
- Preserve timestamps when installing files

* Thu Feb 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.6.5-2
- Rebuilt for Ruby 1.9.3.

* Thu Jan 26 2012 Todd Zullinger <tmz@pobox.com> - 1.6.5-1
- Update to 1.6.5
- Require net-tools and pciutils, thanks to Dominic Cleal (#783749)

* Thu Jan 05 2012 Todd Zullinger <tmz@pobox.com> - 1.6.4-1
- Update to 1.6.4
- Require dmidecode (upstream #11041)

* Sat Oct 15 2011 Todd Zullinger <tmz@pobox.com> - 1.6.2-1
- Update to 1.6.2
- Update source URL

* Thu Sep 29 2011 Todd Zullinger <tmz@pobox.com> - 1.6.1-1
- Update to 1.6.1
- Minor spec file reformatting

* Wed Jul 27 2011 Todd Zullinger <tmz@pobox.com> - 1.6.0-2
- Update license tag, GPLv2+ -> ASL 2.0

* Thu Jul 14 2011 Todd Zullinger <tmz@pobox.com> - 1.6.0-1
- Update to 1.6.0

* Thu May 26 2011 Todd Zullinger <tmz@pobox.com> - 1.5.9-1
- Update to 1.5.9
- Improve Scientific Linux support, courtesy of Orion Poplawski (upstream #7682)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Aug 28 2010 Todd Zullinger <tmz@pobox.com> - 1.5.8-1
- Update to 1.5.8

* Fri Sep 25 2009 Todd Zullinger <tmz@pobox.com> - 1.5.7-1
- Update to 1.5.7
- Update #508037 patch from upstream ticket

* Wed Aug 12 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 1.5.5-3
- Fix #508037 or upstream #2355

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 22 2009 Todd Zullinger <tmz@pobox.com> - 1.5.5-1
- Update to 1.5.5
- Drop upstreamed libperms patch

* Sat Feb 28 2009 Todd Zullinger <tmz@pobox.com> - 1.5.4-1
- New version
- Use upstream install script

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep 09 2008 Todd Zullinger <tmz@pobox.com> - 1.5.2-1
- New version
- Simplify spec file checking for Fedora and RHEL versions

* Mon Sep  8 2008 David Lutterkort <dlutter@redhat.com> - 1.5.1-1
- New version

* Thu Jul 17 2008 David Lutterkort <dlutter@redhat.com> - 1.5.0-3
- Change 'mkdir' in install to 'mkdir -p'

* Thu Jul 17 2008 David Lutterkort <dlutter@redhat.com> - 1.5.0-2
- Remove files that were listed twice in files section

* Mon May 19 2008 James Turnbull <james@lovedthanlosty.net> - 1.5.0-1
- New version
- Added util and plist files

* Mon Sep 24 2007 David Lutterkort <dlutter@redhat.com> - 1.3.8-1
- Update license tag
- Copy all of lib/ into ruby_sitelibdir

* Thu Mar 29 2007 David Lutterkort <dlutter@redhat.com> - 1.3.7-1
- New version

* Fri Jan 19 2007 David Lutterkort <dlutter@redhat.com> - 1.3.6-1
- New version

* Thu Jan 18 2007 David Lutterkort <dlutter@redhat.com> - 1.3.5-3
- require which; facter is very unhappy without it

* Mon Nov 20 2006 David Lutterkort <dlutter@redhat.com> - 1.3.5-2
- Make require ruby(abi) and buildarch: noarch conditional for fedora 5 or
  later to allow building on older fedora releases

* Tue Oct 10 2006 David Lutterkort <dlutter@redhat.com> - 1.3.5-1
- New version

* Tue Sep 26 2006 David Lutterkort <dlutter@redhat.com> - 1.3.4-1
- New version

* Wed Sep 13 2006 David Lutterkort <dlutter@redhat.com> - 1.3.3-2
- Rebuilt for FC6

* Wed Jun 28 2006 David Lutterkort <dlutter@redhat.com> - 1.3.3-1
- Rebuilt

* Mon Jun 19 2006 Luke Kanies <luke@madstop.com> - 1.3.0-1
- Fixed spec file to work again with the extra memory and processor files.
- Require ruby(abi). Build as noarch
- Added memory.rb and processor.rb

* Mon Apr 17 2006 David Lutterkort <dlutter@redhat.com> - 1.1.4-4
- Rebuilt with changed upstream tarball

* Tue Mar 21 2006 David Lutterkort <dlutter@redhat.com> - 1.1.4-3
- Do not rely on install.rb, it will be deleted upstream

* Mon Mar 13 2006 David Lutterkort <dlutter@redhat.com> - 1.1.4-2
- Commented out noarch; requires fix for bz184199

* Mon Mar  6 2006 David Lutterkort <dlutter@redhat.com> - 1.1.4-1
- Removed unused macros

* Mon Feb  6 2006 David Lutterkort <dlutter@redhat.com> - 1.1.1-2
- Fix BuildRoot. Add dist to release tag

* Wed Jan 11 2006 David Lutterkort <dlutter@redhat.com> - 1.1.1-1
- Initial build.
