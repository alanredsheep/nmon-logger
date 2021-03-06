Name: nmon-logger-splunk-hec
Version: 2.0.10
Release: 0
Summary: nmon-logger for Splunk HEC
Source: %{name}.tar.gz
License: Apache 2.0

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-build
Group:          System/Base
Vendor:         Guilhem Marchand

%description
This package provides Nmon performance monitoring logging for your Linux systems, and use Splunk http input to transfer data to your Splunk infrastructure.
For more information, please see: https://github.com/guilhemmarchand/nmon-logger

%prep
%setup -n %{name}

%pre
grep 'nmon' /etc/group || mkgroup nmon
grep -E '^nmon:' || useradd -g nmon -d /etc/nmon-logger nmon

%build
# Nothing to build

%install
# create directories where the files will be located
mkdir -p $RPM_BUILD_ROOT/etc/nmon-logger
mkdir -p $RPM_BUILD_ROOT/etc/nmon-logger/default
mkdir -p $RPM_BUILD_ROOT/etc/nmon-logger/bin
mkdir -p $RPM_BUILD_ROOT/etc/nmon-logger/bin/nmon_external_cmd
mkdir -p $RPM_BUILD_ROOT/var/log/nmon-logger
mkdir -p $RPM_BUILD_ROOT/var/spool/cron/crontabs

cp etc/nmon-logger/default/nmon.conf $RPM_BUILD_ROOT/etc/nmon-logger/default/
cp etc/nmon-logger/default/app.conf $RPM_BUILD_ROOT/etc/nmon-logger/default/
cp etc/nmon-logger/default/nmonparser_config.json $RPM_BUILD_ROOT/etc/nmon-logger/default/
cp etc/nmon-logger/bin/linux.tgz $RPM_BUILD_ROOT/etc/nmon-logger/bin/
cp etc/nmon-logger/bin/nmon2* $RPM_BUILD_ROOT/etc/nmon-logger/bin/
cp etc/nmon-logger/bin/nmon_cleaner* $RPM_BUILD_ROOT/etc/nmon-logger/bin/
cp etc/nmon-logger/bin/nmon_helper.sh $RPM_BUILD_ROOT/etc/nmon-logger/bin/
cp etc/nmon-logger/bin/fifo_* $RPM_BUILD_ROOT/etc/nmon-logger/bin/
cp etc/nmon-logger/bin/nmon_external_cmd/*.sh $RPM_BUILD_ROOT/etc/nmon-logger/bin/nmon_external_cmd/
cp etc/nmon-logger/bin/nmon_helper.sh $RPM_BUILD_ROOT/etc/nmon-logger/bin/
cp etc/nmon-logger/bin/hec_wrapper.sh $RPM_BUILD_ROOT/etc/nmon-logger/bin/
cp etc/nmon-logger/bin/logrotate.sh $RPM_BUILD_ROOT/etc/nmon-logger/bin/
cp -r AIX_support $RPM_BUILD_ROOT/etc/nmon-logger/

# put the files in to the relevant directories.
%post
chown -R nmon:nmon /etc/nmon-logger
cp /etc/nmon-logger/AIX_support/crontab.conf /var/spool/cron/crontabs/nmon
ps -ef | grep '/usr/sbin/cron' | grep -v grep | awk '{print $2}' | xargs kill
echo
echo Nmon logger has been successfully installed. Within next minutes, the performance and configuration data collection will start automatically.
echo Please check the content of "/var/log/nmon-logger/"
echo You will also find a new process running under nmon account, you can get the current list of running processes for the nmon account: "ps -fu nmon"
echo

%postun
echo
if [ "$1" = "0" ]; then
if [ `ps -fu nmon | grep -v 'PID' | wc -l` -ne 0 ]; then echo "Killing running nmon processes:"; echo "**** list of running processes: ****"; echo `ps -fu nmon | grep '/var/log/nmon-logger' | grep topas_nmon`; ps -fu nmon | grep '/var/log/nmon-logger' | grep topas_nmon | awk '{print $2}' | xargs kill; sleep 5; fi
echo "Removing /etc/nmon-logger remaining files."; rm -rf /etc/nmon-logger
echo "Removing /var/log/nmon-logger remaining files."; rm -rf /var/log/nmon-logger
echo "Removing nmon user account"; userdel nmon
echo
echo Nmon logger has been successfully uninstalled.
echo
fi

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf %{_tmppath}/%{name}

# list files owned by the package here
%files
%defattr(0644,root,root)
%attr(0755, nmon, nmon) /etc/nmon-logger
%attr(0755, nmon, nmon) /var/log/nmon-logger
