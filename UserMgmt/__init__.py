import subprocess
import sys

def addUser(pkgName):
    subprocess.run(["useradd", "-g", "install", "-m", name])

def addInstallGroup():
    addGroup("install")
    givePermissions("install")

def givePermissions(group):
    # Add valid install directories
    installDirs = ["/usr/bin", "/usr/sbin", "/usr/include", "/usr/lib",
        "/usr/man/man1", "/usr/man/man2", "/usr/man/man3", "/usr/man/man4",
        "/usr/man/man5", "/usr/man/man6", "/usr/man/man7", "/usr/man/man8",
        "/usr/doc", "/usr/info", "/usr/local/man/man1", "/usr/local/man/man2",
        "/usr/local/man/man3", "/usr/local/man/man4", "/usr/local/man/man5",
        "/usr/local/man/man6", "/usr/local/man/man7", "/usr/local/man/man8",
        "/usr/local/doc", "/usr/local/info", "/usr/share", "/usr/share/dict",
        "/usr/share/doc", "/usr/share/info", "/usr/share/locale", "/usr/share/man/man1",
        "/usr/share/man/man2", "/usr/share/man/man3", "/usr/share/man/man4",
        "/usr/share/man/man5", "/usr/share/man/man6", "/usr/share/man/man7",
        "/usr/share/man/man8", "/usr/share/nls", "/usr/share/misc", "/usr/share/terminfo",
        "/usr/share/zoneinfo", "/usr/share/i18n", "/usr/share/aclocal", "/usr/local/bin",
        "/usr/local/etc", "/usr/local/include", "/usr/local/lib", "/usr/local/sbin",
        "/usr/local/share", "/usr/local/share/dict", "/usr/local/share/doc",
        "/usr/local/share/info", "/usr/local/share/locale", "/usr/local/share/man/man1",
        "/usr/local/share/man/man2", "/usr/local/share/man/man3", "/usr/local/share/man/man4",
        "/usr/local/share/man/man5", "/usr/local/share/man/man6", "/usr/local/share/man/man7",
        "/usr/local/share/man/man8", "/usr/local/share/nls", "/usr/local/share/misc",
        "/usr/local/share/terminfo", "/usr/local/share/zoneinfo", "/opt", "/opt/doc",
        "/opt/info", "/opt/bin", "/opt/include", "/opt/lib", "/opt/man/man1", "/opt/man/man2",
        "/opt/man/man3", "/opt/man/man4", "/opt/man/man5", "/opt/man/man6", "/opt/man/man7",
        "/opt/man/man8", "/var/lib", "/var/opt", "/etc", "/etc/opt", "/sbin", "/bin", "/lib"]
    for i in installDirs:
        try:
            subprocess.run(['chgrp', group, i])
            subprocess.run(['chmod', 'g+w,o+t', i])
        except:
            sys.exit("Failed to create install permission for " + i)

def addGroup(groupName):
        try:
            subprocess.run(['groupadd', '-r', groupName])
        except:
            sys.exit('Failed to create group "' +groupName)